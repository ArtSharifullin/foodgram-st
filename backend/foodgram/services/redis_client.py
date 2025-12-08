import redis
import sys
import logging

sys.path.insert(0, '/app')

from services.vault_helper import vault_helper


logger = logging.getLogger(__name__)


def get_vault_data():
    vault_credentials = vault_helper.get_redis_credentials()
    return vault_credentials


creds = get_vault_data()
logger.info(creds)


def get_redis_client():
    redis_client = redis.Redis(
        host=creds['host'],
        port=creds['port'],
        decode_responses=True
    )

    return redis_client