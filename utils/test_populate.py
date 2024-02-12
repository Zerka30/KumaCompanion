from src.api.KumaCompanion import KumaCompanion
from uptime_kuma_api import MonitorType


def main():
    api = KumaCompanion().get_api()

    for i in range(1, 7):
        api.add_monitor(
            type=MonitorType.HTTP,
            name=f"DO NOT DELETE #{i}",
            url="http://google.com",
        )

    KumaCompanion().disconnect()


if __name__ == "__main__":
    main()
