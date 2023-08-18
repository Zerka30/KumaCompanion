from uptime_kuma_api import UptimeKumaApi
import config

# Connect to uptime kuma instance
api = UptimeKumaApi(config.UPTIME_KUMA_URL)
api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

# Supression d'un monitoring
monitor_id = []
monitors = api.get_monitors()

try:
    for monitor in monitors:
        if "Python Test - " in monitor["name"]:
            monitor_id.append(monitor["id"])
    for monitor_id in monitor_id:
        response = api.delete_monitor(monitor_id)
        print(response["msg"])
    api.disconnect()
except Exception as e:
    api.disconnect()
    print("Error deleting monitors:", str(e))
