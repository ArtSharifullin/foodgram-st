# producer.py
import json
import pika
from vault_helper import vault_helper

# Данные для разных API
messages = [
    {
        'alias': 'newsdata',
        'q': 'Python',
    },
    {
        'alias': 'newsapi',
        'q': 'Python',
    }
]

def main():
    vault_credentials = vault_helper.get_rabbitmq_credentials()
    credentials = pika.PlainCredentials(**vault_credentials)
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
    exchange_name = 'api_exchange'
    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct',
        durable=True
    )

    for data in messages:
        json_data = json.dumps(data)
        routing_key = data['alias']
        
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json_data,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        
        print(f" [x] Sent {json_data} to exchange '{exchange_name}' with routing_key '{routing_key}'")
    
    connection.close()
    print(" [✓] All messages sent successfully!")


if __name__ == "__main__":
    main()
