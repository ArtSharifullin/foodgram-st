import pika

def message_callback(ch, method, properties, body):
    print(f" [x] Received {body}")

def main():
    credentials = pika.PlainCredentials(
        username='testuser',
        password='testpass'
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_consume(
        queue='hello',
        on_message_callback=message_callback,
        auto_ack=True
    )
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
