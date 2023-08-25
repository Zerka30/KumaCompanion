import argparse
from uptime_kuma_api import MonitorType
from api.KumaCompanion import KumaCompanion


def add_monitor(args):
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

    # Initialize the monitor_data dictionary with common keys
    monitor_data = {key: getattr(args, key, None) for key in common_keys}

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

    # Get the additional keys based on the monitor type
    additional_monitor_keys = additional_keys.get(args.type.lower(), [])

    # Update the monitor_data dictionary with additional keys
    monitor_data.update(
        {key: getattr(args, key, None) for key in additional_monitor_keys}
    )

    # Specific case, when monitor_data key is not the same as the argument name
    for arg_name in additional_monitor_keys:
        match arg_name:
            case "dns_resolve_type":
                print(arg_name)
                monitor_data.update({arg_name: getattr(args, "record", None)})
            case "dns_resolve_server":
                monitor_data.update({arg_name: getattr(args, "resolver", None)})
            case "docker_container":
                monitor_data.update({arg_name: getattr(args, "container", None)})
            case "docker_host":
                monitor_data.update({arg_name: getattr(args, "dhost", None)})
            case "databaseConnectionString":
                monitor_data.update({arg_name: getattr(args, "dbcon", None)})
            case "databaseQuery":
                monitor_data.update({arg_name: getattr(args, "query", None)})

    # Add monitor type
    monitor_data["type"] = monitorType[args.type.lower()]

    # Connection to Uptime Kuma API
    api = KumaCompanion().get_api()

    # Delete None values from the dictionary
    monitor_data = {k: v for k, v in monitor_data.items() if v is not None}

    # Add monitor
    try:
        response = api.add_monitor(**monitor_data)
        print(response["msg"])
        return response["msg"]
    except Exception as e:
        print("Error creating monitor:", str(e))


def normalize_type(value):
    return value.lower()


def monitor_parser(subparsers):
    monitor_parser = subparsers.add_parser(
        "add",
        aliases=["create"],
        help="Add a new monitor",
    )

    # Specify options for the monitoring
    monitor_parser.add_argument(
        "--type",
        required=True,
        choices=[
            "dns",
            "http",
            "docker",
            "port",
            "ping",
            "mongodb",
            "gamedig",
            "group",
            "grpc_keyword",
            "keyword",
            "mysql",
            "mqtt",
        ],
        help="Define monitor type (HTTP, Ping, Docker...)",
        type=normalize_type,
    )
    monitor_parser.add_argument(
        "-n", "--name", required=True, help="Define name of the monitoring"
    )
    monitor_parser.add_argument(
        "-d",
        "--description",
        help="Define a human-readable description for the monitoring",
    )
    monitor_parser.add_argument(
        "--parent", help="Define the ID of the parent monitor group"
    )
    monitor_parser.add_argument(
        "-i",
        "--interval",
        type=int,
        help="Define the interval between each ping in seconds",
    )
    monitor_parser.add_argument(
        "-r",
        "--retry",
        type=int,
        help="Define the number of retries before considering the service as down",
    )
    monitor_parser.add_argument(
        "--resend",
        type=int,
        help="Define the number of times to resend requests before considering the service as down",
    )
    monitor_parser.add_argument(
        "--maxretries",
        type=int,
        help="Define the maximum number of retries before the service is marked as down and a notification is sent",
    )
    monitor_parser.add_argument(
        "--url", help="Define the URL to ping for the monitoring"
    )
    monitor_parser.add_argument(
        "--hostname", help="Define the hostname for the monitoring"
    )
    monitor_parser.add_argument(
        "-p", "--port", type=int, help="Define the port to ping for the monitoring"
    )
    monitor_parser.add_argument("--packetsize", type=int, help="Define the packetsize")

    # Add options for each type
    # HTTP options
    http_group = monitor_parser.add_argument_group(title="HTTP Options")
    http_group.add_argument(
        "--expirynotification",
        action="store_true",
        help="Enable certificate expiry notification",
    )
    http_group.add_argument(
        "--ignoretls",
        action="store_true",
        help="Ignore TLS/SSL errors for HTTPS websites",
    )
    http_group.add_argument(
        "--statuscodes",
        nargs="+",
        type=int,
        help="Select status codes considered as a successful response",
    )
    http_group.add_argument("--proxy", help="Define the proxy for the monitoring")
    http_group.add_argument(
        "--method",
        choices=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        default="GET",
        help="Define the method for the monitoring",
    )
    http_group.add_argument(
        "--bodyencoding",
        choices=["json", "xml"],
        default="json",
        help="Define the body encoding for the monitoring",
    )
    http_group.add_argument("--body", help="Define the body for the monitoring")
    http_group.add_argument("--headers", help="Define the headers for the monitoring")
    http_group.add_argument(
        "--authmethod",
        choices=["none", "http_basic", "ntlm", "mtls"],
        default="NONE",
        help="Define the authentication method for the monitoring",
    )

    # Basic authentication options
    basic_auth_group = http_group.add_argument_group(
        title="HTTP Basic Authentication Options"
    )
    basic_auth_group.add_argument(
        "--http-username", help="Define the username for HTTP Basic authentication"
    )
    basic_auth_group.add_argument(
        "--http-password", help="Define the password for HTTP Basic authentication"
    )

    # NTLM authentication options
    ntlm_auth_group = http_group.add_argument_group(title="NTLM Authentication Options")
    ntlm_auth_group.add_argument(
        "--domain", help="Define the domain for NTLM authentication"
    )
    ntlm_auth_group.add_argument(
        "--workstation", help="Define the workstation for NTLM authentication"
    )

    # MTLS authentication options
    mtls_auth_group = http_group.add_argument_group(title="MTLS Authentication Options")
    mtls_auth_group.add_argument(
        "--cert", help="Define the certificate for MTLS authentication"
    )
    mtls_auth_group.add_argument("--key", help="Define the key for MTLS authentication")
    mtls_auth_group.add_argument(
        "--ca", help="Define the certificate authority for MTLS authentication"
    )

    # Keyword options
    keyword_group = monitor_parser.add_argument_group(title="Keyword Options")
    keyword_group.add_argument(
        "--keyword", help="Define the keyword to search for in the response"
    )

    # DNS options
    dns_group = monitor_parser.add_argument_group(title="DNS Options")
    dns_group.add_argument(
        "--resolver", help="Define the resolver server to use for DNS query"
    )
    dns_group.add_argument(
        "--record",
        choices=["A", "AAAA", "CAA", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT"],
        help="Define the DNS record type to query",
    )

    # Docker options
    docker_group = monitor_parser.add_argument_group(title="Docker Options")
    docker_group.add_argument(
        "--container", help="Define the container name or id for the monitoring"
    )
    docker_group.add_argument("--dhost", help="Define the Docker host to use")

    # MQTT options
    mqtt_group = monitor_parser.add_argument_group(title="MQTT Options")
    mqtt_group.add_argument("--topic", help="Define the MQTT topic to subscribe to")
    mqtt_group.add_argument(
        "--mqtt-username", help="Define the username for MQTT authentication"
    )
    mqtt_group.add_argument(
        "--mqtt-password", help="Define the password for MQTT authentication"
    )

    # Database options
    db_group = monitor_parser.add_argument_group(title="Database Options")
    db_group.add_argument("--dbcon", help="Define the database connection string")
    db_group.add_argument("--query", help="Define the SQL or MongoDB query to execute")

    # Radius options
    radius_group = monitor_parser.add_argument_group(title="Radius Options")
    radius_group.add_argument("--radius-secret", help="Define the Radius secret")
    radius_group.add_argument(
        "--radius-username", help="Define the username for Radius authentication"
    )
    radius_group.add_argument(
        "--radius-password", help="Define the password for Radius authentication"
    )
    radius_group.add_argument(
        "--radius-called", help="Define the called station ID for Radius authentication"
    )
    radius_group.add_argument(
        "--radius-calling",
        help="Define the calling station ID for Radius authentication",
    )

    # Gamedig options
    gamedig_group = monitor_parser.add_argument_group(title="Gamedig Options")
    gamedig_group.add_argument("--game", help="Define game")

    # Add validation function for monitor command
    monitor_parser.set_defaults(validate=validate_monitor_args, func=add_monitor)

    # Disconnect from API
    KumaCompanion().disconnect()


def validate_monitor_args(args):
    # Custom validation for monitor command
    required_params = {
        "http": ["url"],
        "port": ["hostname", "port"],
        "ping": ["hostname"],
        "keyword": ["url", "keyword"],
        "grpc_keywword": ["url", "keyword"],
        "dns": ["hostname"],
        "docker": ["container"],
        "steam": ["hostname", "port"],
        "gamedig": ["hostname", "port", "game"],
        "mqtt": ["hostname", "port", "topic"],
        "sqlserver": ["dbcon", "query"],
        "postgres": ["dbcon", "query"],
        "mysql": ["dbcon", "query"],
        "mongodb": ["dbcon", "query"],
        "radius": [
            "hostname",
            "port",
            "radius_username",
            "radius_password",
            "radius_secret",
            "radius_called",
            "radius_calling",
        ],
        "redis": ["dbcon"],
    }

    missing_params = []
    for param in required_params[args.type.lower()]:
        if not getattr(args, param):
            missing_params.append(f"--{param}")

    if missing_params:
        param_list = ", ".join(missing_params)
        raise argparse.ArgumentTypeError(
            f"Missing required parameters for type '{args.type}': {param_list}"
        )

    return args
