from django.apps import AppConfig

class ServicesConfig(AppConfig):
    name = "services"

    def ready(self):
        from services.redis_index import create_redis_index
        create_redis_index()