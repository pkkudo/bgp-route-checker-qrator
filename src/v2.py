"""version 2

Add console logging.
ref) https://docs.python.org/3/howto/logging.html
"""

import logging

# configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)
# create logger
logger = logging.getLogger(__name__)


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
    main()
