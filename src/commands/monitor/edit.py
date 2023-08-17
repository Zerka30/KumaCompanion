import argparse
import config
from uptime_kuma_api import UptimeKumaApi, MonitorType


def edit_monitor(args):
    monitorType = {
        "HTTP": MonitorType.HTTP,
        "PORT": MonitorType.PORT,
        "PING": MonitorType.PING,
        "KEYWORD": MonitorType.KEYWORD,
        "GRPC_KEYWORD": MonitorType.GRPC_KEYWORD,
        "DNS": MonitorType.DNS,
        "DOCKER": MonitorType.DOCKER,
        "PUSH": MonitorType.PUSH,
        "STEAM": MonitorType.STEAM,
        "GAMEDIG": MonitorType.GAMEDIG,
        "MQTT": MonitorType.MQTT,
        "SQLSERVER": MonitorType.SQLSERVER,
        "POSTGRES": MonitorType.POSTGRES,
        "MYSQL": MonitorType.MYSQL,
        "MONGODB": MonitorType.MONGODB,
        "RADIUS": MonitorType.RADIUS,
        "REDIS": MonitorType.REDIS,
        "GROUP": MonitorType.GROUP,
    }

    monitor_data = {
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

    if args.type is not None:
        monitor_data["type"] = monitorType[args.type.upper()]

    match args.type:
        case "HTTP":
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
                case "HTTP_BASIC":
                    monitor_data["basic_auth_user"] = args.http_username
                    monitor_data["basic_auth_pass"] = args.http_password

                case "NTLM":
                    monitor_data["basic_auth_user"] = args.http_username
                    monitor_data["basic_auth_pass"] = args.http_password
                    monitor_data["authDomain"] = args.domain
                    monitor_data["authWorkstation"] = args.workstation

                case "MTLS":
                    monitor_data["tlsCert"] = args.cert
                    monitor_data["tlsKey"] = args.key
                    monitor_data["tlsCa"] = args.ca

        case "Ping":
            monitor_data["hostname"] = args.hostname

        case "Keyword" | "GRPC_KEYWORD":
            monitor_data["url"] = args.url
            monitor_data["keyword"] = args.keyword

        case "DNS":
            monitor_data["hostname"] = args.hostname
            monitor_data["dns_resolve_server"] = args.resolver
            monitor_data["dns_resolve_type"] = args.record

        case "Docker":
            monitor_data["docker_container"] = args.container
            monitor_data["docker_host"] = args.dhost

        case "GameDig":
            monitor_data["hostname"] = args.hostname
            monitor_data["port"] = args.port
            monitor_data["game"] = args.game

        case "MQTT":
            monitor_data["hostname"] = args.hostname
            monitor_data["port"] = args.port
            monitor_data["mqttTopic"] = args.topic
            monitor_data["mqttUsername"] = args.mqtt_username
            monitor_data["mqttPassword"] = args.mqtt_password
            monitor_data["mqttSuccessMessage"] = args.mqtt_success

        case "SQLServer" | "Postgres" | "MySQL" | "MongoDB":
            monitor_data["databaseConnectionString"] = args.dbcon
            monitor_data["databaseQuery"] = args.query

        case "Radius":
            monitor_data["hostname"] = args.hostname
            monitor_data["port"] = args.port
            monitor_data["radiusSecret"] = args.radius_secret
            monitor_data["radiusUsername"] = args.radius_username
            monitor_data["radiusPassword"] = args.radius_password
            monitor_data["radiusCalledStationId"] = args.radius_called
            monitor_data["radiusCallingStationId"] = args.radius_calling

        case "Redis":
            monitor_data["dbcon"] = args.dbcon

    # Delete empty key
    monitor_data = {k: v for k, v in monitor_data.items() if v is not None}

    # Connection to uptime kuma instance
    api = UptimeKumaApi(config.UPTIME_KUMA_URL)
    api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

    # Fetch monitor
    monitor_id = []
    monitors = api.get_monitors()

    try:
        for m in monitors:
            if m["name"] == args.monitor or m["id"] == args.monitor:
                monitor_id.append(m["id"])
                break

        # Edit monitor
        response = api.edit_monitor(monitor_id[0], **monitor_data)
        print(response["msg"])
        api.disconnect()
    except Exception as e:
        api.disconnect()
        print("Error updating monitors:", str(e))


def normalize_type(value):
    return value.lower()


def monitor_parser(subparsers):
    monitor_parser = subparsers.add_parser(
        "edit",
        aliases=["update"],
        help="Edit a monitor",
    )

    # Specify options for the monitoring
    monitor_parser.add_argument(
        "--type",
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
    monitor_parser.add_argument("-n", "--name", help="Define name of the monitoring")
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

    monitor_parser.add_argument(
        "-m",
        "--monitor",
        type=str,
        required=True,
        help="You can specify monitor IDs and/or monitor names.",
    )

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
        choices=["NONE", "HTTP_BASIC", "NTLM", "MTLS"],
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
    monitor_parser.set_defaults(func=edit_monitor)
