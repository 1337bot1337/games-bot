from invoke import task
from invoke.util import cd

from .utils import project_root


@task()
def pipcompile(ctx):
    with cd(project_root):
        ctx.run('pip-compile --upgrade requirements.in', pty=True, echo=True)


@task()
def pipsync(ctx):
    with cd(project_root):
        ctx.run('pip-sync requirements.txt', pty=True, echo=True)
