"""route checker

Routing table check script intended for private network.

v1

fetch_data() to get show ip route from a remote device
target device and its device type, and credentials to use are hardcoded

additional module: netmiko
https://github.com/ktbyers/netmiko

v2

user input for the target destination and credentials

v3

use environment variables
NTA_TARGET=myrouter.example.com
NTA_USERNAME=myusername
NTA_PASSWORD=mypassword

v4

get environment variables from a file, route-checker.env

additional module: python-dotenv
https://github.com/theskumar/python-dotenv

v5

use arg to specify target device
"""

import logging
import logging.handlers

import argparse
import sys
import datetime
import json
import os

from netmiko import ConnectHandler
from netmiko.utilities import get_structured_data

from dotenv import load_dotenv


def logger_setup(options):
    # log file
    f_logfile = sys.argv[0].strip(".py$") + ".log"

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # configure file logging handler
    fh = logging.handlers.RotatingFileHandler(
        f_logfile,
        maxBytes=5000000,
        backupCount=7,
    )
    fh.setLevel(logging.DEBUG)

    # configure console logging handler
    ch = logging.StreamHandler()
    if options.debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # logging format
    # ref) https://docs.python.org/3/library/logging.html#logrecord-attributes
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add file logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def parse_options():
    # parser
    parser = argparse.ArgumentParser(
        add_help=True,
        description="DESCRIPTION",
    )

    # options
    parser.add_argument("--debug", "-d", action="store_true", default=False)
    parser.add_argument(
        "--test", action="store_true", help=argparse.SUPPRESS, default=False
    )
    parser.add_argument(
        "--fetch_data", action="store_true", help="Get show ip route output"
    )
    parser.add_argument(
        "--target",
        "-t",
        help="Target hostname or IP address",
    )

    # process args
    if len(sys.argv) > 1:
        args, unknown = parser.parse_known_args()
        return args, parser
    else:
        # print help and still proceed with --test and --debug
        parser.print_help()
        return sys.exit(1)


def fetch_data(options):
    # network device to access
    host = os.environ.get("NTA_TARGET")
    if options.target:
        host = options.target

    # credentials
    username = os.environ.get("NTA_USERNAME")
    password = os.environ.get("NTA_PASSWORD")

    logger.debug(f"Connecting to {username}:password_REDACTED@{host}")

    # device type
    # see CLASS_MAPPER_BASE in ssh_dispatcher.py
    # https://github.com/ktbyers/netmiko/blob/v4.3.0/netmiko/ssh_dispatcher.py
    device_type = "cisco_ios"

    target = {
        "host": host,
        "username": username,
        "password": password,
        "timeout": 7,
        "device_type": device_type,
    }

    with ConnectHandler(**target) as net_connect:
        logger.info(f"Connected to {host}")
        # prepare session
        net_connect.session_preparation()
        logger.debug("session_preparation() executed")

        # get timestamp
        timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d-%H%M%S")
        logger.debug(f"Timestamp to use is {timestamp}")
        # example) '20240404-052348'

        # show ip route, both raw and formatted
        # https://github.com/ktbyers/netmiko/issues/1332#issuecomment-673526976
        command = "show ip route"
        routes = net_connect.send_command_timing(command, use_textfsm=False)
        logger.debug(f"{command} executed and obtained the result")
        routes_json = get_structured_data(routes, platform=device_type, command=command)
        logger.debug("Parsed the raw result")

    # save the result in files
    filename = "-".join([host, timestamp]) + ".log"
    filename_json = "-".join([host, timestamp]) + ".json"

    with open(filename, "w") as salida:
        salida.write(routes)
        logger.info(f"Raw output saved in {filename}")

    with open(filename_json, "w") as salida:
        salida.write(json.dumps(routes_json, indent=2))
        logger.info(f"Parsed output saved in {filename_json}")

    return 0


def main():
    # environment variables
    basedir = os.path.abspath(os.path.dirname("."))
    load_dotenv(os.path.join(basedir, "route-checker.env"))

    if options.test:
        pass
    elif options.fetch_data:
        fetch_data(options)
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    options, parser = parse_options()
    logger = logger_setup(options)
    main()
