import logging

from celery.signals import (
    task_retry,
    task_failure,
    task_success
)

from django.dispatch import receiver

from .models import Task


logger = logging.getLogger(__name__)


# 1. When a task requests retry
@receiver(task_retry)
def handle_task_retry(
    sender=None,
    request=None,
    reason=None,
    **kwargs
):

    task_id = getattr(request, "id", None)

    if not task_id:
        return

    retry_count = getattr(
        request,
        "retries",
        0
    )

    Task.objects.filter(
        task_id=task_id
    ).update(
        status="RETRY",
        retry_count=retry_count,
        error_message=str(reason)
    )


# 2. When a task finally fails
@receiver(task_failure)
def handle_task_failure(
    sender=None,
    task_id=None,
    exception=None,
    **kwargs
):

    if not task_id:
        return

    task = Task.objects.filter(
        task_id=task_id
    ).first()

    if not task:
        return

    request = getattr(sender, "request", None)

    retry_count = getattr(
        request,
        "retries",
        0
    )

    task.status = "FAILURE"

    task.retry_count = retry_count

    task.error_message = str(exception)

    # Move final failures into application-level DLQ
    task.is_dead_letter = True

    task.save(
        update_fields=[
            "status",
            "retry_count",
            "error_message",
            "is_dead_letter",
            "updated_at"
        ]
    )

    logger.error(
        "Task moved to DLQ: %s",
        task_id
    )


# 3. When a task succeeds
@receiver(task_success)
def handle_task_success(
    sender=None,
    task_id=None,
    result=None,
    **kwargs
):

    if not task_id:
        return

    Task.objects.filter(
        task_id=task_id
    ).update(
        status="SUCCESS",
        result=result,
        error_message=None,
        is_dead_letter=False
    )

    logger.info(
        "Task completed successfully: %s",
        task_id
    )