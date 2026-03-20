import os
from typing import Any, Optional

import requests


class VaultHelper:
    def __init__(self) -> None:
        raw_addr = os.getenv("VAULT_ADDR") or ""
        self.__vault_addr = raw_addr.rstrip("/")
        self.__role_id = os.getenv("VAULT_ROLE_ID") or ""
        self.__secret_id = os.getenv("VAULT_SECRET_ID") or ""
        self.__kv_mount = os.getenv("VAULT_KV_MOUNT") or "secret"
        self.__token: Optional[str] = None

        self.__enabled = all([
            self.__vault_addr,
            self.__role_id,
            self.__secret_id,
        ])

        if self.__enabled:
            self.__token = self.__get_vault_token()

    def __get_vault_token(self) -> Optional[str]:
        if not self.__enabled:
            return None

        try:
            resp = requests.post(
                url=f"{self.__vault_addr}/v1/auth/approle/login",
                json={
                    "role_id": self.__role_id,
                    "secret_id": self.__secret_id,
                },
                timeout=5,
            )
            resp.raise_for_status()
            json_data = resp.json()
            return json_data.get("auth", {}).get("client_token")
        except Exception as exc:
            print(f"[vault] Vault disabled or unavailable during login: {exc}")
            return None

    def is_enabled(self) -> bool:
        return bool(self.__enabled and self.__token)

    def __read_kv2_secret(self, path: str) -> dict[str, Any]:
        if not self.is_enabled():
            return {}

        try:
            resp = requests.get(
                url=f"{self.__vault_addr}/v1/{self.__kv_mount}/data/{path}",
                headers={
                    "X-Vault-Token": self.__token,
                },
                timeout=5,
            )
            resp.raise_for_status()
            json_data = resp.json()
            return json_data.get("data", {}).get("data", {}) or {}
        except Exception as exc:
            print(f"[vault] Failed to read secret '{path}': {exc}")
            return {}

    def get_secret(self, path: str, key: str, default: Any = None) -> Any:
        data = self.__read_kv2_secret(path)
        return data.get(key, default)

    def get_redis_credentials(self) -> dict[str, Any]:
        """
        Совместимость со старым кодом services.redis_client.
        Если Vault не настроен, возвращаем данные из ENV или безопасные defaults.
        """
        if self.is_enabled():
            data = self.__read_kv2_secret("data/foodgram/redis")
            if data:
                return data

        return {
            "host": os.getenv("REDIS_HOST", "redis-service"),
            "port": os.getenv("REDIS_PORT", "6739"),
            "db": os.getenv("REDIS_DB", "0"),
            "password": os.getenv("REDIS_PASSWORD", ""),
        }


vault_helper = VaultHelper()