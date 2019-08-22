import click
from ga4gh.drs.cli.parsing.get import get
from ga4gh.drs.cli.parsing.schemes import schemes

@click.group()
def main():
    pass

main.add_command(get)
main.add_command(schemes)
