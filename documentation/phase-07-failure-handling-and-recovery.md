# Phase 7 – Failure Handling and Recovery

## 1. Overview

Phase 7 introduces failure handling and recovery mechanisms in Celery.

It explains how the system handles task execution failures, retries unsuccessful tasks, manages execution timeouts, and responds to worker or broker failures.

The primary objective is to ensure that temporary failures do not permanently interrupt background processing and that failed tasks can be handled appropriately.

## 2. Concepts Covered

1. Task Failure
2. Exception Handling
3. Automatic Retry
4. Manual Retry
5. Maximum Retry Attempts
6. Retry Delay
7. Exponential Backoff
8. Task Time Limits
9. Soft Time Limit
10. Hard Time Limit
11. Task Failure States
12. Worker Failure Handling
13. Broker Failure Handling
14. Task Recovery
15. Failed Task Management

## 3. Architecture / Internal Flow

The failure handling workflow follows this sequence:

1. Celery worker receives a task message.
2. Worker starts task execution.
3. An exception or unexpected error occurs.
4. Celery identifies the task failure.
5. The configured retry policy is evaluated.
6. If retries are available, another execution attempt is scheduled.
7. The worker executes the task again.
8. If the task succeeds, its state becomes SUCCESS.
9. If retry attempts are exhausted, the task reaches FAILURE.
10. The application records the appropriate task status in MySQL.

**Architecture flow:**

Redis Broker → Celery Worker → Task Execution → Failure Detection → Retry Policy → Retry Execution → SUCCESS / FAILURE

## 4. Implementation Details

The following components are involved in this phase:

| Component | Responsibility |
|---|---|
| Exception Handling | Handles errors during task execution |
| Automatic Retry | Retries tasks according to configured conditions |
| Manual Retry | Allows retry to be requested explicitly |
| `max_retries` | Defines the maximum retry attempts |
| `countdown` | Specifies the delay before another attempt |
| Exponential Backoff | Increases retry delay after repeated failures |
| Soft Time Limit | Raises an exception when the soft execution limit is reached |
| Hard Time Limit | Terminates task execution after the hard limit |
| FAILURE State | Indicates unsuccessful task execution |
| Recovery Mechanism | Handles incomplete or interrupted task processing |

### Retry Mechanism

Retry allows a task to be executed again after a failure.

Two common retry approaches are:

- **Automatic retry:** Configured exceptions trigger retries automatically.
- **Manual retry:** The task explicitly requests another attempt using Celery's retry mechanism.

### Important Retry Parameters

| Parameter | Purpose |
|---|---|
| `max_retries` | Maximum number of retry attempts |
| `countdown` | Delay before the next retry |
| `default_retry_delay` | Default retry delay |
| `retry_backoff` | Enables exponential retry delay |
| `retry_jitter` | Adds randomness to retry delays |
| `autoretry_for` | Specifies exceptions that trigger automatic retries |

### Task Time Limits

Task time limits prevent tasks from running indefinitely.

- **Soft time limit:** Raises a timeout exception that the task may handle.
- **Hard time limit:** Forces task execution to stop after the configured limit.

### Worker and Broker Failure Handling

Worker failures can interrupt task execution. Broker failures can prevent task publishing or message consumption.

Recovery behavior depends on acknowledgement settings, broker transport behavior, task configuration, and application-level recovery mechanisms.

### Failed Task Management

Failed tasks should be recorded and monitored so that developers can identify the cause, determine whether another attempt is appropriate, and avoid repeatedly executing permanently invalid tasks.

## 5. Commands

The following commands are useful for observing workers and task execution during failure handling.

| Command | Purpose |
|---|---|
| `celery -A config worker --pool=solo --loglevel=info` | Starts a Celery worker |
| `celery -A config inspect active` | Displays executing tasks |
| `celery -A config inspect reserved` | Displays reserved tasks |
| `celery -A config inspect scheduled` | Displays tasks scheduled for future execution |
| `celery -A config inspect stats` | Displays worker statistics |
| `celery -A config status` | Checks worker status |

## 6. Testing / Expected Results

### Test 1 – Task Failure

- Submit a task that produces a controlled exception.
- Observe the worker logs.
- Verify that the task enters the failure state.
- Check the corresponding application task status.

### Test 2 – Automatic Retry

- Submit a task configured for automatic retry.
- Trigger a retryable exception.
- Verify that Celery schedules another attempt.
- Confirm whether the task eventually succeeds or fails.

### Test 3 – Manual Retry

- Submit a task that uses manual retry behavior.
- Trigger a controlled exception.
- Verify that another attempt is requested.
- Observe the execution result.

### Test 4 – Maximum Retry Attempts

- Submit a task that repeatedly fails.
- Verify that the configured retry limit is respected.
- Confirm that the task reaches its final failure state after retries are exhausted.

### Test 5 – Retry Delay

- Trigger multiple task failures.
- Observe the delay between attempts.
- Verify the configured retry delay and backoff behavior.

### Test 6 – Task Timeout

- Submit a long-running task.
- Verify soft time limit behavior.
- Verify hard time limit behavior separately.

### Test 7 – Worker Failure

- Submit a long-running task.
- Stop the worker unexpectedly.
- Restart the worker.
- Observe whether the task is recovered or redelivered according to the configured acknowledgement behavior.

## 7. Important Notes

- Task failures can occur because of application errors, external service failures, or infrastructure problems.
- Retry should generally be used for temporary failures.
- Permanent errors should not be retried unnecessarily.
- `max_retries` controls the maximum retry attempts.
- Exponential backoff helps avoid overwhelming unavailable services.
- Soft and hard time limits provide different levels of execution control.
- Worker recovery and task retry are separate mechanisms.
- Message redelivery depends on broker and acknowledgement configuration.
- MySQL application task statuses must be synchronized with Celery execution states through application logic.
- Repeated execution can cause duplicate side effects unless tasks are designed to be idempotent.

**Phase 7 Outcome:** Understand how Celery handles task failures, retries, execution timeouts, worker interruptions, and recovery to improve the reliability of background processing.