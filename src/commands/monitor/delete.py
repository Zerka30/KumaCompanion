import config
from uptime_kuma_api import UptimeKumaApi


def delete_monitor(args):
    # Connect to uptime kuma instance
    api = UptimeKumaApi(config.UPTIME_KUMA_URL)
    api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

    # Supression d'un monitoring
    monitor_id = []
    monitors = api.get_monitors()

    try:
        if args.monitor is None:
            args.monitor = []
        for monitor in args.monitor:
            for m in monitors:
                if m["name"] == monitor or m["id"] == monitor:
                    monitor_id.append(m["id"])
                    break

        for monitor_id in monitor_id:
            response = api.delete_monitor(monitor_id)
            print(response["msg"])
        api.disconnect()
    except Exception as e:
        api.disconnect()
        print("Error deleting monitors:", str(e))


def monitor_parser(subparsers):
    monitor_parser = subparsers.add_parser(
        "delete",
        aliases=["del", "rm", "remove"],
        help="Remove a monitor",
    )

    monitor_parser.add_argument(
        "-m",
        "--monitor",
        nargs="+",
        type=str,
        help="You can specify monitor IDs and/or monitor names.",
    )

    # Add validation function for monitor command
    monitor_parser.set_defaults(func=delete_monitor)
