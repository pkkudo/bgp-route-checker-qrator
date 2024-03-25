"""version 3

Add both console and file logging with file rotation.
ref) https://docs.python.org/3/howto/logging.html
ref) https://docs.python.org/3/howto/logging-cookbook.html#multiple-handlers-and-formatters
"""

import logging
import logging.handlers


def logger_setup():
    # log file
    f_logfile = "v3.log"

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # configure file logging handler
    fh = logging.handlers.RotatingFileHandler(
        f_logfile,
        maxBytes=5000,
        backupCount=7,
    )
    fh.setLevel(logging.DEBUG)

    # configure console logging handler
    ch = logging.StreamHandler()
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


def main():
    logging_test()

    return 0


if __name__ == "__main__":
    logger = logger_setup()
    main()
