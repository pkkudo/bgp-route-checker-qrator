"""version 4

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
"""

import logging
import logging.handlers

import argparse
import sys


def logger_setup(options):
    # log file
    f_logfile = "v4.log"

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

    # process args
    if len(sys.argv) > 1:
        args, unknown = parser.parse_known_args()
        return args
    else:
        # print help and still proceed with --test and --debug
        parser.print_help()
        return sys.exit(1)


def main():
    if options.test:
        logging_test()

    if options.run:
        # run your main jobs
        pass

    return 0


if __name__ == "__main__":
    options = parse_options()
    logger = logger_setup(options)
    main()
