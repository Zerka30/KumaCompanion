from . import add, ls, delete, pause, resume, edit, get


def add_subparser(subparsers):
    monitor_parser = subparsers.add_parser(
        "monitor",  # name of the command
        help="Manage monitors",
    )

    monitor_subparsers = monitor_parser.add_subparsers(
        title="Monitor commands", dest="monitor_command"
    )

    # Add subparsers for each subcommand
    add.monitor_parser(monitor_subparsers)
    ls.monitor_parser(monitor_subparsers)
    delete.monitor_parser(monitor_subparsers)
    resume.monitor_parser(monitor_subparsers)
    pause.monitor_parser(monitor_subparsers)
    edit.monitor_parser(monitor_subparsers)
    get.monitor_parser(monitor_subparsers)

    # Default action when no subcommand is provided
    monitor_parser.set_defaults(func=lambda _: monitor_parser.print_help())
