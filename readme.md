# BGP route checker

A simple python script to check origin and peering ASN for a given CIDR using [Qrator API](https://radar.qrator.dev/open-api) and logs the summary in console and file, and saves the response data in a file.

Scripts are in `./src/` and `./src/v*.py` files are there to go over some python basics with my network engineer buddies.

```shell
cd src
python bgp-route-checker.py -h
python bgp-route-checker.py --cidr 10.0.0.0/8  # replace 10.0.0.0/8 with ipv4 public cidr you wish to check
```
