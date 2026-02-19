import os
import json
import pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
EMAIL_EXCHANGE = os.getenv("EMAIL_EXCHANGE", "email.exchange")
ROUTING_KEY = os.getenv("ROUTING_KEY", "email.send")


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str


@app.post("/api/notifications/email", status_code=202)
def send_email_notification(email: EmailRequest):
    try:
        # Create connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()

        # Declare exchange (safe to declare repeatedly)
        channel.exchange_declare(
            exchange=EMAIL_EXCHANGE,
            exchange_type="direct",
            durable=True
        )

        # Publish message to exchange (NOT directly to queue)
        channel.basic_publish(
            exchange=EMAIL_EXCHANGE,
            routing_key=ROUTING_KEY,
            body=json.dumps(email.dict()),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )

        connection.close()

        return {"message": "Email queued successfully"}

    except pika.exceptions.AMQPConnectionError:
        raise HTTPException(status_code=500, detail="Cannot connect to RabbitMQ")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
