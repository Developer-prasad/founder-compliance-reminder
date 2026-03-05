import os
import json
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
founders = json.loads(os.getenv("FOUNDERS_JSON"))

WELCOME_MESSAGE = """
Welcome to the Founder Compliance Bot.

This bot sends important compliance reminders including:

• GST filing deadlines
• MCA filings
• Income tax reminders
• Other regulatory tasks

Please DO NOT mute this bot. Missing a compliance deadline can result in penalties.

You will automatically receive reminders before important filing dates.
This bot is created and maintained by @developer_prasad.
"""

today = datetime.utcnow().date()


def send(chat_id, message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message
        }
    )


def check_new_users():

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    res = requests.get(url).json()

    updates = res["result"]

    known_names = [f["name"] for f in founders]

    for update in updates:

        if "message" not in update:
            continue

        name = update["message"]["chat"].get("first_name", "Founder")
        chat_id = update["message"]["chat"]["id"]

        if name not in known_names:

            founders.append({
                "name": name,
                "chat_id": chat_id
            })

            send(chat_id, WELCOME_MESSAGE)


check_new_users()

with open("compliance.json") as f:
    tasks = json.load(f)

for task in tasks:

    event_date = datetime.strptime(task["date"], "%Y-%m-%d").date()
    diff = (event_date - today).days

    if diff in [7, 3, 1, 0]:

        if diff == 0:
            message = f"⚠️ TODAY: {task['title']}"
        else:
            message = f"Reminder: {task['title']} in {diff} days"

        for founder in founders:
            send(founder["chat_id"], message)
