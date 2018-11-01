
from clients.slack import SlackClient
from core.celery import app

@app.task()
def send_slack_message(template, context):
    SlackClient().send(template, context)
