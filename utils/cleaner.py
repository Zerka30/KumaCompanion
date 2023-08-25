from src.api.KumaCompanion import KumaCompanion

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Uptime Kuma Cleaner", prog="kuma-cleaner"
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Define common arguments
    common_args = parser.add_argument_group("Common Arguments")
    common_args.add_argument(
        "-e", "--exclude", help="Specify a name to exclude from deletion"
    )
    common_args.add_argument(
        "--type",
        choices=["monitor", "status", "maintenance", "all"],
        required=True,
        help="Specify the kinds to delete",
    )

    # Define the secondary commands
    monitor_parser = subparsers.add_parser("monitor", help="Delete monitors")
    status_parser = subparsers.add_parser("status", help="Delete statuses")
    maintenance_parser = subparsers.add_parser(
        "maintenance", help="Delete maintenances"
    )

    # Add a "type" argument to each secondary command
    for cmd_parser in [monitor_parser, status_parser, maintenance_parser]:
        cmd_parser

    args = parser.parse_args()

    api = KumaCompanion().get_api()

    # Handle your command based on args.command and args.type here
    match args.type:
        case "monitor":
            try:
                # Connect to uptime kuma instance
                monitors = api.get_monitors()
                monitor_id = []

                for monitor in monitors:
                    if args.exclude is not None:
                        if args.exclude not in monitor["name"]:
                            monitor_id.append(monitor["id"])
                    else:
                        monitor_id.append(monitor["id"])
                for monitor_id in monitor_id:
                    response = api.delete_monitor(monitor_id)
                    print(response["msg"])
                KumaCompanion().disconnect()
            except Exception as e:
                KumaCompanion().disconnect()
                print("Error deleting monitors:", str(e))
        case "status":
            try:
                # Connect to uptime kuma instance
                statuses = api.get_status_pages()
                status_page = []

                for status in statuses:
                    # Check if we need to exclude a status page
                    if args.exclude is not None:
                        if args.exclude not in status["title"]:
                            status_page.append(status["slug"])
                    else:
                        status_page.append(status["slug"])
                for status_page in status_page:
                    response = api.delete_status_page(status_page)
                    print("Deleted Successfully.")
                KumaCompanion().disconnect()
            except Exception as e:
                KumaCompanion().disconnect()
                print("Error deleting statuses:", str(e))
        case "maintenance":
            try:
                # Connect to uptime kuma instance
                maintenances = api.get_maintenances()
                maintenance_id = []

                for maintenance in maintenances:
                    # Check if we need to exclude a maintenance
                    if args.exclude is not None:
                        if args.exclude not in maintenance["title"]:
                            maintenance_id.append(maintenance["id"])
                    else:
                        maintenance_id.append(maintenance["id"])
                for maintenance_id in maintenance_id:
                    response = api.delete_maintenance(maintenance_id)
                    print(response["msg"])
                KumaCompanion().disconnect()
            except Exception as e:
                KumaCompanion().disconnect()
                print("Error deleting maintenances:", str(e))
        case "all":
            try:
                # Connect to uptime kuma instance
                monitors = api.get_monitors()
                monitor_id = []

                for monitor in monitors:
                    if args.exclude is not None:
                        if args.exclude not in monitor["name"]:
                            monitor_id.append(monitor["id"])
                    else:
                        monitor_id.append(monitor["id"])
                for monitor_id in monitor_id:
                    response = api.delete_monitor(monitor_id)
                    print(response["msg"])

                # Connect to uptime kuma instance
                statuses = api.get_status_pages()
                status_page = []

                for status in statuses:
                    # Check if we need to exclude a status page
                    if args.exclude is not None:
                        if args.exclude not in status["title"]:
                            status_page.append(status["slug"])
                    else:
                        status_page.append(status["slug"])
                for status_page in status_page:
                    response = api.delete_status_page(status_page)
                    print("Deleted Successfully.")

                # Connect to uptime kuma instance
                maintenances = api.get_maintenances()
                maintenance_id = []

                for maintenance in maintenances:
                    # Check if we need to exclude a maintenance
                    if args.exclude is not None:
                        if args.exclude not in maintenance["title"]:
                            maintenance_id.append(maintenance["id"])
                    else:
                        maintenance_id.append(maintenance["id"])
                for maintenance_id in maintenance_id:
                    response = api.delete_maintenance(maintenance_id)
                    print(response["msg"])

                KumaCompanion().disconnect()
            except Exception as e:
                KumaCompanion().disconnect()
                print("Error deleting all:", str(e))


if __name__ == "__main__":
    main()
