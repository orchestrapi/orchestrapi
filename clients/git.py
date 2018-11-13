"""Git client module."""
from django.conf import settings

from . import ShellClient


class GitClient(ShellClient):

    """Special client for git commands."""
    @staticmethod
    def update(git_name):
        """Updates master branch repo."""
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}', 'pull', 'origin', 'master']
        GitClient.call(template)

    @staticmethod
    def clone(app):
        """Clone the app repo."""
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}', 'clone', f'{app.git.get("url")}']
        GitClient.call(template)

    @staticmethod
    def checkout_tag(git_name, tag):
        """Checkout to an specific tag and pulls it."""
        GitClient.fetch(git_name)
        vtag = 'master' if tag == 'latest' else f'v{tag}'
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}', 'checkout', vtag]
        GitClient.call(template)
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}', 'pull', 'origin', vtag]
        GitClient.call(template)

    @staticmethod
    def checkout_master_and_update(git_name):
        """Checkouts and pulls master"""
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}', 'checkout', 'master']
        GitClient.call(template)
        GitClient.update(git_name)

    @staticmethod
    def fetch(git_name):
        """Fetch all branches."""
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}', 'fetch']
        GitClient.call(template)
