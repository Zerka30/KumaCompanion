from api.KumaCompanion import KumaCompanion


def resume_monitor(args):
    # Connect to uptime kuma instance
    api = KumaCompanion().get_api()

    # Resume un monitoring
    monitors_ids = []
    monitors = api.get_monitors()

    try:
        result = []
        if args.monitor is None:
            args.monitor = []
        for monitor in args.monitor:
            for m in monitors:
                if m["name"] == monitor or m["id"] == int(monitor):
                    monitors_ids.append(m["id"])
                    break

        for monitor_id in monitors_ids:
            response = api.resume_monitor(monitor_id)
            print(response["msg"])
            result.append(response["msg"])
        # api.disconnect()
        return result
    except Exception as e:
        # api.disconnect()
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
