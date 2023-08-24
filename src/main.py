import argparse
import config as cfg
from commands.monitor import monitor
from commands.maintenance import maintenance
from commands.config import config
from api.KumaCompanion import KumaCompanion


def main():
    parser = argparse.ArgumentParser(description="KumaCompanion CLI", prog="kuma")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="KumaCompanion v" + cfg.VERSION,
        help="Show KumaCompanion version",
    )

    # Add subparsers for each top-level command
    monitor.add_subparser(subparsers)
    maintenance.add_subparser(subparsers)
    config.add_subparser(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        # Validate the arguments
        if hasattr(args, "validate"):
            try:
                args = args.validate(args)
            except argparse.ArgumentTypeError as e:
                parser.error(str(e))

        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    KumaCompanion().disconnect()
