import os
import threading
from typing import Any, Dict, Optional

import requests


class VaultClientError(Exception):
    """Raised when Vault interaction fails."""


class VaultClient:
    """Minimal helper for fetching KV secrets from Vault."""

    def __init__(self) -> None:
        self.addr = os.getenv('VAULT_ADDR')
        self.role_id = os.getenv('VAULT_ROLE_ID')
        self.secret_id = os.getenv('VAULT_SECRET_ID')
        self.mount_point = os.getenv('VAULT_KV_MOUNT', 'secrets')
        self._token: Optional[str] = None
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    @property
    def enabled(self) -> bool:
        return all([self.addr, self.role_id, self.secret_id])

    def _login(self) -> str:
        if not self.enabled:
            raise VaultClientError(
                'Vault is not configured. Provide VAULT_ADDR/ROLE_ID/SECRET_ID.'
            )
        response = requests.post(
            f'{self.addr}/v1/auth/approle/login',
            json={
                'role_id': self.role_id,
                'secret_id': self.secret_id
            },
            timeout=10,
            proxies={'http': None, 'https': None}
        )
        response.raise_for_status()
        self._token = response.json()['auth']['client_token']
        return self._token

    def _get_token(self) -> str:
        with self._lock:
            if self._token:
                return self._token
            return self._login()

    def read_secret(self, path: str, *, force_refresh: bool = False) -> Dict[str, Any]:
        if not self.enabled:
            raise VaultClientError(
                'Vault is not configured. Provide VAULT_ADDR/ROLE_ID/SECRET_ID.'
            )
        if not force_refresh and path in self._cache:
            return self._cache[path]
        token = self._get_token()
        response = requests.get(
            f'{self.addr}/v1/{self.mount_point}/data/{path}',
            headers={'X-Vault-Token': token},
            timeout=10,
            proxies={'http': None, 'https': None}
        )
        response.raise_for_status()
        data = response.json()['data']['data']
        self._cache[path] = data
        return data

    def get_secret_value(self, path: str, key: str) -> Optional[Any]:
        secrets = self.read_secret(path)
        return secrets.get(key)


vault_client = VaultClient()


