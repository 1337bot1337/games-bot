from invoke import Collection
from .pip import pipcompile, pipsync


ns = Collection()

# pip
pip = Collection('pip')
pip.add_task(pipcompile, 'compile')
pip.add_task(pipsync, 'sync')
ns.add_collection(pip)
