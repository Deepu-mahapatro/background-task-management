
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from celery.result import AsyncResult

from .models import Task

from .serializers import (
    TaskCreateSerializer,
    TaskReadSerializer
)

from .services import (
    create_task,
    publish_task,
    recover_failed_task
)


# --------------------------------------------------
# 1. CREATE TASK API
# --------------------------------------------------

class TaskCreateView(APIView):

    def post(self, request):

        # Step 1: Validate incoming request data
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Create a new task or retrieve an existing one
        task, created = create_task(
            task_type=serializer.validated_data["task_type"],
            payload=serializer.validated_data["payload"],
            metadata=serializer.validated_data.get("metadata", {}),
            idempotency_key=serializer.validated_data.get(
                "idempotency_key"
            )
        )

        # Step 3: Publish only newly created tasks
        if created:
            publish_task(task)

        # Step 4: Serialize task information
        response_serializer = TaskReadSerializer(task)

        # Step 5: Return appropriate HTTP response
        return Response(
            response_serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )


# --------------------------------------------------
# 2. TASK STATUS AND RESULT API
# --------------------------------------------------

class TaskStatusView(APIView):

    def get(self, request, task_id):

        # Step 1: Find task in MySQL
        task = get_object_or_404(
            Task,
            task_id=task_id
        )

        # Step 2: Retrieve Celery task information
        celery_result = AsyncResult(
            str(task.task_id)
        )

        # Step 3: Serialize MySQL task information
        response_data = TaskReadSerializer(task).data

        # Step 4: Preserve MySQL status separately
        response_data["database_status"] = task.status

        # Step 5: Return Celery execution state
        response_data["status"] = celery_result.state

        # Step 6: Return successful task result
        if celery_result.state == "SUCCESS":

            response_data["result"] = celery_result.result

        # Step 7: Return failure information
        elif celery_result.state == "FAILURE":

            response_data["result"] = None

            response_data["error_message"] = str(
                celery_result.result
            )

        else:

            response_data["result"] = None

        # Step 8: Add task completion information
        response_data["ready"] = celery_result.ready()

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )


# --------------------------------------------------
# 3. FAILED TASK LIST API
# --------------------------------------------------

class FailedTaskListView(ListAPIView):

    serializer_class = TaskReadSerializer

    queryset = Task.objects.filter(
        is_dead_letter=True
    ).order_by("-created_at")


# --------------------------------------------------
# 4. TASK RECOVERY API
# --------------------------------------------------

class TaskRecoveryView(APIView):

    def post(self, request, task_id):

        # Step 1: Find failed task in MySQL
        task = get_object_or_404(
            Task,
            task_id=task_id
        )

        try:

            # Step 2: Execute recovery service
            celery_result = recover_failed_task(task)

        except ValueError as exc:

            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:

            return Response(
                {
                    "detail": "Unable to publish recovery task"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Step 3: Return recovery submission information
        return Response(
            {
                "task_id": str(task.task_id),
                "celery_task_id": celery_result.id,
                "status": "PENDING",
                "message": "Task submitted for recovery"
            },
            status=status.HTTP_202_ACCEPTED
        )
