import requests

resp = requests.post(
    url="http://localhost:8200/v1/auth/approle/login",
    json={
        "role_id": "cb4a6323-0a03-7f30-e249-5e3647812b30",
        "secret_id": "7ea2ad02-e0bc-390e-ef45-b3aada0a39c7"
    }
)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
