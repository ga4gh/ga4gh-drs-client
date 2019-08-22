import click

@click.group()
def schemes():
    pass

@schemes.command()
def ls():
    pass

@schemes.command()
def update_supported():
    pass

