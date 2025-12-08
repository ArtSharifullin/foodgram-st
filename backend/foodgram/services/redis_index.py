from redis.commands.search.field import TextField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
import sys

sys.path.insert(0, '/app')

from services.redis_client import get_redis_client

def create_redis_index():
    try:
        redis = get_redis_client()
        redis.ft("idx_docs").create_index(
            fields=[
                TextField("quote"),
                TextField("author"),
                TextField("fact"),
                TagField("source"),
            ],
            definition=IndexDefinition(prefix=["breakingbad:", "catfact:"], index_type=IndexType.HASH)
        )
    except Exception as e:
        print("Index may already exist:", e)