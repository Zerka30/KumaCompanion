from uptime_kuma_api import UptimeKumaApi
import config


class KumaTest:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KumaTest, cls).__new__(cls)
            cls._instance.api = None
            cls._instance.connect_to_api()
        return cls._instance

    def connect_to_api(self):
        if self.api is None:
            print(config.UPTIME_KUMA_URL)
            self.api = UptimeKumaApi(config.UPTIME_KUMA_URL)
            self.api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

    def get_monitors(self):
        return self.api.get_monitors()
