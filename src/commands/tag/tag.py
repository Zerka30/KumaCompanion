from . import add


def add_subparser(subparsers):
    tag_parser = subparsers.add_parser(
        "tag",  # name of the command
        help="Manage instance tags",
    )
    tag_subparsers = tag_parser.add_subparsers(title="Tag commands", dest="tag_command")

    # Add subparsers for each subcommand
    add.tag_parser(tag_subparsers)

    # Default action when no subcommand is provided
    tag_parser.set_defaults(func=lambda _: tag_parser.print_help())
