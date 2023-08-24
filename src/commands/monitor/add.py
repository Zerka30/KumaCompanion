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

    monitor_data = {
        "type": monitorType[args.type.lower()],
        "name": args.name,
        "parent": args.parent,
        "description": args.description,
        "interval": args.interval,
        "retryInterval": args.retry,
        "resendInterval": args.resend,
        "maxretries": args.maxretries,
        "port": args.port,
        "url": args.url,
        "hostname": args.hostname,
    }
    match args.type.lower():
        case "http":
            monitor_data["url"] = args.url
            monitor_data["expiryNotification"] = args.expirynotification
            monitor_data["ignoreTls"] = args.ignoretls
            monitor_data["accepted_statuscodes"] = args.statuscodes
            monitor_data["proxyId"] = args.proxy
            monitor_data["method"] = args.method
            monitor_data["httpBodyEncoding"] = args.bodyencoding
            monitor_data["body"] = args.body
            monitor_data["headers"] = args.headers
            monitor_data["authMethod"] = args.authmethod

            match args.authmethod:
                case "http_basic":
                    monitor_data["basic_auth_user"] = args.http_username
                    monitor_data["basic_auth_pass"] = args.http_password

                case "ntlm":
                    monitor_data["basic_auth_user"] = args.http_username
                    monitor_data["basic_auth_pass"] = args.http_password
                    monitor_data["authDomain"] = args.domain
                    monitor_data["authWorkstation"] = args.workstation

                case "mtls":
                    monitor_data["tlsCert"] = args.cert
                    monitor_data["tlsKey"] = args.key
                    monitor_data["tlsCa"] = args.ca

        case "ping":
            monitor_data["hostname"] = args.hostname

        case "keyword" | "grpc_keyword":
            monitor_data["url"] = args.url
            monitor_data["keyword"] = args.keyword

        case "dns":
            monitor_data["hostname"] = args.hostname
            monitor_data["dns_resolve_server"] = args.resolver
            monitor_data["dns_resolve_type"] = args.record

        case "docker":
            monitor_data["docker_container"] = args.container
            monitor_data["docker_host"] = args.dhost

        case "gamedig":
            monitor_data["hostname"] = args.hostname
            monitor_data["port"] = args.port
            monitor_data["game"] = args.game

        case "mqtt":
            monitor_data["hostname"] = args.hostname
            monitor_data["port"] = args.port
            monitor_data["mqttTopic"] = args.topic
            monitor_data["mqttUsername"] = args.mqtt_username
            monitor_data["mqttPassword"] = args.mqtt_password
            monitor_data["mqttSuccessMessage"] = args.mqtt_success

        case "sqlserver" | "postgres" | "mysql" | "mongodb":
            monitor_data["databaseConnectionString"] = args.dbcon
            monitor_data["databaseQuery"] = args.query

        case "radius":
            monitor_data["hostname"] = args.hostname
            monitor_data["port"] = args.port
            monitor_data["radiusSecret"] = args.radius_secret
            monitor_data["radiusUsername"] = args.radius_username
            monitor_data["radiusPassword"] = args.radius_password
            monitor_data["radiusCalledStationId"] = args.radius_called
            monitor_data["radiusCallingStationId"] = args.radius_calling

        case "redis":
            monitor_data["dbcon"] = args.dbcon

    # Connexion a notre instance uptime kuma
    api = KumaCompanion().get_api()

    # Création d'un monitoring
    # Suppression des clés avec valeur None
    monitor_data = {k: v for k, v in monitor_data.items() if v is not None}
    # Appeler la méthode add_monitor pour créer le monitoring
    try:
        response = api.add_monitor(**monitor_data)
        print(response["msg"])
        # api.disconnect()
        return response["msg"]
    except Exception as e:
        # api.disconnect()
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
