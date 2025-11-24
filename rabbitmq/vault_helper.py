from dotenv import load_dotenv
import requests
import os

class VaultHelper:
    def __init__(self):
        load_dotenv('../.env')
        self.__vault_addr = os.getenv('VAULT_ADDR')
        self.__token = self.__get_client_token()

    def __get_client_token(self) -> str:
        url = f"{self.__vault_addr}/v1/auth/approle/login"
        role_id = os.getenv('VAULT_ROLE_ID')
        secret_id = os.getenv('VAULT_SECRET_ID')
        
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Role ID: {role_id}")
        print(f"[DEBUG] Secret ID: {secret_id}")
        
        resp = requests.post(
            url=url,
            json={
                "role_id": role_id,
                "secret_id": secret_id
            },
            proxies={'http': None, 'https': None}
        )
        
        print(f"[DEBUG] Status code: {resp.status_code}")
        print(f"[DEBUG] Response text: {resp.text[:200]}")
        
        resp.raise_for_status()
        json_data = resp.json()
        return json_data["auth"]["client_token"]



    def __get_secrets(self, secret_path: str):
        resp = requests.get(
            url=f"{self.__vault_addr}/v1/secrets/data/{secret_path}",
            headers={
                'X-Vault-Token': self.__token
            },
            proxies={'http': None, 'https': None}
        )
        
        resp.raise_for_status()
        json_data = resp.json()
        return json_data['data']['data']


    def get_rabbitmq_credentials(self) -> dict:
        return self.__get_secrets("rabbitmq")

    def get_api_key(self, alias: str) -> str:
        api_data = self.__get_secrets("apikeys")
        return api_data[alias]
    
vault_helper = VaultHelper() 