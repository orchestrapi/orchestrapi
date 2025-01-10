"""Slack client module."""

from django.conf import settings
from django.template import loader
from slack_sdk import WebClient as SlackC

class SlackClient:

    """Helper class to use slackbot."""

    def __init__(self):
        """Init method."""
        self.key = settings.SLACKBOT_KEY
        self.secret = settings.SLACKBOT_SECRET
        self.client = SlackC(token=self.key)

    def _render(self, template, context):
        """Render message from a html file."""
        template = loader.get_template(template)
        return template.render(context)

    def send(self, template, context=None):
        """Uses SLACK API to send the redered message."""
        if not settings.SLACK_BOT_ACTIVE:
            return
        if not context:
            context = dict()
        text = self._render(template, context)
        self.client.chat_postMessage(channel="general", text=text)