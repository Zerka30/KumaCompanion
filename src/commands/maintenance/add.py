import argparse
import config
from datetime import datetime
from uptime_kuma_api import UptimeKumaApi, MaintenanceStrategy


def add_maintenance(args):
    strategyType = {
        "manual": MaintenanceStrategy.MANUAL,
        "single": MaintenanceStrategy.SINGLE,
        "interval": MaintenanceStrategy.RECURRING_INTERVAL,
        "weekday": MaintenanceStrategy.RECURRING_WEEKDAY,
        "day_of_month": MaintenanceStrategy.RECURRING_DAY_OF_MONTH,
        "cron": MaintenanceStrategy.CRON,
    }

    data = {
        "title": args.title,
        "description": args.description,
        "strategy": strategyType[args.strategy],
        "active": True,
        "intervalDay": 1,
        "timeRange": args.timerange,
        "timezoneOption": args.timezone,
    }

    if args.daterange is not None:
        data["dateRange"] = [
            args.daterange[0].strftime("%Y-%m-%d %H:%M:%S"),
            args.daterange[1].strftime("%Y-%m-%d %H:%M:%S"),
        ]

    match args.strategy:
        case "weekday":
            data["weekdays"] = args.weekdays
        case "day_of_month":
            data["daysOfMonth"] = args.dayofmonths
        case "cron":
            data["cron"] = args.cron
            data["durationMinutes"] = args.duration

    # Connection to Uptime Kuma API
    api = UptimeKumaApi(config.UPTIME_KUMA_URL)
    api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

    # Creating a new maintenance
    # Delete key with None value
    data = {k: v for k, v in data.items() if v is not None}

    # Add maintenance
    try:
        response = api.add_maintenance(**data)
        maintenanceID = response["maintenanceID"]
    except Exception as e:
        api.disconnect()
        print("Error creating maintenance:", str(e))

    # Add impacted monitors
    impacted = []
    monitors = api.get_monitors()
    try:
        if args.impacted is None:
            args.impacted = []
        for monitor in args.impacted:
            monitor_info = next(
                (
                    m
                    for m in monitors
                    if m["name"] == monitor or m["id"] == int(monitor)
                ),
                None,
            )
            if monitor_info is not None:
                impacted.append(
                    {"id": monitor_info["id"], "name": monitor_info["name"]}
                )
            else:
                print(f"Monitor with ID or name '{monitor}' not found.")

        response = api.add_monitor_maintenance(maintenanceID, impacted)
    except Exception as e:
        api.disconnect()
        print("Error adding impacted monitors:", str(e))

    # Add maintenance to status page
    status_page = []
    pages = api.get_status_pages()
    try:
        if args.statuspage is None:
            args.statuspage = []
        for page in args.statuspage:
            page_info = next(
                (p for p in pages if p["title"] == page or p["id"] == int(page)), None
            )
            if page_info is not None:
                status_page.append({"id": page_info["id"], "name": page_info["title"]})
            else:
                print(f"Status page with ID or name '{page}' not found.")

        response = api.add_status_page_maintenance(maintenanceID, status_page)
        print(response["msg"])
        api.disconnect()
    except Exception as e:
        api.disconnect()
        print("Error adding status page:", str(e))


def weekday_list(values):
    weekdays_map = {
        "sunday": 0,
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6,
    }

    # Return list of weekdays
    return [weekdays_map[day.lower()] for day in values]


def parse_time_range(value):
    try:
        start_time, end_time = value.split("-")
        start_hour, start_minute, start_second = map(int, start_time.split(":"))
        end_hour, end_minute, end_second = map(int, end_time.split(":"))

        if (
            not (0 <= start_hour < 24)
            or not (0 <= end_hour < 24)
            or not (0 <= start_minute < 60)
            or not (0 <= end_minute < 60)
            or not (0 <= start_second < 60)
            or not (0 <= end_second < 60)
        ):
            raise argparse.ArgumentTypeError("Invalid time format in time range")

        return [
            start_hour,
            start_minute,
            start_second,
            end_hour,
            end_minute,
            end_second,
        ]
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid format for time range. Use 'start_hour:start_minute:start_second-end_hour:end_minute:end_second'"
        )


def parse_day_of_month(value):
    try:
        # Vérifier si la valeur est sous forme de plage (par exemple, "1-7")
        if "-" in value:
            start, end = map(int, value.split("-"))
            if start < 1 or end > 31 or start > end:
                raise argparse.ArgumentTypeError("Invalid day range")
            return list(range(start, end + 1))
        else:
            return [int(day) for day in value.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid value for day of month")


def parse_datetime(value):
    try:
        # Vérifier si la date est au format 'YYYY-MM-DD HH:mm:ss'
        datetime_obj = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return datetime_obj
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid date format. Use 'YYYY-MM-DD HH:mm:ss'"
        )


def maintenance_parser(subparsers):
    maintenance_parser = subparsers.add_parser(
        "add",
        aliases=["create"],
        help="Add a new maintenance",
    )

    maintenance_parser.add_argument(
        "-t", "--title", required=True, help="Set maintenance title"
    )
    maintenance_parser.add_argument(
        "-d", "--description", required=True, help="Set maintenance description"
    )
    maintenance_parser.add_argument(
        "-tz", "--timezone", help="Set maintenance timezone"
    )
    maintenance_parser.add_argument(
        "-s",
        "--strategy",
        required=True,
        choices=["manual", "single", "interval", "weekday", "day_of_month", "cron"],
        help="Set maintenance strategy",
    )

    maintenance_parser.add_argument(
        "--daterange",
        nargs=2,
        type=parse_datetime,
        metavar=("start_date", "end_date"),
        help="DateTime Range. Format: 'YYYY-MM-DD HH:mm:ss'",
    )

    maintenance_parser.add_argument(
        "-tr",
        "--timerange",
        type=parse_time_range,
        help="Maintenance Time Window of a Day. Format: 'start_hour:start_minute:start_second-end_hour:end_minute:end_second'",
    )

    maintenance_parser.add_argument(
        "-i", "--interval", type=int, help="Set maintenance interval"
    )

    maintenance_parser.add_argument(
        "--impacted",
        nargs="+",
        type=str,
        help="Set impacted monitors. You can specify monitor IDs and/or monitor names.",
    )

    maintenance_parser.add_argument(
        "--statuspage",
        nargs="+",
        type=str,
        help="Set status page. You can specify status page IDs and/or status page names.",
    )

    # Add options for specific strategy
    # Strategy: Weekday
    weekdays_group = maintenance_parser.add_argument_group(title="Weekday Options")
    weekdays_group.add_argument(
        "-w",
        "--weekdays",
        nargs="*",
        choices=[
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ],
        type=weekday_list,
        help="List of days of the week on which the maintenance is enabled. Ex: 'Monday Friday'",
    )

    # Strategy: Day of month
    dom_group = maintenance_parser.add_argument_group(title="Day of month Options")
    dom_group.add_argument(
        "--dayofmonths",
        type=parse_day_of_month,
        help="List of days of the month on which the maintenance is enabled. Ex: '1,7,14,21,30' or '1-7'",
    )

    # Strategy: Cron
    cron_group = maintenance_parser.add_argument_group(title="Cron Options")
    cron_group.add_argument(
        "-c", "--cron", default="30 3 * * *", help="Set cron expression"
    )
    cron_group.add_argument(
        "--duration", type=int, default=60, help="Set cron run time"
    )

    # Add validation function for monitor command
    maintenance_parser.set_defaults(func=add_maintenance)
