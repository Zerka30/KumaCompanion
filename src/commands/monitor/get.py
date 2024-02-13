import os
import json
from api.KumaCompanion import KumaCompanion
from uptime_kuma_api import MonitorType


def get_monitor(args):
    # Connect to uptime kuma instance
    try:
        api = KumaCompanion().get_api()
    except ConnectionError as e:
        print("Error connecting to Uptime Kuma:", str(e))
        os._exit(1)

    # Fetch monitorings
    monitor_info = []
    monitors = api.get_monitors()

    monitorType = {
        "http": MonitorType.HTTP,
        "port": MonitorType.PORT,
        "ping": MonitorType.PING,
        "keyword": MonitorType.KEYWORD,
        "grpc_keyword": MonitorType.GRPC_KEYWORD,
        "dns": MonitorType.DNS,
        "docker": MonitorType.DOCKER,
        "push": MonitorType.PUSH,
        "steam": MonitorType.STEAM,
        "gamedig": MonitorType.GAMEDIG,
        "mqtt": MonitorType.MQTT,
        "sqlserver": MonitorType.SQLSERVER,
        "postgres": MonitorType.POSTGRES,
        "mysql": MonitorType.MYSQL,
        "mongodb": MonitorType.MONGODB,
        "radius": MonitorType.RADIUS,
        "redis": MonitorType.REDIS,
        "group": MonitorType.GROUP,
    }

    # Define common keys that apply to all monitor types
    common_keys = [
        "name",
        "parent",
        "description",
        "interval",
        "retryInterval",
        "resendInterval",
        "maxretries",
    ]

    additional_keys = {
        "http": [
            "url",
            "expiryNotification",
            "ignoreTls",
            "accepted_statuscodes",
            "proxyId",
            "method",
            "httpBodyEncoding",
            "body",
            "headers",
            "authMethod",
        ],
        "port": ["hostname", "port"],
        "ping": ["hostname"],
        "keyword": ["url", "keyword"],
        "grpc_keyword": ["url", "keyword"],
        "dns": ["hostname", "dns_resolve_server", "dns_resolve_type"],
        "docker": ["docker_container", "docker_host"],
        "gamedig": ["hostname", "port", "game"],
        "mqtt": [
            "hostname",
            "port",
            "mqttTopic",
            "mqttUsername",
            "mqttPassword",
            "mqttSuccessMessage",
        ],
        "sqlserver": ["databaseConnectionString", "databaseQuery"],
        "postgres": ["databaseConnectionString", "databaseQuery"],
        "mysql": ["databaseConnectionString", "databaseQuery"],
        "mongodb": ["databaseConnectionString", "databaseQuery"],
        "radius": [
            "hostname",
            "port",
            "radiusSecret",
            "radiusUsername",
            "radiusPassword",
            "radiusCalledStationId",
            "radiusCallingStationId",
        ],
        "redis": ["dbcon"],
    }

    try:
        result = []
        if args.monitor is None:
            args.monitor = []
        for monitor in args.monitor:
            for m in monitors:
                if m["name"] == monitor or m["id"] == int(monitor):
                    monitor_info.append(m)
                    break

        monitor = monitor_info[0]
        selected_keys = common_keys + additional_keys.get(
            monitorType[monitor["type"]], []
        )

        filtered_monitor_data = {
            key: monitor.get(key) for key in selected_keys if key in monitor
        }

        print(json.dumps(filtered_monitor_data, indent=4))
        return filtered_monitor_data
    except Exception as e:
        print("Error deleting monitors:", str(e))


def monitor_parser(subparsers):
    monitor_parser = subparsers.add_parser(
        "get",
        aliases=["info", "show"],
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
    monitor_parser.set_defaults(func=get_monitor)
