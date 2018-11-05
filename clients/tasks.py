"""Tasks for clients app."""
from clients.slack import SlackClient
from core.celery import app


@app.task()
def send_slack_message(template, context):
    """Send a Slack message using Celery."""
    SlackClient().send(template, context)
