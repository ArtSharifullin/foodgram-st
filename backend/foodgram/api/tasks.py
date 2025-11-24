import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import requests
from celery import shared_task
from django.conf import settings

from foodgram.integrations.vault import VaultClientError, vault_client

EXTERNAL_API_CONFIG = {
    'newsdata': {
        'url': 'https://newsdata.io/api/1/news',
        'key_param': 'apikey',
        'env_var': 'NEWSDATA_API_KEY',
    },
    'newsapi': {
        'url': 'https://newsapi.org/v2/everything',
        'key_param': 'apiKey',
        'env_var': 'NEWSAPI_API_KEY',
    },
}

DEFAULT_API_MESSAGES: List[Dict[str, object]] = [
    {'alias': 'newsdata', 'params': {'q': 'Python'}},
    {'alias': 'newsapi', 'params': {'q': 'Python'}},
]

API_SECRET_PATH = os.getenv('VAULT_EXTERNAL_API_PATH', 'apikeys')


def _resolve_api_key(alias: str) -> Optional[str]:
    config = EXTERNAL_API_CONFIG.get(alias)
    if not config:
        return None
    env_value = os.getenv(config['env_var'])
    if env_value:
        return env_value
    try:
        return vault_client.get_secret_value(API_SECRET_PATH, alias)
    except VaultClientError:
        return None


def _persist_result(alias: str, payload: Dict) -> str:
    media_root = Path(getattr(settings, 'MEDIA_ROOT', '/tmp'))
    target_dir = media_root / 'external_api_results'
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f'{alias}_result.json'
    with target_file.open('w', encoding='utf-8') as handler:
        json.dump(payload, handler, indent=2, ensure_ascii=False)
    return str(target_file)


def _normalize_messages(messages: Optional[Iterable[Dict]]) -> List[Dict]:
    if not messages:
        return DEFAULT_API_MESSAGES
    normalized = []
    for item in messages:
        alias = item.get('alias')
        params = item.get('params', {})
        normalized.append({'alias': alias, 'params': params})
    return normalized


@shared_task(bind=True, autoretry_for=(requests.RequestException,), retry_backoff=True, max_retries=3)
def fetch_external_api_task(self, payload: Dict):
    alias = payload.get('alias')
    params = payload.get('params') or {}
    if alias not in EXTERNAL_API_CONFIG:
        raise ValueError(f"Unknown API alias '{alias}'. Supported: {', '.join(EXTERNAL_API_CONFIG)}")
    api_key = _resolve_api_key(alias)
    if not api_key:
        raise ValueError(
            f"API key for '{alias}' not found. Provide env '{EXTERNAL_API_CONFIG[alias]['env_var']}' "
            f"or a Vault secret at '{API_SECRET_PATH}/{alias}'."
        )
    config = EXTERNAL_API_CONFIG[alias]
    params_with_key = {**params, config['key_param']: api_key}
    response = requests.get(config['url'], params=params_with_key, timeout=20)
    response.raise_for_status()
    filename = _persist_result(alias, response.json())
    return {'alias': alias, 'file': filename, 'status_code': response.status_code}


@shared_task
def dispatch_external_api_jobs(messages: Optional[List[Dict]] = None):
    normalized = _normalize_messages(messages)
    for payload in normalized:
        fetch_external_api_task.delay(payload)
    return {'scheduled': len(normalized)}
