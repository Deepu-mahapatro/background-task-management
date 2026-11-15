# 🚀 Background Task Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-Backend-red?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/Celery-5.7-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/Redis-Broker-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Postman-API_Testing-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman">
</p>

<p align="center">
  <b>A Django REST Framework-based background task management system designed to understand and implement asynchronous task processing using Celery, Redis, and MySQL, covering task creation, message publishing, worker execution, task lifecycle, acknowledgement, and failure handling.</b>
</p>

---

## 📌 About the Project

Background Task Management System is a backend learning and implementation project developed to understand how asynchronous background processing works in real-world applications.

The system uses Django REST Framework to manage task requests, Celery to handle background execution, Redis as the message broker, and MySQL for persistent task information.

Instead of executing time-consuming operations directly during API requests, the application submits tasks to Celery for background processing.

The project covers **10 learning and implementation phases**, organized into two categories:

- **7 Practical Implementation Phases:** Building and understanding the background task processing system using Django REST Framework, Celery, Redis, and MySQL.
- **3 Conceptual Phases:** Studying advanced reliability, multiple queues and workers, testing, and production readiness concepts.

The primary objective is to understand the complete background processing architecture, from task submission to execution, result handling, and failure management.

## 🎯 Project Objectives

- Understand synchronous and asynchronous execution.
- Learn Celery architecture and its components.
- Implement task creation and management using Django REST Framework.
- Understand the producer and consumer architecture.
- Configure Redis as a Celery message broker.
- Understand task message creation, serialization, and publishing.
- Implement background task execution using Celery workers.
- Understand task lifecycle and execution states.
- Explore message acknowledgement and redelivery mechanisms.
- Implement failure handling and task retry mechanisms.
- Understand idempotency and duplicate execution prevention.
- Study multiple queues, task routing, and worker management.
- Explore testing, monitoring, security, and production readiness.
- Maintain structured technical documentation for all 10 phases.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Backend programming |
| Django 5.2 | Backend framework |
| Django REST Framework | REST API development |
| Celery 5.7 | Asynchronous task processing |
| Redis | Celery message broker and result backend |
| Memurai | Redis-compatible server for Windows development |
| MySQL 8.0 | Persistent database |
| Postman | API testing |
| Git and GitHub | Version control and project hosting |
| VS Code | Development environment |

---

## ⚡ Core System Components

The project focuses on the following major components:

| Component | Responsibility |
|---|---|
| Django REST Framework | Receives and manages task requests |
| Task Model | Stores task information and metadata |
| Task Serializer | Validates incoming task data |
| Task Creation Service | Handles task creation logic |
| Celery Application | Initializes Celery and its configuration |
| Celery Producer | Submits background task messages |
| Redis Broker | Stores messages waiting for execution |
| Celery Worker | Consumes messages and executes tasks |
| Result Backend | Stores Celery task execution results |
| MySQL | Maintains persistent application task records |
| Task Status API | Provides task information and status |

---

## 🏗️ System Architecture

The system follows a producer-broker-consumer architecture.

### Architecture Flow

```text
              CLIENT / POSTMAN
                     |
                     v
             DJANGO REST FRAMEWORK
                     |
                     v
              REQUEST VALIDATION
                     |
                     v
             TASK CREATION SERVICE
                     |
                     v
                  MYSQL
             (Task Information)
                     |
                     v
              CELERY PRODUCER
                     |
                     v
              MESSAGE CREATION
                     |
                     v
               REDIS BROKER
              (Task Queues)
                     |
                     v
               CELERY WORKER
                     |
                     v
               TASK EXECUTION
                     |
              +------+------+
              |             |
              v             v
         SUCCESS         FAILURE
              |             |
              v             v
        RESULT BACKEND   RETRY / FAILURE
              |             |
              +------+------+
                     |
                     v
              TASK STATUS UPDATE
                     |
                     v
                MYSQL
                     |
                     v
               STATUS API
                     |
                     v
                  CLIENT
```

### Component Responsibilities

**Django REST Framework**
- Receives task creation requests.
- Validates task information.
- Stores task records.
- Provides task retrieval and status APIs.

**Celery Producer**
- Identifies registered tasks.
- Prepares task messages.
- Assigns task identifiers.
- Publishes messages to Redis.

**Redis Broker**
- Receives task messages from producers.
- Stores messages in queues.
- Makes messages available to workers.

**Celery Worker**
- Connects to the broker.
- Consumes available task messages.
- Identifies registered tasks.
- Executes background operations.

**Result Backend**
- Stores task execution results and states when configured.
- Allows task results to be retrieved.

**MySQL**
- Stores application-level task records.
- Maintains task metadata and application-level status.

---

## 🔄 Background Task Execution Workflow

The complete background task processing workflow follows these steps:

1. **Task Submission:** Client submits a task request through the API.
2. **Validation:** Django REST Framework validates the request.
3. **Task Creation:** The task creation service creates a task record.
4. **Database Storage:** Task information is stored in MySQL.
5. **Task Publishing:** Celery producer prepares and publishes the task message.
6. **Message Storage:** Redis receives and stores the task message.
7. **Message Consumption:** Celery worker receives the message.
8. **Task Execution:** Worker executes the corresponding background operation.
9. **State Management:** Celery tracks task execution states.
10. **Result Storage:** Result backend stores execution results when configured.
11. **Status Retrieval:** Client retrieves task information through the status API.

---

## ⚙️ Key Features and Concepts

The project explores the following background processing capabilities:

| Feature | Description |
|---|---|
| Task Management | Create and manage background task records |
| Task Identification | Assign unique identifiers to tasks |
| Payload Validation | Validate task-specific input data |
| Asynchronous Processing | Execute time-consuming operations outside API requests |
| Message Publishing | Publish task messages through Celery |
| Message Broker | Use Redis for message communication |
| Worker Execution | Process background tasks independently |
| Task Lifecycle | Understand task execution states |
| Result Management | Store and retrieve task execution results |
| Acknowledgement | Understand early and late message acknowledgement |
| Retry Mechanism | Handle unsuccessful task execution |
| Failure Handling | Understand task and worker failure scenarios |
| Idempotency | Study duplicate execution protection |
| Queue Management | Understand multiple queues and task routing |
| Worker Management | Study multiple workers and concurrency |

---

## 📊 Task Lifecycle

A background task moves through different execution states.

| Task State | Description |
|---|---|
| PENDING | Task is waiting for execution or its state is not yet known to the result backend |
| RECEIVED | Worker has received the task message |
| STARTED | Task execution has started |
| SUCCESS | Task completed successfully |
| FAILURE | Task execution failed |
| RETRY | Another execution attempt is scheduled |
| REVOKED | Task execution has been revoked |

**Typical successful execution flow:**

```text
PENDING
   |
   v
RECEIVED
   |
   v
STARTED
   |
   v
SUCCESS
```

A task may follow a different lifecycle when execution fails or retry is requested.

---

## 🧪 Practical Implementation and Testing

The practical implementation covers the foundational background processing workflow developed during Phases 1–7.

### Task Management

- Create background task records.
- Validate task types and payloads.
- Generate unique task identifiers.
- Store task information in MySQL.
- Retrieve task details and status.

### Celery Producer and Message Publishing

- Initialize the Celery application.
- Configure Celery.
- Define and register tasks.
- Understand task discovery.
- Submit tasks using `delay()` and `apply_async()`.
- Publish messages to Redis.

### Redis Message Broker

- Configure Redis/Memurai.
- Establish broker connectivity.
- Understand message storage.
- Observe message publishing and consumption.

### Worker Execution

- Start Celery workers.
- Verify task registration.
- Observe message delivery.
- Execute registered background tasks.

### Task Processing and Lifecycle

- Execute background operations.
- Observe task execution states.
- Retrieve task results.
- Maintain application-level task status.

### Acknowledgement Mechanism

- Understand early acknowledgement.
- Understand late acknowledgement.
- Study message requeueing and redelivery behavior.

### Failure Handling and Recovery

- Handle task execution failures.
- Configure retry behavior.
- Understand retry delays and limits.
- Explore execution time limits.
- Study worker and broker failure scenarios.

### API Testing

Postman is used to submit task requests and verify API responses, task information, and status retrieval for the implemented functionality.

---

## 📚 Learning Roadmap and Documentation

The project is organized into 10 phases, each covering a specific part of the background task processing architecture.

### Practical Implementation Phases

These phases cover the practical foundation and implementation work.

| No. | Phase | Key Concepts Covered | Status |
|---:|---|---|---|
| 1 | Task Creation and Management | Task Models, Task Types, Payload Validation, Task Creation API, Metadata, Status API | Completed |
| 2 | Celery Producer and Message Publishing | Celery App, Task Registration, Discovery, Producer, Serialization, `delay()`, `apply_async()` | Completed |
| 3 | Redis Message Broker | Redis Architecture, Broker Configuration, Message Storage, Queues, Persistence | Completed |
| 4 | Celery Worker and Message Delivery | Worker Initialization, Consumer, Message Delivery, Task Registration | Completed |
| 5 | Task Processing and Lifecycle | Task Execution, Lifecycle, Task States, Result Backend | Completed |
| 6 | Acknowledgement Mechanism | ACK, Early ACK, Late ACK, Requeueing, Redelivery | Completed |
| 7 | Failure Handling and Recovery | Exceptions, Retries, Backoff, Time Limits, Failure Handling | Completed |

### Conceptual Study Phases

These phases cover advanced concepts studied theoretically. Practical implementation and testing remain pending.

| No. | Phase | Key Concepts Covered | Status |
|---:|---|---|---|
| 8 | Reliability and Data Consistency | Duplicate Execution, Idempotency, Idempotency Keys, Task Deduplication, Recovery | Theory Completed |
| 9 | Multiple Queues and Workers | Queue Architecture, Task Routing, Multiple Workers, Concurrency, Monitoring | Theory Completed |
| 10 | Testing and Production Readiness | Testing Approaches, Failure Simulation, Load Testing, Security, Deployment Preparation | Theory Completed |

### Detailed Phase Documentation

Each phase has a dedicated Markdown document explaining its overview, concepts, architecture, relevant implementation details, commands, testing scenarios, and important notes.

See the [Documentation Index](documentation/README.md) for all 10 phase documents.

---

## 📁 Project Structure

```text
background-task-management/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   ├── wsgi.py
│   └── asgi.py
│
├── task_management/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services.py
│   └── tasks.py
│
├── documentation/
│   ├── README.md
│   ├── phase-01-task-creation-and-management.md
│   ├── phase-02-celery-producer-and-message-publishing.md
│   ├── phase-03-redis-message-broker.md
│   ├── phase-04-celery-worker-and-message-delivery.md
│   ├── phase-05-task-processing-and-lifecycle.md
│   ├── phase-06-acknowledgement-mechanism.md
│   ├── phase-07-failure-handling-and-recovery.md
│   ├── phase-08-reliability-and-data-consistency.md
│   ├── phase-09-multiple-queues-and-workers.md
│   └── phase-10-testing-and-production-readiness.md
│
├── .env.example
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Setup and Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd background-task-management
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference.

Configure the required values for:

- Django secret key.
- MySQL database credentials.
- Redis broker URL.
- Celery result backend URL.
- Application settings.

**Important:** Never commit `.env` or expose secret credentials on GitHub.

### 5. Configure MySQL

- Start MySQL Server.
- Create the project database.
- Configure database credentials.
- Apply Django migrations.

```bash
python manage.py migrate
```

### 6. Start Memurai

Start the Redis-compatible Memurai server.

Verify connectivity:

```powershell
memurai-cli ping
```

Expected output:

```text
PONG
```

### 7. Start Django Application

```bash
python manage.py runserver
```

### 8. Start Celery Worker

Open a separate terminal, activate the virtual environment, and execute:

```powershell
celery -A config worker --pool=solo --loglevel=info
```

**Note:** The `solo` pool is used in our Windows development environment.

---

## 🔍 Useful Development Commands

| Command | Purpose |
|---|---|
| `python manage.py check` | Checks Django configuration |
| `python manage.py makemigrations` | Creates migration files |
| `python manage.py migrate` | Applies database migrations |
| `python manage.py showmigrations` | Displays migration status |
| `python manage.py runserver` | Starts Django development server |
| `memurai-cli ping` | Checks Memurai connectivity |
| `celery -A config worker --pool=solo --loglevel=info` | Starts Celery worker |
| `celery -A config inspect ping` | Checks worker availability |
| `celery -A config inspect active` | Displays executing tasks |
| `celery -A config inspect registered` | Displays registered tasks |

---

## 🧠 Learning Outcomes

Through this project, the following concepts are explored:

- Synchronous vs asynchronous execution.
- Background task processing architecture.
- Celery application and task configuration.
- Producer and consumer architecture.
- Message brokers and task queues.
- Task message creation and serialization.
- Redis-based message communication.
- Celery worker initialization and execution.
- Task lifecycle and result management.
- Message acknowledgement and redelivery.
- Retry mechanisms and failure handling.
- Idempotency and duplicate execution prevention.
- Multiple queue and worker architecture.
- Monitoring and performance concepts.
- Testing and production readiness fundamentals.

---

## 🚧 Project Scope and Limitations

This project focuses on learning and understanding the complete background task processing architecture through practical implementation and conceptual study.

**Practical implementation:**
- Foundational background task management.
- Celery producer and message publishing.
- Redis broker integration.
- Celery worker execution.
- Task lifecycle and result handling.
- Acknowledgement concepts and failure handling.

**Conceptual studies:**
- Reliability and data consistency.
- Duplicate execution and idempotency.
- Multiple queues and workers.
- Testing and production readiness.

**Current limitations:**
- Phases 8–10 have not undergone practical implementation or testing.
- Multiple queue and worker configuration is not yet implemented.
- Production deployment and load testing have not been completed.
- Advanced reliability mechanisms remain subjects for future implementation.

These boundaries distinguish the concepts studied from the functionality actually implemented.

---

## 🔮 Future Improvements

- Implement advanced idempotency and duplicate execution protection.
- Explore task expiration and revocation.
- Implement multiple queues and dedicated workers.
- Add advanced task monitoring.
- Introduce automated testing.
- Perform load and performance testing.
- Improve worker failure recovery.
- Prepare production deployment configuration.

---

## 🧠 Key Takeaway

> Background Task Management System provides a structured exploration of asynchronous processing using Django REST Framework, Celery, Redis, and MySQL, covering the complete journey of task creation, message publishing, worker execution, task lifecycle, and failure handling, along with advanced reliability and production architecture concepts.

