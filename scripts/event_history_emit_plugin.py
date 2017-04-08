#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#

"""
sensu api metric pusher

Prequisite:
    1) Update Sensu API Hosts
    2) Sensu Port
"""

import requests
import argparse

from collections import defaultdict

# Servers running Sensu API
_sensu_api_hosts = ['host1', 'host2']
# Sensu API Port
api_port = str(4567)


def check_api(sensu_api_host_list):
    for host in sensu_api_host_list:
        url = 'http://'+host+':'+api_port
        # print url
        reach = requests.get(url+'/info')
        if reach.status_code == 200:
            return url


def get_api_data(sensu_api_host, end_point):
    _url = check_api(sensu_api_host)+'/'+end_point
    try:
        if _url:
            return requests.get(_url).json()
    except:
        print "can't find data"


def get_clients_list(sensu_api_host, end_point):
    _json_data = sorted(set([k.get('name') for k in
                             get_api_data(sensu_api_host, end_point)
                             for i, j in k.items()]))
    return _json_data


def get_metric_check(sensu_api_hosts, host, check_name):
    _end_point = 'results'+'/'+host+'/'+check_name
    _get_data = get_api_data(sensu_api_hosts, _end_point)
    metric_to_emit = _get_data.get('client').split('.')[0]+'.'+_get_data.get('check').get('name')+'.check'
    issued = _get_data.get('check').get('issued')
    status = _get_data.get('check').get('status')
    return [metric_to_emit, status, issued]


def main():
    parser = argparse.ArgumentParser(description="\033[1;34mCheck Metric Emitter\033[1;m")
    parser.add_argument("-H", "--host", required=True,
                        help="Hostname with example.com to check for metric value")
    parser.add_argument("-c", "--check", required=True,
                        help="metric name to check in Sensu API")
    args = parser.parse_args()

    if args.host and args.check:
        if args.host.split('.')[-1] != 'com':
            print "Please enter hostname with FQDN. e.g. host1.example.com"
        else:
            try:
                meta = get_metric_check(_sensu_api_hosts, args.host, args.check)
                print ' '.join(str(i) for i in meta)
            except:
                print "\033[1;34mCheck metric name in Sensu API\033[1;m"



if __name__ == "__main__":
    main()
