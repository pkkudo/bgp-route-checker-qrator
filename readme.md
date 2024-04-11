# BGP route checker

A simple python script to check origin and peering ASN for a given CIDR using [Qrator API](https://radar.qrator.dev/open-api) and logs the summary in console and file, and saves the response data in a file.

Scripts are in `./src/` and `./src/v*.py` files are there to go over some python basics with my network engineer buddies.

```shell
cd src
python bgp-route-checker.py -h
python bgp-route-checker.py --cidr 10.0.0.0/8  # replace 10.0.0.0/8 with ipv4 public cidr you wish to check
```

No additional packages to install using poetry/pip. (Mar 2024) Confirmed on python@3.12.2 and also on [python@3.8.19 which is almost reaching eol](https://devguide.python.org/versions/).

# example

```shell
# run
$ cd src
$ python bgp-route-checker.py --cidr 111.98.0.0/16
2024-04-11 12:34:38,560 INFO Received response from https://new-api.radar.qrator.net/v1/get-all-paths?prefix=111.98.0.0%2F16
2024-04-11 12:34:38,561 INFO Saved the obtained data in qrator-111.98.0.0-16-20240411-123435.json
2024-04-11 12:34:38,561 INFO ASN {'2516'} for 111.98.0.0/16
2024-04-11 12:34:38,561 INFO Summary of peer ASNs: [('1299', 105), ('3356', 74), ('174', 54), ('6762', 32), ('3257', 24), ('6939', 14), ('3491', 11), ('4230', 10), ('6461', 7), ('3320', 6), ('4637', 4), ('1273', 4), ('2914', 4), ('6830', 3), ('35280', 3), ('12389', 3), ('60068', 2), ('15412', 2), ('6453', 2), ('137409', 2), ('3549', 2), ('17676', 2), ('7473', 1), ('199524', 1), ('4134', 1), ('7922', 1), ('8966', 1), ('8928', 1), ('4788', 1), ('3303', 1), ('37271', 1), ('41095', 1), ('58453', 1), ('49544', 1), ('7843', 1), ('2518', 1), ('2497', 1), ('2907', 1)]
2024-04-11 12:34:38,561 INFO Summary of peer ASNs with path-prepend at origin: []

# raw data saved in a file
$ cat qrator-111.98.0.0-16-20240411-123435.json
{
  "meta": {
    "status": "success",
    "code": 200
  },
  "data": {
    "111.98.0.0/16": [
      "1003,12186,32097,1299,2516",
      "11039,6461,2516",
      "11071,3356,2516",
......
      "8893,1299,2516",
      "8926,3356,2516",
      "9002,3257,2516",
      "924,6939,2516",
      "955,6939,2516",
      "9902,1299,2516",
      "9902,3491,2516"
    ]
  }
}
```
