# tests/commands/monitor/test_add.py

from commands.monitor.add import add_monitor
from api.KumaCompanion import KumaCompanion
from uptime_kuma_api import MonitorType
import argparse


# Test add http monitor
def test_add_monitor_http():
    name = "Python Test - HTTP"
    url = "http://github.com/Zerka30/KumaCompanion"

    args = argparse.Namespace(
        type="HTTP",
        name=name,
        url=url,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()

        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["url"] == url
                assert monitor["name"] == name
                assert monitor["type"] == MonitorType.HTTP
                break

    finally:
        pass


# Test add port monitor
def test_add_monitor_port():
    name = "Python Test - Port"
    hostname = "8.8.8.8"
    port = 53

    args = argparse.Namespace(
        type="PORT",
        name=name,
        port=port,
        hostname=hostname,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()

        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["name"] == name
                assert monitor["hostname"] == hostname
                assert monitor["port"] == port
                assert monitor["type"] == MonitorType.PORT
                break
    finally:
        pass


# Test add ping monitor
def test_add_monitor_ping():
    name = "Python Test - Ping"
    hostname = "8.8.8.8"

    args = argparse.Namespace(
        type="PING",
        name=name,
        hostname=hostname,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()

        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["name"] == name
                assert monitor["hostname"] == hostname
                assert monitor["type"] == MonitorType.PING
                break
    finally:
        pass


# Test add keyword monitor
def test_add_monitor_keyword():
    name = "Python Test - Keyword"
    url = "https://banlist.zerka.dev/health"
    keyword = "running"

    args = argparse.Namespace(
        type="KEYWORD",
        name=name,
        url=url,
        keyword=keyword,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()

        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["name"] == name
                assert monitor["url"] == url
                assert monitor["keyword"] == keyword
                assert monitor["type"] == MonitorType.KEYWORD
                break
    finally:
        pass


# Test add dns monitor
def test_add_monitor_dns():
    name = "Python Test - DNS"
    hostname = "google.com"
    record = "AAAA"
    resolver = "8.8.8.8"

    args = argparse.Namespace(
        type="dNs",
        name=name,
        hostname=hostname,
        record=record,
        resolver=resolver,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()

        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["name"] == name
                assert monitor["hostname"] == hostname
                assert monitor["dns_resolve_type"] == record
                assert monitor["dns_resolve_server"] == resolver
                assert monitor["type"] == MonitorType.DNS
                break
    finally:
        pass


# Test add docker monitor
def test_add_monitor_docker():
    name = "Python Test - Docker"
    container = "uptime-kuma"
    dhost = 1

    args = argparse.Namespace(
        type="Docker",
        name="Python Test - Docker",
        container=container,
        dhost=dhost,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()

        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["name"] == name
                assert monitor["docker_container"] == container
                assert monitor["docker_host"] == dhost
                assert monitor["type"] == MonitorType.DOCKER
                break
    finally:
        pass


# Test add gamedig monitor
def test_add_monitor_gamedig():
    name = "Python Test - GameDig"
    hostname = "play.hypixel.net"
    port = 25565
    game = "minecraft"

    args = argparse.Namespace(
        type="GAMEDIG",
        name=name,
        hostname=hostname,
        port=port,
        game=game,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()

        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["name"] == name
                assert monitor["hostname"] == hostname
                assert monitor["port"] == port
                assert monitor["game"] == game
                assert monitor["type"] == MonitorType.GAMEDIG
                break
    finally:
        pass


# Test add database monitor
def test_add_monitor_db():
    name = "Python Test - Database"
    dbcon = "mysql://kuma-alive:sB6n79KGWaHxe6V6@zerka.dev:3306/alive"
    query = "SELECT * FROM run;"

    args = argparse.Namespace(
        type="MYSQL",
        name=name,
        dbcon=dbcon,
        query=query,
    )

    try:
        # Call the add_monitor function with arguments
        result = add_monitor(args)

        # Assert the result matches the expected response
        assert result == "Added Successfully."

        # Fetch the monitor
        monitors = KumaCompanion().get_api().get_monitors()
        for monitor in monitors:
            if monitor["name"] == name:
                assert monitor["name"] == name
                assert monitor["databaseConnectionString"] == dbcon
                assert monitor["databaseQuery"] == query
                assert monitor["type"] == MonitorType.MYSQL
                break
    finally:
        pass
