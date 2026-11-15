# Phase 2 – Celery Producer and Message Publishing

## 1. Overview

Phase 2 introduces the Celery producer mechanism responsible for submitting background tasks.

It establishes the connection between the Django application and Celery, defines and registers Celery tasks, prepares task messages, and publishes those messages to the configured broker.

The primary objective is to understand how a task request moves from the Django application to the message broker without executing the task inside the API request.

## 2. Concepts Covered

1. Celery Application Initialization
2. Celery Configuration
3. Task Definition
4. Task Registration
5. Task Discovery
6. Producer Architecture
7. Message Creation
8. Task Message Structure
9. Serialization and Deserialization
10. Task Submission Using `delay()` and `apply_async()`
11. Task ID Generation
12. Message Publishing

## 3. Architecture / Internal Flow

The producer workflow follows this sequence:

1. Client submits a task creation request.
2. Django processes and validates the request.
3. The task creation service prepares the background task.
4. The Celery application identifies the registered task.
5. The producer prepares a task message.
6. The message receives a task ID and execution metadata.
7. The task arguments are serialized.
8. The producer publishes the message to the configured broker.
9. The broker stores the message until a worker consumes it.

**Architecture flow:**

Django API → Task Creation Service → Celery Application → Celery Producer → Message Creation → Serialization → Redis Broker

## 4. Implementation Details

The following components are involved in this phase:

| Component | Responsibility |
|---|---|
| Celery Application | Initializes the Celery application |
| Celery Configuration | Defines broker and task-related settings |
| Celery Task | Defines background execution functions |
| Task Registration | Makes tasks available to Celery |
| Task Discovery | Finds task modules automatically |
| Producer | Submits tasks to the broker |
| Task Message | Represents the task request sent to the broker |
| Serializer | Converts task data into a transportable format |
| Task ID | Identifies the submitted task |
| Redis Broker | Stores published task messages |

### Task Submission Methods

**`delay()`**

A shortcut for submitting a task with positional arguments.

**`apply_async()`**

Provides more control over task submission, including:

- Task arguments and keyword arguments.
- Task ID.
- Target queue.
- Execution countdown.
- ETA scheduling.
- Other execution options.

### Task Message

A Celery task message contains information required to identify and execute a task, such as:

- Task name.
- Task ID.
- Task arguments.
- Task keyword arguments.
- Execution metadata.
- Headers and delivery information.

The exact message structure depends on the Celery version, protocol, and transport configuration.

### Serialization and Deserialization

- **Serialization:** Converts task arguments into a format suitable for message transport.
- **Deserialization:** Converts the received message data back into usable Python values.

JSON is a commonly used serialization format.

### Important Distinction

The producer does not execute the background task itself.

Its responsibility is to prepare and publish the task message. Actual execution is handled by Celery workers in subsequent stages.

## 5. Commands

The following commands are relevant when running and observing the producer workflow in our Windows development environment.

| Command | Purpose |
|---|---|
| `python manage.py check` | Checks Django configuration |
| `python manage.py runserver` | Starts the Django API server |
| `celery -A config worker --pool=solo --loglevel=info` | Starts a worker to receive and execute published tasks |

**Note:** The worker command is included to verify message delivery and execution. Worker architecture and execution are covered separately in later phases.

## 6. Testing / Expected Results

### Test 1 – Celery Application Initialization

- Start the Django application.
- Verify that the Celery application initializes correctly.
- Check for configuration or import errors.

### Test 2 – Task Registration

- Verify that the defined Celery tasks are available to the Celery application.
- Check that task modules are discovered correctly.

### Test 3 – Task Submission

- Submit a valid background task through the API.
- Verify that the producer submits the task.
- Confirm that a task ID is generated.
- Verify that the API does not wait for the background operation to finish.

### Test 4 – Message Publishing

- Start the Celery worker.
- Submit a task through Postman.
- Observe the worker logs.
- Verify that the submitted task reaches the worker.

### Test 5 – Submission Methods

- Verify task submission using `delay()`.
- Verify task submission using `apply_async()`.
- Compare their available configuration options.

## 7. Important Notes

- The Celery application acts as the central configuration and task-management entry point.
- Task registration makes task functions available to Celery.
- Task discovery helps load task modules.
- The producer is responsible for preparing and publishing task messages.
- Serialization makes task arguments suitable for message transport.
- Every submitted task has an identifier used for tracking.
- Redis acts as the message broker in our project.
- Publishing a message and executing a task are two separate operations.

**Phase 2 Outcome:** The Django application can submit background tasks through Celery, prepare task messages, and publish them to the configured message broker.