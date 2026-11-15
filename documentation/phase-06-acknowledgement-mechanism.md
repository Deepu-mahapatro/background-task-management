# Phase 6 – Acknowledgement Mechanism

## 1. Overview

Phase 6 explains how message acknowledgement (ACK) works in Celery and how it affects task delivery and reliability.

It covers how workers acknowledge received messages, the difference between early and late acknowledgement, message requeueing, and redelivery behavior.

The primary objective is to understand how Celery manages message acknowledgement and what happens when a worker fails during task execution.

## 2. Concepts Covered

1. Message Acknowledgement
2. ACK Mechanism
3. Early Acknowledgement
4. Late Acknowledgement
5. `task_acks_late`
6. Message Requeueing
7. Message Redelivery
8. Unacknowledged Messages
9. Worker Failure and Acknowledgement
10. `task_reject_on_worker_lost`
11. `task_acks_on_failure`
12. Message Delivery Lifecycle

## 3. Architecture / Internal Flow

### Early Acknowledgement

In early acknowledgement, the worker acknowledges the message before the task execution is completed.

Flow:

1. Worker receives a message.
2. Worker acknowledges the message.
3. Task execution begins.
4. Worker completes or fails the task.

If the worker crashes after acknowledgement, the broker generally considers the message handled and does not automatically redeliver it.

### Late Acknowledgement

In late acknowledgement, the worker acknowledges the message after task execution completes.

Flow:

1. Worker receives a message.
2. Task execution begins.
3. Task completes successfully.
4. Worker acknowledges the message.
5. Broker considers the message handled.

If the worker fails before acknowledgement, the message may be redelivered according to the broker transport and Celery configuration.

**Architecture flow:**

Redis Broker → Worker Receives Message → Task Execution → Acknowledgement → Message Handled

## 4. Implementation Details

The following components and settings are involved in this phase:

| Component / Setting | Responsibility |
|---|---|
| ACK | Confirms message handling |
| Early ACK | Acknowledges before execution completes |
| Late ACK | Acknowledges after execution completes |
| `task_acks_late` | Enables late acknowledgement for applicable tasks |
| `task_reject_on_worker_lost` | Controls rejection and requeue behavior when a worker process is lost |
| `task_acks_on_failure` | Controls acknowledgement behavior for failed tasks when late ACK is enabled |
| Requeue | Makes a message available for another delivery |
| Redelivery | Delivers a message again after an earlier delivery was not completed successfully |

### Important Configuration Parameters

**`task_acks_late`**

Enables acknowledgement after task execution rather than before execution.

**`task_reject_on_worker_lost`**

Controls whether a message should be rejected and requeued when the worker process executing it is lost.

**`task_acks_on_failure`**

Controls whether messages are acknowledged when tasks fail or time out under late acknowledgement behavior.

### Important Distinction

- Acknowledgement means the broker considers a message handled.
- Requeueing makes a message available for another delivery.
- Redelivery means a worker receives a message again.
- Acknowledgement does not guarantee exactly-once task execution.

A task may execute more than once if a worker fails after performing its business operation but before acknowledging the message.

Therefore, idempotency is important for preventing harmful duplicate side effects.

## 5. Commands

The following commands are useful for observing acknowledgement-related behavior.

| Command | Purpose |
|---|---|
| `celery -A config worker --pool=solo --loglevel=info` | Starts a Celery worker |
| `celery -A config inspect active` | Displays currently executing tasks |
| `celery -A config inspect reserved` | Displays reserved tasks |
| `celery -A config inspect stats` | Displays worker statistics |
| `memurai-cli ping` | Checks broker availability |

## 6. Testing / Expected Results

### Test 1 – Early Acknowledgement

- Run a worker with early acknowledgement behavior.
- Submit a background task.
- Observe message acknowledgement and task execution.
- Understand what happens if the worker crashes after acknowledgement.

### Test 2 – Late Acknowledgement

- Enable late acknowledgement for the applicable task.
- Submit a background task.
- Observe task execution.
- Verify that acknowledgement occurs after execution completes.

### Test 3 – Worker Failure

- Submit a long-running task.
- Stop the worker unexpectedly during execution.
- Observe whether the message is redelivered.
- Verify the task status in MySQL.

### Test 4 – Requeue and Redelivery

- Simulate a worker failure under the configured acknowledgement behavior.
- Observe whether the message becomes available again.
- Verify whether another worker receives the message.

### Test 5 – Failure Acknowledgement

- Execute a task that produces a controlled failure.
- Observe the acknowledgement behavior.
- Verify the resulting task state and whether a retry or redelivery occurs.

## 7. Important Notes

- ACK stands for Acknowledgement.
- Early acknowledgement occurs before task execution completes.
- Late acknowledgement occurs after task execution completes.
- `task_acks_late` controls late acknowledgement.
- Requeueing and redelivery depend on broker transport and Celery configuration.
- Late acknowledgement can improve recovery opportunities but may result in duplicate execution.
- `task_reject_on_worker_lost` affects behavior when a worker process is lost.
- Exactly-once execution is not guaranteed by ACK configuration alone.
- Idempotency is essential when duplicate execution could produce unwanted side effects.

**Phase 6 Outcome:** Understand how Celery manages message acknowledgements, early and late ACK behavior, requeueing, and message redelivery during worker failures.