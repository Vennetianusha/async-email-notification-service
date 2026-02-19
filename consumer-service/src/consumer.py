import os
import json
import pika
import random
import time
import sys

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))

EMAIL_EXCHANGE = os.getenv("EMAIL_EXCHANGE", "email.exchange")
ROUTING_KEY = os.getenv("ROUTING_KEY", "email.send")
EMAIL_QUEUE_NAME = os.getenv("EMAIL_QUEUE_NAME", "email_queue")

DEAD_LETTER_EXCHANGE = os.getenv("DEAD_LETTER_EXCHANGE", "dlx.email")
DEAD_LETTER_QUEUE = os.getenv("DEAD_LETTER_QUEUE", "dlq.email")

MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))


def callback(ch, method, properties, body):
    message = json.loads(body)
    headers = properties.headers or {}
    retry_count = headers.get("x-retry-count", 0)

    try:
        print(f"\n📧 Sending email to {message['to']}", flush=True)

        # Simulate 20% failure
        if random.random() < 0.2:
            raise Exception("Simulated email failure")

        print("✅ Email sent successfully", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"❌ Error: {e}", flush=True)

        if retry_count < MAX_RETRIES:
            headers["x-retry-count"] = retry_count + 1

            print(f"🔁 Retrying attempt {retry_count + 1}", flush=True)

            ch.basic_publish(
                exchange=EMAIL_EXCHANGE,
                routing_key=ROUTING_KEY,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    headers=headers,
                    delivery_mode=2
                )
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            print("☠️ Max retries exceeded → Sending to DLQ", flush=True)

            ch.basic_reject(
                delivery_tag=method.delivery_tag,
                requeue=False
            )


def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )

    channel = connection.channel()

    # Declare main exchange
    channel.exchange_declare(
        exchange=EMAIL_EXCHANGE,
        exchange_type="direct",
        durable=True
    )

    # Declare dead letter exchange
    channel.exchange_declare(
        exchange=DEAD_LETTER_EXCHANGE,
        exchange_type="direct",
        durable=True
    )

    # Declare main queue with DLX configuration
    channel.queue_declare(
        queue=EMAIL_QUEUE_NAME,
        durable=True,
        arguments={
            "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE,
            "x-dead-letter-routing-key": ROUTING_KEY
        }
    )

    # Bind main queue to exchange
    channel.queue_bind(
        exchange=EMAIL_EXCHANGE,
        queue=EMAIL_QUEUE_NAME,
        routing_key=ROUTING_KEY
    )

    # Declare DLQ
    channel.queue_declare(queue=DEAD_LETTER_QUEUE, durable=True)

    # Bind DLQ
    channel.queue_bind(
        exchange=DEAD_LETTER_EXCHANGE,
        queue=DEAD_LETTER_QUEUE,
        routing_key=ROUTING_KEY
    )

    print("🚀 Consumer is waiting for messages...", flush=True)

    channel.basic_consume(
        queue=EMAIL_QUEUE_NAME,
        on_message_callback=callback
    )

    channel.start_consuming()


if __name__ == "__main__":
    while True:
        try:
            start_consumer()
        except Exception as e:
            print(f"Connection error: {e}", flush=True)
            print("Retrying in 5 seconds...", flush=True)
            time.sleep(5)
