"""BGP route checker

This script uses Qrator API publicly available to check the BGP path data for a given CIDR
and logs origin ASN and peering ASN on console and file.

The response json data from Qrator will be saved in a file with CIDR and timestamp in its filename.

ref) https://radar.qrator.dev/open-api
"""

import logging
import logging.handlers

import argparse
import sys

import ipaddress

from datetime import datetime

import urllib.request
import json
from collections import Counter


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
        description="BGP route checker for a given CIDR using Qrator API",
    )

    # options
    parser.add_argument("--debug", "-d", action="store_true", default=False)
    parser.add_argument(
        "--test", action="store_true", help=argparse.SUPPRESS, default=False
    )
    parser.add_argument("--cidr", help="IPv4 CIDR to check")

    # process args
    if len(sys.argv) > 1:
        args, unknown = parser.parse_known_args()
        return args, parser
    else:
        # print help and still proceed with --test and --debug
        parser.print_help()
        return sys.exit(1)


def validate_ipv4network(cidr):
    try:
        check_cidr = ipaddress.IPv4Network(cidr)
        logger.debug(f"{cidr} is valid IPv4 network")
        if check_cidr.is_private:
            logger.info("The CIDR is on private IP range. Exiting.")
            sys.exit(0)
        if "/" not in cidr:
            logger.warning(
                f"Using {cidr}/32 as no prefix was given in the cidr argument"
            )
            cidr = cidr + "/32"
            logger.error("This script won't check BGP route with /32 netmask. Exiting")
            sys.exit(1)
    except ValueError:
        logger.error(
            f"Expecting IPv4 prefix like 10.0.0.0/24. String given is {cidr}. Exiting."
        )
        sys.exit(1)

    return cidr


def bgp_path_checker_qrator(cidr):
    # replace "/" with "%2F"
    cidr_q = cidr.replace("/", "%2F")

    # set url
    url = f"https://new-api.radar.qrator.net/v1/get-all-paths?prefix={cidr_q}"
    logger.debug(f"Qrator API URL to use is {url}")

    # timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # get response from Qrator api
    with urllib.request.urlopen(url) as r:
        # response code
        if r.code != 200:
            logger.error(f"Failed to receive response from {url}")
            sys.exit(1)
        logger.info(f"Received response from {url}")

        # headers
        ct = r.getheader("content-type")
        length = r.getheader("content-length")
        logger.debug(f"Received {length} bytes of {ct} data in response")

        # load data
        data = json.loads(r.read())

        # saving the data with timestamp in the filename
        filename = "qrator-" + cidr.replace("/", "-") + "-" + timestamp + ".json"
        with open(filename, "w") as salida:
            salida.write(json.dumps(data, indent=2))
            logger.info(f"Saved the obtained data in {filename}")

    # exit if no data found
    if cidr not in data["data"].keys():
        logger.info(
            "The given CIDR was not found. See IRR/WHOIS/RADB/etc. and try different prefix. Exiting."
        )
        sys.exit(0)

    # passing over only paths data
    paths = data["data"][cidr]

    return paths


def origin_check(paths, cidr):
    """Go through the ASN paths to check origin ASN"""
    logger.debug(f"Processing {type(paths)} with {len(paths)} items.")

    # origin check
    lst_origin_asn = []
    # for each path observed by Qrator
    for path in paths:
        # split comma-delimited ASN list
        asns = path.split(",")

        # the last entry is the origin
        lst_origin_asn.append(asns[-1])

    # confirm the unique origin ASN observed
    origin = set(lst_origin_asn)
    logger.info(f"ASN {origin} for {cidr}")

    # get counter to show summary if there is more than one origin ASN observed
    c = Counter(lst_origin_asn)
    if len(origin) != 1:
        logger.warning(
            f"Multiple origin ASN observed. ASN and its occurrence: {c.most_common()}"
        )

    # pick the origin, the one with most occurrence if there are multiple
    origin_asn = c.most_common()[0][0]

    return origin_asn


def peer_check(paths, origin_asn):
    """Go through the ASN paths to check the neighboring ASNs"""
    peers = []
    for path in paths:
        # split comma-delimited ASN list
        asns = path.split(",")

        # exclude origin asn from the list
        while asns.count(origin_asn):
            asns.remove(origin_asn)

        # the last ASN from the list with origin ASN removed
        # is the peer BGP ASN
        peers.append(asns[-1])

    # generate the counter and log summary of the peer ASNs
    c = Counter(peers)
    logger.info(f"Summary of peer ASNs: {c.most_common()}")

    # peers with path-prepend
    peers_pathprepend = []
    for path in paths:
        asns = path.split(",")
        if asns.count(origin_asn) > 1:
            while asns.count(origin_asn):
                asns.remove(origin_asn)
            peers_pathprepend.append(asns[-1])
    c = Counter(peers_pathprepend)
    logger.info(f"Summary of peer ASNs with path-prepend at origin: {c.most_common()}")

    return 0


def main():
    if options.cidr:
        cidr = options.cidr
        cidr = validate_ipv4network(cidr)
        paths = bgp_path_checker_qrator(cidr)
        origin_asn = origin_check(paths, cidr)
        peer_check(paths, origin_asn)
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    options, parser = parse_options()
    logger = logger_setup(options)
    main()
