
from django.db import IntegrityError, transaction

from rest_framework.exceptions import ValidationError

from .models import Task

from .tasks import (
    send_email_task,
    generate_pdf_task,
    process_file_task
)


# ==================================================
# 1. CREATE TASK
# ==================================================

def create_task(
    *,
    task_type,
    payload,
    metadata=None,
    idempotency_key=None
):

    # No idempotency key: create a normal task.
    if not idempotency_key:

        task = Task.objects.create(
            task_type=task_type,
            payload=payload,
            metadata=metadata or {}
        )

        return task, True

    try:

        with transaction.atomic():

            task = Task.objects.create(
                task_type=task_type,
                payload=payload,
                metadata=metadata or {},
                idempotency_key=idempotency_key
            )

            return task, True

    except IntegrityError:

        # Check whether this key already exists.
        existing_task = Task.objects.filter(
            idempotency_key=idempotency_key
        ).first()

        # If no matching task exists, this was
        # another database integrity problem.
        if existing_task is None:
            raise

        # Prevent reuse of the key for different data.
        if (
            existing_task.task_type != task_type
            or existing_task.payload != payload
        ):

            raise ValidationError({
                "idempotency_key":
                "This key was already used with different task data."
            })

        # Return the previously created task.
        return existing_task, False


# ==================================================
# 2. PUBLISH TASK
# ==================================================

def publish_task(task):

    if task.task_type == Task.TaskType.EMAIL:

        result = send_email_task.apply_async(
            args=[
                task.payload["recipient"],
                task.payload["subject"],
                task.payload["message"]
            ],
            task_id=str(task.task_id)
        )

    elif task.task_type == Task.TaskType.PDF_GENERATION:

        result = generate_pdf_task.apply_async(
            args=[
                task.payload["content"]
            ],
            task_id=str(task.task_id)
        )

    elif task.task_type == Task.TaskType.FILE_PROCESSING:

        result = process_file_task.apply_async(
            args=[
                task.payload["content"]
            ],
            task_id=str(task.task_id)
        )

    else:
        raise ValueError("Unsupported task type")

    return result


# ==================================================
# 3. RECOVER FAILED TASK
# ==================================================

def recover_failed_task(task):

    # Only allow recovery of failed tasks.
    if task.status != Task.Status.FAILURE:
        raise ValueError(
            "Only failed tasks can be recovered"
        )

    if not task.is_dead_letter:
        raise ValueError(
            "Task is not in the Dead Letter Queue"
        )

    # Preserve previous failure information.
    metadata = dict(task.metadata or {})

    metadata["previous_retry_count"] = task.retry_count

    metadata["recovery_count"] = (
        metadata.get("recovery_count", 0) + 1
    )

    # Reset task state before republishing.
    task.status = Task.Status.PENDING
    task.result = None
    task.error_message = None
    task.retry_count = 0
    task.is_dead_letter = False
    task.metadata = metadata

    task.save(
        update_fields=[
            "status",
            "result",
            "error_message",
            "retry_count",
            "is_dead_letter",
            "metadata",
            "updated_at"
        ]
    )

    try:

        celery_result = publish_task(task)

        return celery_result

    except Exception:

        # Restore failure state if publishing fails.
        task.status = Task.Status.FAILURE
        task.is_dead_letter = True

        task.save(
            update_fields=[
                "status",
                "is_dead_letter",
                "updated_at"
            ]
        )

        raise
