from . import ShellClient

from django.conf import settings

class GitClient(ShellClient):

    @staticmethod
    def update(project):
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}/{project.git_name}','pull', 'origin', 'master']
        GitClient.call(template)


    @staticmethod
    def clone(project):
        template = ['git', '-C', f'{settings.GIT_PROJECTS_ROUTE}','clone', f'{project.git_url}']
        GitClient.call(template)
