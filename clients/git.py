from . import ShellClient

from django.conf import settings

class GitClient(ShellClient):

    @staticmethod
    def update(git_name):
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}','pull', 'origin', 'master']
        GitClient.call(template)


    @staticmethod
    def clone(project):
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}','clone', f'{project.git_url}']
        GitClient.call(template)

    @staticmethod
    def checkout_tag(git_name, tag):
        GitClient.fetch(git_name)
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}','checkout', f'v{tag}']
        GitClient.call(template)
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}','pull', 'origin', f'v{tag}']
        GitClient.call(template)

    @staticmethod
    def checkout_master_and_update(git_name):
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}','checkout', 'master']
        GitClient.call(template)
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}','pull', 'origin', 'master']
        GitClient.call(template)

    @staticmethod
    def fetch(git_name):
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{git_name}','fetch']
        GitClient.call(template)