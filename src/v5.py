"""version 5

v3

Add both console and file logging with file rotation.
ref) https://docs.python.org/3/howto/logging.html
ref) https://docs.python.org/3/howto/logging-cookbook.html#multiple-handlers-and-formatters

v4

Use argparse to use arguments.
ref) https://docs.python.org/3/library/argparse.html

python v4.py  # prints argparse help
python v4.py --test  # runs logging test
python v4.py --test -d  # sets debug level console logging

v5

Pass CIDR using argparse and check if the given CIDR is valid IPv4 Network
ref) https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network
"""

import logging
import logging.handlers

import argparse
import sys

import ipaddress


def logger_setup(options):
    # log file
    f_logfile = "v5.log"

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


def logging_test():
    logger.info("info level logging")
    logger.error("error message")
    logger.debug("debug message")
    logger.warning("warning")

    return 0


def parse_options():
    # parser
    parser = argparse.ArgumentParser(
        add_help=True,
        description="ENTER_SCRIPT_DESCRIPTION_HERE",
    )

    # options
    parser.add_argument("--debug", "-d", action="store_true", default=False)
    parser.add_argument(
        "--test", action="store_true", help=argparse.SUPPRESS, default=False
    )
    parser.add_argument("--run", action="store_true", help="Run the script")
    parser.add_argument("--cidr", help="IPv4 CIDR to check")

    # process args
    if len(sys.argv) > 1:
        args, unknown = parser.parse_known_args()
        return args
    else:
        # print help and still proceed with --test and --debug
        parser.print_help()
        return sys.exit(1)


def validate_ipv4network(cidr):
    try:
        ipaddress.IPv4Network(cidr)
        logger.debug(f"{cidr} is valid IPv4 network")
        if "/" not in cidr:
            logger.warning(
                f"Using {cidr}/32 as no prefix was given in the cidr argument"
            )
            cidr = cidr + "/32"
    except ValueError:
        logger.error(
            f"Expecting IPv4 prefix like 10.0.0.0/24. String given is {cidr}. Exiting."
        )
        sys.exit(1)

    return cidr


def main():
    if options.test:
        logging_test()

    if options.cidr:
        cidr = options.cidr
        cidr = validate_ipv4network(cidr)

    if options.run:
        # run your main jobs
        pass

    return 0


if __name__ == "__main__":
    options = parse_options()
    logger = logger_setup(options)
    main()
