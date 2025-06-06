from invoke import task
from invoke.context import Context

@task
def ingest(ctx: Context):
    ctx.run("python src/data_eng/stage1_ingestion.py")

@task
def clean(ctx: Context):
    ctx.run("python src/data_eng/stage2_cleaning.py")

@task
def features(ctx: Context):
    ctx.run("python src/data_eng/stage3_labeling.py")

@task
def split(ctx: Context):
    ctx.run("python src/data_eng/stage4_splitting.py")

@task
def data_eng_pipeline(ctx: Context):
    ingest(ctx)
    clean(ctx)
    features(ctx)
    split(ctx)
    
@task(help={'mensaje': "Mensaje del commit"})
def git(ctx: Context, mensaje: str):
    ctx.run("git add .")
    ctx.run(f'git commit -m "{mensaje}"')
    ctx.run("git push origin main")