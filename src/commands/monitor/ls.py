import config
from uptime_kuma_api import UptimeKumaApi, Timeout
from tabulate import tabulate
import os


def monitor_parser(subparsers):
    """
    Add subparser for the ls command.

    Args:
        subparsers: The subparsers object to add the ls subparser to.
    """
    ls_parser = subparsers.add_parser(
        "ls",
        aliases=["list"],
        help="List all monitors",
    )

    ls_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all monitors, including disabled ones",
    )

    ls_parser.add_argument(
        "-s", "--short", action="store_true", help="Show only the name and status"
    )
    ls_parser.add_argument(
        "-i", "--no-id", action="store_true", help="Don't show the monitor id"
    )
    ls_parser.add_argument(
        "-t", "--no-type", action="store_true", help="Don't show the monitor type"
    )

    ls_parser.add_argument(
        "-u", "--no-url", action="store_true", help="Don't show the monitor url"
    )

    ls_parser.add_argument(
        "-d",
        "--no-description",
        action="store_true",
        help="Don't show the monitor description",
    )
    ls_parser.set_defaults(func=ls_monitors)


def ls_monitors(args):
    """
    List all monitors.

    Args:
        args: The arguments passed to the ls command.
    """
    # Connexion a notre instance uptime kuma
    api = UptimeKumaApi(config.UPTIME_KUMA_URL, timeout=0.5)

    # Retry to login, until it works
    success = False
    while not success:
        try:
            api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)
            success = True
        except Exception:
            success = False

    monitors = []

    try:
        monitors = api.get_monitors()
    except Exception as e:
        api.disconnect()
        print("Error listing monitors:", str(e))
        os._exit(1)

    monitors_data_table = []
    for monitor in monitors:
        try:
            monitor_beats = api.get_monitor_beats(monitor["id"], 1)
            # print(monitor_beats)
        except Exception as e:
            api.disconnect()
            print("Error listing monitors:", str(e))
            os._exit(1)

        if monitor["active"] or args.all:
            data_row = [
                monitor["name"],
                monitor_beats[-1]["status"].name.capitalize(),
            ]

            if not args.short:
                if not args.no_id:
                    data_row.insert(0, monitor["id"])

                if not args.no_type:
                    data_row.append(monitor["type"].name)

                if not args.no_url:
                    url = monitor["url"] or ""
                    hostname = monitor["hostname"] or ""
                    hostname_port = (
                        (hostname + ":" + str(monitor["port"]))
                        if hostname and monitor["port"]
                        else ""
                    )
                    dbcon = monitor["databaseConnectionString"] or ""
                    container = monitor["docker_container"] or ""

                    value = {
                        "http": url,
                        "port": hostname_port,
                        "ping": hostname,
                        "keyword": url,
                        "grpc_keyword": url,
                        "dns": hostname,
                        "docker": container,
                        "steam": hostname_port,
                        "gamedig": hostname_port,
                        "mqtt": hostname_port,
                        "sqlserver": dbcon,
                        "postgres": dbcon,
                        "mysql": dbcon,
                        "mongodb": dbcon,
                        "radius": hostname_port,
                        "redis": dbcon,
                    }

                    type = monitor["type"].name.lower()
                    data_row.append(value[type])

                if not args.no_description:
                    data_row.append(monitor["description"])

            monitors_data_table.append(data_row)
            # print(monitors_data_table)
    headers = ["NAME", "STATUS"]

    if not args.short:
        if not args.no_id:
            headers.insert(0, "ID")
        if not args.no_type:
            headers.append("TYPE")

        if not args.no_url:
            headers.append("HOSTNAME")

        if not args.no_description:
            headers.append("DESCRIPTION")

    print(
        tabulate(
            monitors_data_table,
            headers=headers,
            tablefmt="plain",
        )
    )

    api.disconnect()
