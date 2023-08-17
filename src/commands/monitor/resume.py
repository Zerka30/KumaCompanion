import config
from uptime_kuma_api import UptimeKumaApi


def resume_monitor(args):
    # Connect to uptime kuma instance
    api = UptimeKumaApi(config.UPTIME_KUMA_URL)
    api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

    # Resume un monitoring
    monitors_ids = []
    monitors = api.get_monitors()

    try:
        if args.monitor is None:
            args.monitor = []
        for monitor in args.monitor:
            for m in monitors:
                if m["name"] == monitor or m["id"] == monitor:
                    monitors_ids.append(m["id"])
                    break

        for monitor_id in monitors_ids:
            response = api.resume_monitor(monitor_id)
            print(response["msg"])
        api.disconnect()
    except Exception as e:
        api.disconnect()
        print("Error deleting monitors:", str(e))


def monitor_parser(subparsers):
    monitor_parser = subparsers.add_parser(
        "resume",
        help="Resume a monitor",
    )

    monitor_parser.add_argument(
        "-m",
        "--monitor",
        nargs="+",
        type=str,
        help="You can specify monitor IDs and/or monitor names.",
    )

    # Add validation function for monitor command
    monitor_parser.set_defaults(func=resume_monitor)
