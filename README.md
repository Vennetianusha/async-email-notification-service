# 🚀 Asynchronous Email Notification Service with RabbitMQ

## 📌 Project Overview

This project implements a **fully containerized asynchronous email notification microservice** using **FastAPI** and **RabbitMQ**.

The system demonstrates:

- Event-driven architecture
- Producer–Consumer pattern
- Retry mechanism
- Dead Letter Queue (DLQ)
- Dockerized microservices
- Environment-based configuration

The email sending process is simulated and processed asynchronously to ensure that the API remains fast and responsive.

---

## 🏗 Architecture Overview

```
Client
   ↓
FastAPI Producer (API)
   ↓
RabbitMQ Exchange (email.exchange)
   ↓
Primary Queue (email_queue)
   ↓
Consumer Service
   ↓
Dead Letter Exchange (dlx.email)
   ↓
Dead Letter Queue (dlq.email)
```

---

## ⚙️ Tech Stack

- Python 3.11
- FastAPI
- RabbitMQ
- Docker & Docker Compose
- Pytest

---

## 📂 Project Structure

```
my-notification-service/
│
├── producer-api/
│   ├── src/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── consumer-service/
│   ├── src/
│   │   └── consumer.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── tests/
│   ├── test_producer.py
│   ├── test_consumer.py
│   └── test_integration.py
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Vennetianusha/async-email-notification-service.git
cd async-email-notification-service
```

---

### 2️⃣ Start All Services

```bash
docker compose up --build
```

This will start:

- RabbitMQ
- Producer API
- Consumer Service

---

## 🌐 Access URLs

### 📬 API Documentation (Swagger UI)

```
http://localhost:8000/docs
```

---

### 🐰 RabbitMQ Management UI

```
http://localhost:15672
```

Login Credentials:

```
Username: guest
Password: guest
```

---

## 📮 API Endpoint

### POST `/api/notifications/email`

### Request Body

```json
{
  "to": "test@example.com",
  "subject": "Hello",
  "body": "This is a test email."
}
```

### Success Response

**Status:** `202 Accepted`

```json
{
  "message": "Email queued successfully"
}
```

---

## 🔄 Retry & Dead Letter Strategy

### ✔ Retry Mechanism

- If email sending fails (simulated random failure),
- Message is retried up to `MAX_RETRIES`
- Retry count tracked using message headers (`x-retry-count`)

### ✔ Dead Letter Queue (DLQ)

- If retries exceed limit,
- Message is rejected without requeue
- RabbitMQ routes message to `dlq.email`

This ensures:

- No message loss
- Fault tolerance
- Safe inspection of failed messages

---

## 🧪 Running Tests

```bash
pytest
```

Tests cover:

- Producer validation
- Consumer logic
- Basic integration test

---

## 🔐 Environment Configuration

All configurations are managed via environment variables.

See `.env.example`:

```
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672

EMAIL_EXCHANGE=email.exchange
ROUTING_KEY=email.send
EMAIL_QUEUE_NAME=email_queue

DEAD_LETTER_EXCHANGE=dlx.email
DEAD_LETTER_QUEUE=dlq.email

MAX_RETRIES=3
```

---

## 🧠 Key Concepts Demonstrated

- Asynchronous Processing
- Publish–Subscribe Messaging Pattern
- Exchange-Based Routing
- Message Acknowledgment
- Retry Handling
- Dead Letter Queues
- Dockerized Microservices
- Health Checks
- Environment-Based Configuration

---

## 🏆 Resume Summary

Designed and implemented a fully containerized asynchronous email notification microservice using FastAPI and RabbitMQ. Implemented retry logic, exchange-based routing, and Dead Letter Queue handling to ensure fault tolerance in a distributed system.

---

## 🚀 Future Improvements

- Exponential backoff retry strategy
- Delayed queues using TTL
- Monitoring with Prometheus
- Cloud deployment (AWS / Render / Railway)
- Kubernetes orchestration

---

## 📄 License

This project is for educational and demonstration purposes.
