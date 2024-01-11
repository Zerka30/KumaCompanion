import os
import subprocess

from socketio.exceptions import TimeoutError
from uptime_kuma_api import Timeout, UptimeKumaApi, UptimeKumaException


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
    print("Version: 1.0.0")
    print("Github: https://github.com/Zerka/KumaCompanion")
    print("")

    if args.show:
        print_configuration()
    else:
        if (args.url and args.username and args.password) or (
            config.UPTIME_KUMA_URL
            and config.UPTIME_KUMA_USERNAME
            and config.UPTIME_KUMA_PASSWORD
        ):
            success = False

            try:
                api = UptimeKumaApi(args.url)
                result, error_message = is_correct_credentials(
                    api, args.username, args.password
                )
                api.disconnect()
                # Use the function directly in the if statement
                # raise Timeout()
                if result:
                    print("\n✓ Login successful")
                    success = True
                else:
                    print("\nX Login failed:", error_message)
                    return
            except (UptimeKumaException, ConnectionError):
                print("\nX Login failed: Unable to connect")
                print("\nPlease check your network connection and try again !")
            except (Timeout, TimeoutError):
                api.disconnect()
                print("\nX Login failed: Connection timed out")
                return
            except Exception as e:
                api.disconnect()
                print("\nLogin failed:", e)
                return

            if success:
                # Set the environment variables
                os.environ["UPTIME_KUMA_URL"] = args.url
                os.environ["UPTIME_KUMA_USERNAME"] = args.username
                os.environ["UPTIME_KUMA_PASSWORD"] = args.password

                # Update the .bashrc file
                update_bashrc()

                print(
                    "\nConfiguration completed. Your credentials have been stored in environment variables."
                )
                print(
                    "Please reload your shell to use the new configuration or run 'source ~/.bashrc'"
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

            success = False

            try:
                api = UptimeKumaApi(url)
                result, error_message = is_correct_credentials(api, username, password)
                api.disconnect()
                # Use the function directly in the if statement
                if result:
                    print("\n✓ Login successful")
                    success = True
                else:
                    print("\nX Login failed:", error_message)
                    return
            except (UptimeKumaException, ConnectionError):
                print("\nX Login failed: Unable to connect")
                print("\nPlease check your network connection and try again !")
            except (Timeout, TimeoutError):
                api.disconnect()
                print("\nX Login failed: Connection timed out")
                return
            except Exception as e:
                api.disconnect()
                print("\nLogin failed:", e)
                return

            if success:
                # Set the environment variables
                os.environ["UPTIME_KUMA_URL"] = url
                os.environ["UPTIME_KUMA_USERNAME"] = username
                os.environ["UPTIME_KUMA_PASSWORD"] = password

                # Update the .bashrc file
                update_bashrc()

                print(
                    "\nConfiguration completed. Your credentials have been stored in environment variables."
                )
                print(
                    "Please reload your shell to use the new configuration or run 'source ~/.bashrc'"
                )


def update_bashrc():
    # Get the current user's home directory
    home_dir = os.path.expanduser("~")

    # Generate the lines to be added to the .bashrc file
    lines = [
        f'export UPTIME_KUMA_URL="{os.environ["UPTIME_KUMA_URL"]}"\n',
        f'export UPTIME_KUMA_USERNAME="{os.environ["UPTIME_KUMA_USERNAME"]}"\n',
        f'export UPTIME_KUMA_PASSWORD="{os.environ["UPTIME_KUMA_PASSWORD"]}"\n',
    ]

    # Remove old configuration lines from the .bashrc file
    with open(f"{home_dir}/.bashrc", "r") as f:
        bashrc_content = f.readlines()

    with open(f"{home_dir}/.bashrc", "w") as f:
        for line in bashrc_content:
            if not any(
                variable in line
                for variable in [
                    "UPTIME_KUMA_URL",
                    "UPTIME_KUMA_USERNAME",
                    "UPTIME_KUMA_PASSWORD",
                ]
            ):
                f.write(line)

        f.writelines(lines)

    # Source the updated .bashrc file to load the environment variables
    subprocess.run(f"source {home_dir}/.bashrc", shell=True, executable="/bin/bash")


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


def is_correct_credentials(api, user, password):
    try:
        api.login(user, password)
        api.disconnect()
        return True, None
    except UptimeKumaException as e:
        api.disconnect()
        return False, e
