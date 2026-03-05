import os
import json
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

today = datetime.utcnow().date()

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

with open("compliance.json") as f:
    tasks = json.load(f)

for task in tasks:

    date = datetime.strptime(task["date"], "%Y-%m-%d").date()
    diff = (date - today).days

    if diff == 7:
        send(f"Reminder: {task['title']} in 7 days")

    if diff == 3:
        send(f"Reminder: {task['title']} in 3 days")

    if diff == 1:
        send(f"Reminder: {task['title']} tomorrow")

    if diff == 0:
        send(f"Reminder: {task['title']} TODAY")
