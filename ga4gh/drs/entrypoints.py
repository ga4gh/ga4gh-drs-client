import click
import sys

from ga4gh.drs.cli.main_cli import MainCLI
from ga4gh.drs.exceptions.cli_exception import CLIException
from ga4gh.drs.routes.route_object_info import RouteObjectInfo

@click.command()
@click.option("--url", "-u", help="DRS Service Base URL")
@click.option("--object-id", "-i", help="DRS Object Id")
@click.option("--download", "-d", is_flag=True, 
    help="Flag. If set, download object bytes")
@click.option("--expand", "-x", is_flag=True, 
    help="Flag. If set, program will recursively traverse inner bundles within "
        + "the root bundle")
@click.option("--validate", "-v", is_flag=True, 
    help="Flag. If set, perform checksum validation on downloaded objects")
@click.option("--output-dir", "-o",
    help="Directory to write downloaded files")
def main(url, object_id, download, expand, validate, output_dir):

    kwargs = {
        "url": url,
        "object_id": object_id,
        "download": download,
        "expand": expand,
        "validate": validate,
        "output_dir": output_dir
    }

    try:

        cli = MainCLI(**kwargs)
        cli.validate_args()
        route_obj_info = RouteObjectInfo(url, object_id, expand)
        response = route_obj_info.issue_request()

        if download:
            pass
        
    except CLIException as e:
        print(str(e) + "\n")
        with click.Context(main) as ctx:
            click.echo(main.get_help(ctx))
        sys.exit(1)
