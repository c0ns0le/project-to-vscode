from os import chmod, getenv, makedirs, path, system
from re import match
from sys import argv
from venv import EnvBuilder

from git import Repo


class ExtendedEnvBuilder(EnvBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        self.activate = '{}/bin/activate'.format(context.env_dir)
        self.packages = ['autopep8', 'pep8', 'pylint', 'pylint-django']
        system('source {} && pip install -U pip'.format(self.activate))
        system('source {} && pip install {}'.format(
            self.activate, ' '.join(x for x in self.packages)
        ))
        if path.isdir('{}/../.git'.format(context.env_dir)) and system(
                'git show-branch develop'
        ):
            system('cd {}/../ && git checkout develop'.format(context.env_dir))
        if path.isfile('{}/../requirements.txt'.format(context.env_dir)):
            system('source {} && pip install -r {}/../requirements.txt'.format(
                self.activate, context.env_dir
            ))
        with open('{}/bin/activate'.format(context.env_dir), 'a') as file_act:
            file_act.write('\n')
            file_act.write('HISTFILE="$VIRTUAL_ENV/../.bash_history"\n')
            file_act.write('export HISTFILE\n')
            file_act.write('\n')


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
            Repo.clone_from(self.arg, '{}'.format(self.path_project))

    def venv(self):
        ExtendedEnvBuilder(with_pip=True).create('{}/.venv'.format(
            self.path_project
        ))

    def shortcut(self):
        with open('{}/code.desktop'.format(self.path_project), 'w') as vscode:
            vscode.write('[Desktop Entry]\n')
            vscode.write('Type = Application\n')
            vscode.write('Name = Visual Studio Code\n')
            vscode.write('Exec = bash -c ')
            vscode.write('"source {}/.venv/bin/activate && code {}"\n'.format(
                self.path_project, self.path_project
            ))
            vscode.write('Icon = code\n')
        chmod('{}/code.desktop'.format(self.path_project), 0o775)


if __name__ == '__main__':
    start = Create(argv[1])
    start.folder()
    try:
        start.git_clone()
    except:
        pass
    try:
        start.venv()
    except:
        pass
    start.shortcut()
