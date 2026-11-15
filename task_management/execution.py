from .models import Task


def claim_task_execution(task_id):

    # Atomically change PENDING or RETRY to STARTED.
    updated_rows = Task.objects.filter(
        task_id=task_id,
        status__in=[
            Task.Status.PENDING,
            Task.Status.RETRY
        ]
    ).update(
        status=Task.Status.STARTED
    )

    # Exactly one worker can successfully claim this state.
    return updated_rows == 1