from commands.monitor.delete import delete_monitor
from api.KumaCompanion import KumaCompanion
import argparse


# Test delete a single monitor by id
def test_delete_monitor_id():
    try:
        monitor_id = None
        monitors = KumaTest().get_monitors()
        for monitor in monitors:
            if monitor["name"] == "Python Test - HTTP":
                monitor_id = monitor["id"]
                break

        args = argparse.Namespace(monitor=[monitor_id])
        result = delete_monitor(args)
        assert result[0] == "Deleted Successfully."

    finally:
        pass


# Test delete a single monitor by name
def test_delete_monitor_name():
    args = argparse.Namespace(monitor=["Python Test - DNS"])
    result = delete_monitor(args)
    assert result[0] == "Deleted Successfully."


# Test delete list monitors by id
def test_delete_list_monitors_id():
    try:
        monitor_id = []
        monitors = KumaCompanion().get_api().get_monitors()
        for monitor in monitors:
            if (
                monitor["name"] == "Python Test - Ping"
                or monitor["name"] == "Python Test - Port"
            ):
                monitor_id.append(monitor["id"])

        args = argparse.Namespace(monitor=monitor_id)
        result = delete_monitor(args)
        assert "Deleted Successfully." in result
        assert result.count("Deleted Successfully.") == 2

    finally:
        pass


# Test delete list monitors by name
def test_delete_list_monitors_name():
    args = argparse.Namespace(monitor=["Python Test - Docker", "Python Test - GameDig"])
    result = delete_monitor(args)
    assert "Deleted Successfully." in result
    assert result.count("Deleted Successfully.") == 2
