from api.KumaCompanion import KumaCompanion


def delete_tag(args):
    # Connect to uptime kuma instance
    api = KumaCompanion().get_api()

    # Supression d'un monitoring
    tags_id = []
    tags = api.get_tags()

    try:
        result = []
        if args.tag is None:
            args.tag = []
        for tag in args.tag:
            for t in tags:
                if t["name"] == tag or t["id"] == int(t["id"]):
                    tags_id.append(t["id"])
                    break

        for tag_id in tags_id:
            response = api.delete_tag(tag_id)
            print(response["msg"])
            result.append(response["msg"])
        # api.disconnect()
        return result
    except Exception as e:
        # api.disconnect()
        print("Error deleting tag:", str(e))


def tag_parser(subparsers):
    tag_parser = subparsers.add_parser(
        "delete",
        aliases=["del", "rm", "remove"],
        help="Remove a uptime kuma tag",
    )

    tag_parser.add_argument(
        "-t",
        "--tag",
        nargs="+",
        type=str,
        help="You can specify tag IDs and/or tag names.",
        required=True,
    )

    # Add validation function for monitor command
    tag_parser.set_defaults(func=delete_tag)
