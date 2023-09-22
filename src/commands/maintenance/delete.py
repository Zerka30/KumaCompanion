from api.KumaCompanion import KumaCompanion


def delete_maintenance(args):
    # Connect to uptime kuma instance
    api = KumaCompanion().get_api()

    # Supression d'une maintenance
    maintenance_id = []
    maintenances = api.get_maintenances()

    try:
        result = []
        if args.maintenance is None:
            args.maintenance = []

        for maintenance in args.maintenance:
            for m in maintenances:
                print(m)
                if m["title"] == maintenance or m["id"] == maintenance:
                    maintenance_id.append(m["id"])
                    break

        for maintenance_id in maintenance_id:
            response = api.delete_maintenance(maintenance_id)
            print(response["msg"])
            result.append(response["msg"])
        # api.disconnect()
        return result
    except Exception as e:
        # api.disconnect()
        print("Error deleting maintenance:", str(e))


def maintenance_parser(subparsers):
    monitor_parser = subparsers.add_parser(
        "delete",
        aliases=["del", "rm", "remove"],
        help="Remove a maintenance",
    )

    monitor_parser.add_argument(
        "-m",
        "--maintenance",
        nargs="+",
        type=str,
        help="You can specify maintenance IDs and/or maintenance names.",
    )

    # Add validation function for monitor command
    monitor_parser.set_defaults(func=delete_maintenance)
