from invoke import Collection

from .codestyle import isort
from .pip import pipcompile, pipsync


ns = Collection()

# code style
ns.add_task(isort)

# pip
pip = Collection('pip')
pip.add_task(pipcompile, 'compile')
pip.add_task(pipsync, 'sync')

ns.add_collection(pip)
