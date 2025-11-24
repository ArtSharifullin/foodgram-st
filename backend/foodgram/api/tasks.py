from celery import shared_task
import requests


@shared_task
def get_chuck_joke_task():
    url = "https://api.chucknorris.io/jokes/random"
    resp = requests.get(url)
    return resp.json()

@shared_task
def get_SW_info_task(count):
    url = f"https://swapi.dev/api/people/{count}"
    resp = requests.get(url)
    return resp.json()