from commands.monitor.pause import pause_monitor
from commands.monitor.resume import resume_monitor
import argparse


# Test pause a single monitor by id
def test_pause_monitor_id():
    args = argparse.Namespace(monitor=[374])
    result = pause_monitor(args)
    assert result[0] == "Paused Successfully."


# Test pause a single monitor by name
def test_pause_monitor_name():
    args = argparse.Namespace(monitor=["DO NOT DELETE #2"])
    result = pause_monitor(args)
    assert result[0] == "Paused Successfully."


# Test list of monitors by id
def test_pause_monitor_list_id():
    args = argparse.Namespace(monitor=[376, 377])
    result = pause_monitor(args)
    assert "Paused Successfully." in result
    assert result.count("Paused Successfully.") == 2


# Test list of monitors by name
def test_pause_monitor_list_name():
    args = argparse.Namespace(monitor=["DO NOT DELETE #5", "DO NOT DELETE #6"])
    result = pause_monitor(args)
    assert "Paused Successfully." in result
    assert result.count("Paused Successfully.") == 2


# Test resume a single monitor by id
def test_resume_monitor_id():
    args = argparse.Namespace(monitor=[374])
    result = resume_monitor(args)
    assert result[0] == "Resumed Successfully."


# Test resume a single monitor by name
def test_resume_monitor_name():
    args = argparse.Namespace(monitor=["DO NOT DELETE #2"])
    result = resume_monitor(args)
    assert result[0] == "Resumed Successfully."


# Test resume list of monitors by id
def test_resume_monitor_list_id():
    args = argparse.Namespace(monitor=[376, 377])
    result = resume_monitor(args)
    assert "Resumed Successfully." in result
    assert result.count("Resumed Successfully.") == 2


# Test resume list of monitors by name
def test_resume_monitor_list_name():
    args = argparse.Namespace(monitor=["DO NOT DELETE #5", "DO NOT DELETE #6"])
    result = resume_monitor(args)
    assert "Resumed Successfully." in result
    assert result.count("Resumed Successfully.") == 2
