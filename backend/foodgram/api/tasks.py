from celery import shared_task
import requests

@shared_task
def get_quote_task(count):
    url = f"https://api.breakingbadquotes.xyz/v1/quotes/{count}"
    resp = requests.get(url)
    return resp.json()

@shared_task
def get_cat_fact_task(count):
    url = f"https://meowfacts.herokuapp.com/?count={count}"
    resp = requests.get(url)
    return resp.json()