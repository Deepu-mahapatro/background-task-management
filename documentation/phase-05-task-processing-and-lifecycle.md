# Phase 5 – Task Processing and Lifecycle

## 1. Overview

Phase 5 explains how Celery processes task messages received from the Redis broker and executes the corresponding background operations.

It covers task execution, task lifecycle, task states, execution flow, and the relationship between Celery task states and application-level task status stored in MySQL.

The primary objective is to understand how a task moves from submission to successful completion or failure.

## 2. Concepts Covered

1. Task Processing
2. Task Execution
3. Task Execution Flow
4. Task Lifecycle
5. Task States
6. PENDING State
7. RECEIVED State
8. STARTED State
9. SUCCESS State
10. FAILURE State
11. RETRY State
12. REVOKED State
13. Task Result
14. Task Result Storage
15. Task State Transitions

## 3. Architecture / Internal Flow

The task processing workflow follows this sequence:

1. Celery worker receives a task message from Redis.
2. The worker identifies the registered task.
3. The task arguments are prepared for execution.
4. The worker executes the corresponding task function.
5. The task performs its background operation.
6. Celery tracks the task execution state.
7. The task completes successfully or encounters an error.
8. The result backend stores the task result and state when configured.
9. The application updates its task status in MySQL.
10. The client retrieves the latest task information through the status API.

**Architecture flow:**

Redis Broker → Celery Worker → Task Identification → Task Execution → Result Backend → MySQL Task Status → Status API

## 4. Implementation Details

The following components are involved in this phase:

| Component | Responsibility |
|---|---|
| Celery Worker | Executes background tasks |
| Registered Task | Defines the background operation |
| Task Execution | Runs the task function |
| Task Lifecycle | Represents the complete task processing journey |
| Task State | Indicates the current execution condition |
| Result Backend | Stores Celery task results and states |
| MySQL | Stores application-level task information and status |
| Status API | Returns task information to clients |

### Task States

| State | Meaning |
|---|---|
| PENDING | Task is waiting for execution or its state is not yet known to the result backend |
| RECEIVED | Worker has received the task message |
| STARTED | Task execution has started |
| SUCCESS | Task completed successfully |
| FAILURE | Task execution failed |
| RETRY | Task execution is scheduled for another attempt |
| REVOKED | Task execution has been revoked |

**Note:** `RECEIVED` and `RETRY` are Celery task events/states with configuration and lifecycle nuances. Not every state is necessarily persisted or observable in every setup.

### Task Lifecycle

A typical successful lifecycle:

PENDING → RECEIVED → STARTED → SUCCESS

A failure and retry lifecycle may look like:

PENDING → RECEIVED → STARTED → RETRY → RECEIVED → STARTED → SUCCESS

A permanently failed task may follow:

PENDING → RECEIVED → STARTED → FAILURE

A revoked task may enter the REVOKED state.

### Task Result

A task result represents the outcome of task execution.

Depending on the task and result backend configuration, it may contain:

- Returned value.
- Execution state.
- Error information.
- Task identification information.

### Result Backend

The result backend stores task execution results and states separately from the message broker.

In our project, Redis DB 1 is configured as the Celery result backend, while MySQL stores application-level task records.

These two storage responsibilities should not be confused.

## 5. Commands

The following commands are useful for observing and managing task execution.

| Command | Purpose |
|---|---|
| `celery -A config worker --pool=solo --loglevel=info` | Starts a Celery worker |
| `celery -A config inspect active` | Displays currently executing tasks |
| `celery -A config inspect reserved` | Displays tasks reserved by workers |
| `celery -A config inspect scheduled` | Displays tasks scheduled for future execution |
| `celery -A config inspect stats` | Displays worker statistics |
| `celery -A config inspect registered` | Displays registered tasks |

## 6. Testing / Expected Results

### Test 1 – Successful Task Execution

- Submit a valid task through Postman.
- Verify that the worker receives it.
- Observe the task execution logs.
- Verify that the task reaches SUCCESS.
- Check the stored result and MySQL task status.

### Test 2 – Task State Verification

- Submit a background task.
- Observe its lifecycle through worker logs and the status API.
- Verify the state transitions that are actually exposed by our configuration.

### Test 3 – Failed Task Execution

- Submit a task that produces a controlled execution error.
- Verify that the worker reports the failure.
- Check the Celery result state and application-level status.

### Test 4 – Task Result Retrieval

- Submit a task that returns a result.
- Retrieve the result using the configured result backend.
- Verify that the returned information matches the execution outcome.

### Test 5 – Worker Inspection

- Inspect active tasks.
- Inspect reserved tasks.
- Inspect scheduled tasks.
- Verify that the worker reports the expected task information.

## 7. Important Notes

- Task processing happens inside Celery workers.
- The task lifecycle describes the journey from submission to completion.
- Celery task states indicate execution conditions.
- The result backend stores execution results and states.
- MySQL stores application-level task information.
- The broker and result backend have different responsibilities.
- A Celery task state and a custom MySQL task status are not automatically synchronized; application logic must manage that synchronization.
- Result storage depends on the configured result backend and task settings.

**Phase 5 Outcome:** Understand how Celery workers execute background tasks, manage task lifecycle states, and store execution results through the configured result backend.