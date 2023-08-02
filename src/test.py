from uptime_kuma_api import UptimeKumaApi, MaintenanceStrategy
import config

api = UptimeKumaApi(config.UPTIME_KUMA_URL)
api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

data = {'title': 'kuma test', 'description': 'kuma test', 'strategy': MaintenanceStrategy.MANUAL, 'active': True, 'intervalDay': 1}

response = api.add_maintenance(**data)
print(response["msg"])

api.disconnect()