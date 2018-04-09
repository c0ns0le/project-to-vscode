from sys import argv
from os import getenv, path, makedirs, chmod, system
from re import match
from git import Repo

from venv import EnvBuilder


class ExtendedEnvBuilder(EnvBuilder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path_project = args[0]

    def post_setup(self, context):
        activate = '{}/bin/activate'.format(context.env_dir)
        system('source {} && pip install -U pip'.format(activate))
        system('source {} && pip install pylint'.format(activate))
        system('source {} && pip install pep8'.format(activate))

        if path.isfile('{}/development.txt'.format(self.path_project)):
            system('source {} && pip install -r {}/development.txt'.format(
                activate, self.path_project))


class Create(object):

    def __init__(self, arg):
        self.path_workspace = '{}/{}'.format(getenv('HOME'), 'Projects')
        self.arg = arg

        if match('^https://github.com/', self.arg):
            self.git = True
            self.name = self.arg.split('/')[-1][:-4]
        else:
            self.git = False
            self.name = self.arg

        self.path_project = '{}/{}'.format(self.path_workspace, self.name)

    def folder(self):
        makedirs('{}'.format(self.path_project), exist_ok=True)

    def git_clone(self):
        if self.git:
            Repo.clone_from(self.arg, '{}'.format(self.path_workspace))

    def venv(self):
        ExtendedEnvBuilder(self.path_project, with_pip=True).create(
            '{}/.venv'.format(self.path_project))

    def shortcut(self):
        with open('{}/code.desktop'.format(
                self.path_project), 'w') as vscode:
            vscode.write('[Desktop Entry]\n')
            vscode.write('Type = Application\n')
            vscode.write('Name = Visual Studio Code\n')
            vscode.write('Exec = bash -c ')
            vscode.write(
                '"source {}/.venv/bin/activate && code {}"\n'.format(
                    self.path_project, self.path_project))
            vscode.write('Icon = code\n')
        chmod('{}/code.desktop'.format(self.path_project), 0o775)

if __name__ == '__main__':
    start = Create(argv[1])
    start.folder()
    start.git_clone()
    start.venv()
    start.shortcut()
