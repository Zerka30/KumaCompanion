from api.KumaCompanion import KumaCompanion
import os
from tabulate import tabulate


def tag_parser(subparsers):
    ls_parser = subparsers.add_parser(
        "ls",
        aliases=["list"],
        help="List all monitors",
    )
    
    ls_parser.set_defaults(func=ls_tags)


def ls_tags(args):
    # Connection to uptime kuma instance
    try:
        api = KumaCompanion().get_api()
    except ConnectionError as e:
        print("Error connecting to Uptime Kuma:", str(e))
        os._exit(1)
        
    tags = []
    
    try:
        tags = api.get_tags()
    except Exception as e:
        print("Error listing monitors:", str(e))
        os._exit(1)
        
    tags_data_table = []
    for tag in tags:
        data_row = [
            tag["id"],
            tag["name"],
            tag["color"],
        ]
        
        tags_data_table.append(data_row)
    
    headers = ["ID", "NAME", "COLOR"]
    
    print(
        tabulate(
            tags_data_table,
            headers=headers,
            tablefmt="plain",
        )
    )