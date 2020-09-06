from invoke import task


@task()
def isort(ctx):
    ctx.run('isort .')
