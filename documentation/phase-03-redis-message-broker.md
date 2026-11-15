# Phase 3 – Redis Message Broker

## 1. Overview

Phase 3 introduces Redis as the message broker in our Background Task Management System.

It explains how Redis receives task messages from the Celery producer, stores them, and makes them available for Celery workers to consume.

The primary objective is to understand the broker's role in asynchronous communication between the Django application and Celery workers.

## 2. Concepts Covered

1. Message Broker
2. Redis Architecture
3. Redis as a Celery Broker
4. Broker Connection Configuration
5. Redis Database Selection
6. Message Storage
7. Message Queue
8. Message Delivery
9. Message Consumption
10. Broker Communication
11. Message Persistence
12. Broker Availability

## 3. Architecture / Internal Flow

The message broker workflow follows this sequence:

1. Django submits a background task through Celery.
2. The Celery producer prepares the task message.
3. The producer connects to Redis using the configured broker URL.
4. Redis receives and stores the message in the appropriate queue.
5. The message remains available until a worker consumes it.
6. A Celery worker connects to Redis.
7. The worker receives the available task message.
8. The worker proceeds with task execution.

**Architecture flow:**

Django API → Celery Producer → Redis Broker → Task Queue → Celery Worker

## 4. Implementation Details

The following components are involved in this phase:

| Component | Responsibility |
|---|---|
| Redis | Acts as the message broker |
| Memurai | Provides Redis-compatible functionality on Windows |
| Broker URL | Defines the Redis connection address |
| Redis Database 0 | Configured as the Celery broker database |
| Redis Database 1 | Configured as the Celery result backend database |
| Message Queue | Holds pending task messages |
| Producer | Publishes task messages |
| Consumer | Receives messages from the broker |
| Worker | Processes received tasks |

### Broker Configuration

Our project uses the following Redis configuration:

- Host: `localhost`
- Port: `6379`
- Broker database: `0`
- Result backend database: `1`

### Redis Database Selection

Redis supports multiple logical databases within one Redis server.

In our project:

- DB 0 is used for Celery broker communication.
- DB 1 is used for Celery result storage.

Using separate logical databases helps organize broker messages and task results. They still share the same Redis server and resources.

### Message Storage and Delivery

Redis temporarily holds task messages so producers and workers do not need to communicate directly.

The producer publishes messages, and workers consume them when available.

The broker therefore acts as an intermediary between task submission and execution.

### Message Persistence

Message persistence concerns whether broker data survives Redis restarts.

It depends on Redis persistence configuration and Celery transport behavior.

Redis supports:

- RDB snapshots.
- AOF (Append Only File).

These mechanisms help persist Redis data, but they do not by themselves guarantee that every Celery task will be recovered correctly after every failure.

## 5. Commands

The following commands are useful for checking Redis/Memurai and observing its availability.

| Command | Purpose |
|---|---|
| `memurai-cli ping` | Checks whether the Redis-compatible server is responding |
| `memurai-cli` | Opens the Memurai command-line interface |
| `SELECT 0` | Selects logical database 0 |
| `SELECT 1` | Selects logical database 1 |
| `DBSIZE` | Displays the number of keys in the selected database |
| `INFO` | Displays Redis server information |
| `INFO persistence` | Displays persistence-related information |
| `MONITOR` | Displays commands received by Redis in real time |

**Note:** `MONITOR` can generate substantial output and overhead. Use it only for short debugging sessions.

## 6. Testing / Expected Results

### Test 1 – Redis Connectivity

- Start Memurai.
- Execute `memurai-cli ping`.
- Verify that the server responds with `PONG`.

### Test 2 – Database Selection

- Select Redis DB 0.
- Verify that the database can be accessed.
- Select Redis DB 1.
- Verify that the database can be accessed.

### Test 3 – Broker Connection

- Start the Django application.
- Submit a background task.
- Verify that Celery can connect to the configured broker.
- Check for connection errors.

### Test 4 – Message Publishing and Consumption

- Start a Celery worker.
- Submit a task through Postman.
- Observe the worker logs.
- Verify that the message reaches the worker through Redis.

### Test 5 – Redis Server Information

- Execute `INFO`.
- Inspect server information.
- Check persistence information using `INFO persistence`.

## 7. Important Notes

- Redis acts as the message broker in our project.
- Memurai provides Redis-compatible functionality on Windows.
- The producer publishes task messages to the broker.
- Workers consume messages from the broker.
- Redis separates task submission from task execution.
- Broker database 0 and result backend database 1 are configured separately.
- Redis broker storage and Celery result storage have different responsibilities.
- Redis persistence and Celery task recovery are related but separate concerns.

**Phase 3 Outcome:** Redis/Memurai is configured as the message broker, enabling communication between Celery producers and workers through task queues.