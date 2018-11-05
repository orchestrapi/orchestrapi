"""Slack client module."""

from django.conf import settings
from django.template import loader
from slackclient import SlackClient as SlackC


class SlackClient:

    """Helper class to use slackbot."""

    def __init__(self):
        """Init method."""
        self.key = settings.SLACKBOT_KEY
        self.secret = settings.SLACKBOT_SECRET
        self.sc = SlackC(self.key)

    def _render(self, template, context):
        """Render message from a html file."""
        template = loader.get_template(template)
        return template.render(context)

    def send(self, template, context={}):
        """Uses SLACK API to send the redered message."""
        if not settings.SLACK_BOT_ACTIVE:
            return

        text = self._render(template, context)
        self.sc.api_call(
            "chat.postMessage",
            channel="general",
            text=text
        )
