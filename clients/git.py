from . import ShellClient

class GitClient(ShellClient):

    @staticmethod
    def update(project):
        template = [f'{project.git_path}','git', 'pull', 'origin', 'master']
        GitClient.call(template)
