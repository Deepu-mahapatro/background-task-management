
import uuid

from django.db import models


class Task(models.Model):

    class TaskType(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        PDF_GENERATION = "PDF_GENERATION", "PDF Generation"
        FILE_PROCESSING = "FILE_PROCESSING", "File Processing"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RECEIVED = "RECEIVED", "Received"
        STARTED = "STARTED", "Started"
        RETRY = "RETRY", "Retry"
        SUCCESS = "SUCCESS", "Success"
        FAILURE = "FAILURE", "Failure"
        REVOKED = "REVOKED", "Revoked"

    id = models.BigAutoField(primary_key=True)

    task_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    idempotency_key = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True
    )

    task_type = models.CharField(
        max_length=30,
        choices=TaskType.choices
    )

    payload = models.JSONField(default=dict)
    metadata = models.JSONField(default=dict, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    result = models.JSONField(null=True, blank=True)

    error_message = models.TextField(null=True, blank=True)

    retry_count = models.PositiveIntegerField(default=0)

    is_dead_letter = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task_type} - {self.task_id}"
