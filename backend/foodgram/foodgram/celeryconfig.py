import os

rabbitmq_user = os.getenv('RABBITMQ_USER', 'testuser')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'testpass')
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.getenv('RABBITMQ_PORT', '5672')

broker_url = f'amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}//'
result_backend = 'rpc://'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Moscow'
enable_utc = True
task_acks_late = True
worker_concurrency = 2