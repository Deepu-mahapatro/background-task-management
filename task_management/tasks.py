
import time

from celery import shared_task

from .execution import claim_task_execution


# ==========================================================
# 1. BUSINESS TASKS
# ==========================================================


# ----------------------------------------------------------
# EMAIL TASK
# ----------------------------------------------------------

@shared_task(bind=True)
def send_email_task(self, recipient, subject, message):

    task_id = self.request.id

    # Prevent duplicate execution
    if not claim_task_execution(task_id):
        print("Duplicate email execution prevented:", task_id)

        return {
            "task_id": task_id,
            "status": "SKIPPED_DUPLICATE",
            "message": "Task already claimed or completed"
        }

    print("Executing Email Task:", task_id)
    print("Sending email to:", recipient)

    # Actual email implementation goes here.

    return {
        "task_id": task_id,
        "message": "Email task executed",
        "recipient": recipient
    }


# ----------------------------------------------------------
# PDF GENERATION TASK
# ----------------------------------------------------------

@shared_task(bind=True)
def generate_pdf_task(self, content):

    task_id = self.request.id

    # Prevent duplicate execution
    if not claim_task_execution(task_id):
        print("Duplicate PDF execution prevented:", task_id)

        return {
            "task_id": task_id,
            "status": "SKIPPED_DUPLICATE",
            "message": "Task already claimed or completed"
        }

    print("Executing PDF Task:", task_id)
    print("Generating PDF")

    # Actual PDF generation implementation goes here.

    return {
        "task_id": task_id,
        "message": "PDF task executed",
        "content": content
    }


# ----------------------------------------------------------
# FILE PROCESSING TASK
# ----------------------------------------------------------

@shared_task(bind=True)
def process_file_task(self, content):

    task_id = self.request.id

    # Prevent duplicate execution
    if not claim_task_execution(task_id):
        print("Duplicate file execution prevented:", task_id)

        return {
            "task_id": task_id,
            "status": "SKIPPED_DUPLICATE",
            "message": "Task already claimed or completed"
        }

    print("Executing File Processing Task:", task_id)
    print("Processing file content")

    word_count = len(content.split())

    return {
        "task_id": task_id,
        "message": "File processing completed",
        "word_count": word_count
    }


# ==========================================================
# 2. TASK LIFECYCLE TEST
# ==========================================================

@shared_task(bind=True)
def lifecycle_test_task(self):

    print("Task ID:", self.request.id)
    print("Task execution started")

    time.sleep(15)

    print("Task execution completed")

    return {
        "message": "Lifecycle test successful",
        "task_id": self.request.id
    }


# ==========================================================
# 3. EXECUTION TIME AND RESULT TEST
# ==========================================================

@shared_task(bind=True)
def execution_result_test_task(self, duration):

    start_time = time.perf_counter()

    print("Task ID:", self.request.id)
    print("Task execution started")

    time.sleep(duration)

    print("Task execution completed")

    execution_time = round(
        time.perf_counter() - start_time,
        3
    )

    return {
        "task_id": self.request.id,
        "message": "Task completed successfully",
        "requested_duration": duration,
        "execution_time_seconds": execution_time
    }


# ==========================================================
# 4. ACKNOWLEDGEMENT TEST TASKS
# ==========================================================


# Early Acknowledgement

@shared_task(
    bind=True,
    acks_late=False
)
def early_ack_test_task(self, duration):

    print("Early ACK Task ID:", self.request.id)
    print("Early ACK: Task execution started")

    time.sleep(duration)

    print("Early ACK: Task execution completed")

    return {
        "task_id": self.request.id,
        "acknowledgement": "EARLY",
        "message": "Early ACK task completed"
    }


# Late Acknowledgement

@shared_task(
    bind=True,
    acks_late=True
)
def late_ack_test_task(self, duration):

    print("Late ACK Task ID:", self.request.id)
    print("Late ACK: Task execution started")

    time.sleep(duration)

    print("Late ACK: Task execution completed")

    return {
        "task_id": self.request.id,
        "acknowledgement": "LATE",
        "message": "Late ACK task completed"
    }


# Message Redelivery

@shared_task(
    bind=True,
    acks_late=True
)
def ack_redelivery_test_task(self, duration, marker):

    task_id = self.request.id

    delivery_info = self.request.delivery_info or {}

    redelivered = delivery_info.get("redelivered", False)

    print("--------------------------------")
    print("ACK REDELIVERY TEST")
    print("Task ID:", task_id)
    print("Marker:", marker)
    print("Redelivered:", redelivered)
    print("Task execution started")
    print("--------------------------------")

    time.sleep(duration)

    print("Task execution completed")

    return {
        "task_id": task_id,
        "marker": marker,
        "redelivered": redelivered,
        "message": "Redelivery test completed"
    }


# Ordinary Task Failure

@shared_task(
    bind=True,
    acks_late=True
)
def ack_failure_test_task(self):

    print("Failure ACK test started")
    print("Task ID:", self.request.id)

    raise ValueError(
        "Simulated task failure for ACK testing"
    )


# Worker-loss Configuration

@shared_task(
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True
)
def worker_lost_config_test_task(self):

    print("Worker-loss configuration test")
    print("Task ID:", self.request.id)

    return {
        "task_id": self.request.id,
        "message": "Worker-loss configuration test completed"
    }


# ==========================================================
# 5. AUTOMATIC RETRY TEST
# ==========================================================

@shared_task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_kwargs={
        "max_retries": 3
    },
    retry_backoff=True,
    retry_backoff_max=30,
    retry_jitter=False
)
def retry_demo_task(self, fail_times=2):

    attempt = self.request.retries + 1

    print("--------------------------------")
    print("RETRY DEMONSTRATION TASK")
    print("Task ID:", self.request.id)
    print("Attempt:", attempt)
    print("Retry count:", self.request.retries)
    print("--------------------------------")

    if self.request.retries < fail_times:

        print("Simulating connection failure")

        raise ConnectionError(
            "External service temporarily unavailable"
        )

    print("Task completed successfully")

    return {
        "task_id": self.request.id,
        "attempts": attempt,
        "retries": self.request.retries,
        "message": "Task completed successfully"
    }


# ==========================================================
# 6. RETRY JITTER TEST
# ==========================================================

@shared_task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_kwargs={
        "max_retries": 3
    },
    retry_backoff=True,
    retry_backoff_max=30,
    retry_jitter=True
)
def retry_jitter_demo_task(self, fail_times=2):

    attempt = self.request.retries + 1

    print("--------------------------------")
    print("RETRY JITTER DEMO")
    print("Task ID:", self.request.id)
    print("Attempt:", attempt)
    print("Retry count:", self.request.retries)
    print("--------------------------------")

    if self.request.retries < fail_times:

        raise ConnectionError(
            "Simulated temporary connection failure"
        )

    return {
        "task_id": self.request.id,
        "attempts": attempt,
        "retries": self.request.retries,
        "message": "Task completed successfully"
    }


# ==========================================================
# 7. WORKER RECOVERY TEST
# ==========================================================

@shared_task(
    bind=True,
    acks_late=True
)
def recovery_demo_task(self, duration=30):

    task_id = self.request.id

    delivery_info = self.request.delivery_info or {}

    redelivered = delivery_info.get("redelivered", False)

    print("--------------------------------")
    print("WORKER RECOVERY TEST")
    print("Task ID:", task_id)
    print("Redelivered:", redelivered)
    print("Execution started")
    print("--------------------------------")

    time.sleep(duration)

    print("Execution completed")

    return {
        "task_id": task_id,
        "redelivered": redelivered,
        "message": "Recovery test completed"
    }


# ==========================================================
# 8. POISON MESSAGE TEST
# ==========================================================

@shared_task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_kwargs={
        "max_retries": 2,
        "countdown": 2
    },
    retry_backoff=False
)
def poison_message_test_task(self):

    print("--------------------------------")
    print("POISON MESSAGE TEST")
    print("Task ID:", self.request.id)
    print("Retry count:", self.request.retries)
    print("--------------------------------")

    raise ConnectionError(
        "Permanent test failure"
    )
