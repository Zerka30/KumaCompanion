import os


def config(args):
    print(
        """
                 _  __                      _____                                  _             
                | |/ /                     / ____|                                (_)            
                | ' /_   _ _ __ ___   __ _| |     ___  _ __ ___  _ __   __ _ _ __  _  ___  _ __  
                |  <| | | | '_ ` _ \ / _` | |    / _ \| '_ ` _ \| '_ \ / _` | '_ \| |/ _ \| '_ \ 
                | . \ |_| | | | | | | (_| | |___| (_) | | | | | | |_) | (_| | | | | | (_) | | | |
                |_|\_\__,_|_| |_| |_|\__,_|\_____\___/|_| |_| |_| .__/ \__,_|_| |_|_|\___/|_| |_|
                                                                | |                              
                                                                |_|                                               

          """
    )
    print("Version: " + os.environ["VERSION"])
    print("Github: https://github.com/Zerka/KumaCompanion")
    print("")

    if args.show:
        print_configuration()
    else:
        if args.url and args.username and args.password:
            # Set the environment variables
            os.environ["UPTIME_KUMA_URL"] = args.url
            os.environ["UPTIME_KUMA_USERNAME"] = args.username
            os.environ["UPTIME_KUMA_PASSWORD"] = args.password

            print(
                "Configuration completed. Your credentials have been stored in environment variables."
            )
        else:
            print(
                "Welcome to KumaCompanion configuration!\n"
                "Please provide the following information to configure your Uptime Kuma instance:\n"
            )

            try:
                url = input("Uptime Kuma API URL: ")
                username = input("Username: ")
                password = input("Password: ")
            except (KeyboardInterrupt, EOFError):
                print("\n\nConfiguration aborted.")
                return

            # Set the environment variables
            os.environ["UPTIME_KUMA_URL"] = url
            os.environ["UPTIME_KUMA_USERNAME"] = username
            os.environ["UPTIME_KUMA_PASSWORD"] = password

            print(
                "Configuration completed. Your credentials have been stored in environment variables."
            )


def print_configuration():
    print("Current Configuration:")
    print(f"Uptime Kuma API URL: {os.environ.get('UPTIME_KUMA_URL', 'Not set')}")
    print(f"Username: {os.environ.get('UPTIME_KUMA_USERNAME', 'Not set')}")
    print(f"Password: {os.environ.get('UPTIME_KUMA_PASSWORD', 'Not set')}")


def add_subparser(subparsers):
    config_parser = subparsers.add_parser(
        "config",  # name of the command
        aliases=["cfg", "conf"],  # aliases of the command
        help="Configure KumaCompanion",
    )

    config_parser.add_argument(
        "--show",
        help="Show current configuration",
        required=False,
        action="store_true",
    )

    config_parser.add_argument(
        "--url",
        help="Set the API URL",
        required=False,
    )

    config_parser.add_argument(
        "-u",
        "--username",
        help="Set the username",
        required=False,
    )

    config_parser.add_argument(
        "-p",
        "--password",
        help="Set the password",
        required=False,
    )

    # Default action when no subcommand is provided
    config_parser.set_defaults(func=config)
