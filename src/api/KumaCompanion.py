from uptime_kuma_api import UptimeKumaApi
import config


class KumaCompanion:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KumaCompanion, cls).__new__(cls)
            cls._instance.api = None
        return cls._instance

    def connect(self):
        if self.api is None:
            self.api = UptimeKumaApi(config.UPTIME_KUMA_URL)
            self.api.login(config.UPTIME_KUMA_USERNAME, config.UPTIME_KUMA_PASSWORD)

    def disconnect(self):
        if self.api is not None:
            self.api.disconnect()
            self.api = None

    def get_api(self):
        if self.api is None:
            self.connect()  # Connectez-vous si ce n'est pas déjà fait
        return self.api
