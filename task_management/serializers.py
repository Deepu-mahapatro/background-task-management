
from rest_framework import serializers

from .models import Task


# ==================================================
# TASK CREATE SERIALIZER
# ==================================================

class TaskCreateSerializer(serializers.Serializer):

    task_type = serializers.ChoiceField(
        choices=Task.TaskType.choices
    )

    payload = serializers.JSONField()

    metadata = serializers.JSONField(
        required=False,
        default=dict
    )

    # Idempotency key supplied by the client
    idempotency_key = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=128
    )

    def validate_payload(self, payload):

        if not isinstance(payload, dict):
            raise serializers.ValidationError(
                "Payload must be a JSON object."
            )

        task_type = self.initial_data.get("task_type")

        required_fields = {
            "EMAIL": ["recipient", "subject", "message"],
            "PDF_GENERATION": ["content"],
            "FILE_PROCESSING": ["content"]
        }

        for field in required_fields.get(task_type, []):

            if not payload.get(field):
                raise serializers.ValidationError(
                    f"{field} is required."
                )

        if task_type == "EMAIL":

            email = serializers.EmailField()

            payload["recipient"] = email.run_validation(
                payload["recipient"]
            )

        return payload

    def validate_metadata(self, metadata):

        if not isinstance(metadata, dict):
            raise serializers.ValidationError(
                "Metadata must be a JSON object."
            )

        return metadata


# ==================================================
# TASK READ SERIALIZER
# ==================================================

class TaskReadSerializer(serializers.ModelSerializer):

    class Meta:

        model = Task

        fields = [
            "task_id",
            "idempotency_key",
            "task_type",
            "payload",
            "metadata",
            "status",
            "result",
            "error_message",
            "retry_count",
            "is_dead_letter",
            "created_at",
            "updated_at"
        ]

        read_only_fields = fields
