import argparse
from api.KumaCompanion import KumaCompanion


def add_tag(args):
    # Connection to Uptime Kuma API
    api = KumaCompanion().get_api()
    # Creating a new tag
    # Add tag
    try:
        api.add_tag(name=args.name, color=args.color)
        print("Added Successfully.")
    except Exception as e:
        api.disconnect()
        print("Error creating tag:", str(e))


def parse_hexa_color(value):
    if len(value) < 6:
        raise argparse.ArgumentTypeError("Color must be 6 characters long")
    return value


def tag_parser(subparsers):
    tag_parser = subparsers.add_parser(
        "add",
        aliases=["create"],
        help="Add a new tag",
    )

    tag_parser.add_argument("-n", "--name", required=True, help="Set tag name")
    tag_parser.add_argument(
        "-c", "--color", required=True, type=parse_hexa_color, help="Set tag color"
    )

    # Add validation function for monitor command
    tag_parser.set_defaults(func=add_tag)
