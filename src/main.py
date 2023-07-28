import argparse
from commands import create

def main():
    parser = argparse.ArgumentParser(description="KumaCompanion CLI - Create")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Add subparsers for each top-level command
    create.add_subparser(subparsers)

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
        print("YOOO")
        parser.print_help()

def validate_monitor_args(args):
    # Custom validation for monitor command
    if args.type == "HTTP" and not args.url:
        raise argparse.ArgumentTypeError("--url is required for type 'HTTP'")
    if args.type == "Ping" and not args.hostname:
        raise argparse.ArgumentTypeError("--hostname is required for type 'Ping'")
    return args

if __name__ == "__main__":
    main()
