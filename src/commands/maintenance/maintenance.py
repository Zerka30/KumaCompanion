from . import add, delete


def add_subparser(subparsers):
    maintenance_parser = subparsers.add_parser(
        "maintenance",  # name of the command
        help="Manage maintenance",
    )
    maintenance_subparsers = maintenance_parser.add_subparsers(
        title="Maintenance commands", dest="maintenance_command"
    )

    # Add subparsers for each subcommand
    add.maintenance_parser(maintenance_subparsers)
    delete.maintenance_parser(maintenance_subparsers)

    # Default action when no subcommand is provided
    maintenance_parser.set_defaults(func=lambda _: maintenance_parser.print_help())
