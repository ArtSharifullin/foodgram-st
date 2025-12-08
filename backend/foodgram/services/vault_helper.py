import requests
import os

class VaultHelper:
    def __init__(self):
        self.__vault_addr = f"{os.getenv('VAULT_ADDR')}:8200"
        self.__token = self.__get_vault_token()

    def __get_vault_token(self) -> str:
        resp = requests.post(
            url = f"{self.__vault_addr}/v1/auth/approle/login",
            json = {
                'role_id': os.getenv('VAULT_ROLE_ID'),
                'secret_id': os.getenv('VAULT_SECRET_ID'),
            }
        )

        json_data = resp.json()
        return json_data['auth']['client_token']

    def get_redis_credentials(self) -> dict:
        resp = requests.get(
            url = f"{self.__vault_addr}/v1/secret/data/data/foodgram/redis",
            headers = {
                'X-Vault-Token': self.__token,
            }
        )

        json_data = resp.json()
        return json_data['data']['data']


vault_helper = VaultHelper()