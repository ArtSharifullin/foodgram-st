# consumer.py
import pika
import json
import requests
import sys
from vault_helper import vault_helper


def message_callback(ch, method, properties, body):
    """Обработка сообщения из очереди"""
    print(f" [x] Received {body}")
    
    try:
        json_data = json.loads(body)
        alias = json_data.pop('alias')
        params = json_data
        
        api_key = vault_helper.get_api_key(alias)
        
        if alias == 'newsdata':
            api_url = 'https://newsdata.io/api/1/news'
            params['apikey'] = api_key
        elif alias == 'newsapi':
            api_url = 'https://newsapi.org/v2/everything'
            params['apiKey'] = api_key
        else:
            print(f"Unknown API alias: {alias}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        print(f" [*] Calling API: {alias}")
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        result_data = response.json()
        filename = f"{alias}_result.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f" [✓] Saved result to {filename}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f" [!] Error: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    if len(sys.argv) < 2:
        print("Usage: python consumer.py <queue_name>")
        print("Example: python consumer.py newsdata")
        sys.exit(1)
    
    queue_name = sys.argv[1]
    
    vault_credentials = vault_helper.get_rabbitmq_credentials()
    
    print(f"[DEBUG] RabbitMQ credentials from Vault:")
    print(f"  Username: {vault_credentials.get('username')}")
    print(f"  Password: {vault_credentials.get('password')}")
    
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

    channel.queue_declare(queue=queue_name, durable=True)

    
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=queue_name
    )

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=message_callback,
        auto_ack=False
    )
    
    print(f" [*] Waiting for messages in queue '{queue_name}'. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
