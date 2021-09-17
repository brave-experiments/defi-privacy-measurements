#!/usr/bin/env python3

import json
import os
import sys
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import publicsuffix2
import networkx as nx

# The Ethereum address of the MetaMask wallet that we used.
ETH_ADDR = "FDb672F061E5718eF0A56Db332e08616e9055548".lower()

# The ID of the MetaMask extension that we used.
EXT_ADDR = "bamklijogcfjklbogdbpkgfgnplalmdg"

# 1Inch's domains.
ONE_INCH_DOMAINS = ["1inch.exchange", "1inch.io"]
BALANCER_DOMAINS = ["balancer.fi", "balancer.finance"]

G = nx.DiGraph()
defi_nodes = set()
script_nodes = set()
edges = []
addr_leaks = {}

def log(msg):
    """Log the given message to stderr."""
    print("[+] " + msg, file=sys.stderr)

def parse_file(file_name):
    """Parse the given JSON file and return its content."""
    with open(file_name, "r") as fd:
        json_data = json.load(fd)
    return json_data

def get_etld1(url):
    """Return the given URL's eTLD+1."""
    fqdn = urlparse(url).netloc
    if "cloudflare" in fqdn:
        return "cloudflare"
    if "google" in fqdn or "gstatic" in fqdn:
        return "google"

    return publicsuffix2.get_sld(fqdn)


def get_script_hosts(reqs):
    hosts = set()
    for req in reqs:
        if req["type"] != "script":
            continue
        url = req["url"]
        if url == EXT_ADDR:
            continue
        hosts.add(get_etld1(url))
    return hosts


def parse_directory(directory):
    """Iterate over the given directory and parse its JSON files."""

    origin2deps = {}

    for file_name in os.listdir(directory):
        file_name = os.path.join(directory, file_name)
        if not os.path.isfile(file_name) or not file_name.endswith(".json"):
            log("Skipping {}; not a JSON file.".format(file_name))
            continue

        log("Parsing file: {}".format(file_name))
        json_data = parse_file(file_name)
        log("Extracted {} reqs from file: {}".format(
              len(json_data["requests"]), file_name))

        origin2deps[get_etld1(json_data["url"])] = get_script_hosts(json_data["requests"])

    return origin2deps


def calc_3p_presence(all_3ps, funnel, name):
    # Iterate over all third parties and see what fraction of each funnel they
    # observe, e.g. what percentage of each funnel does google.com see?
    third_party2pct = {}
    for third_party in all_3ps:
        num = 0
        for origin, origin_3ps in funnel.items():
            if third_party in origin_3ps:
                num += 1
        third_party2pct[third_party] = num/len(funnel.values())

    print("\n{} funnel:".format(name))
    for k, v in sorted(third_party2pct.items(), key = lambda kv:(kv[1], kv[0]), reverse=True):
        if v != 0:
            print("{}: {:.0%}".format(k, v))
    return {k: v for k, v in third_party2pct.items() if v > 0.01}


def intersect(top_funnel, middle_funnel, bottom_funnel):

    def flat(l):
        r = []
        for s in l:
            r += list(s)
        return r

    all_3ps = set()
    for third_party in flat(top_funnel.values()) + flat(middle_funnel.values()) + flat(bottom_funnel.values()):
        all_3ps.add(third_party)

    top3p2pct = calc_3p_presence(all_3ps, top_funnel, "top")
    mid3p2pct = calc_3p_presence(all_3ps, middle_funnel, "middle")
    bot3p2pct = calc_3p_presence(all_3ps, bottom_funnel, "bottom")

    for third_party in all_3ps:
        if third_party in top3p2pct.keys() and \
           third_party in mid3p2pct.keys() and \
           third_party in bot3p2pct.keys():
            print("{} present in at least 10\% of each funnel.".format(third_party))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: {} FUNNEL_DIR_1 FUNNEL_DIR_2 FUNNEL_DIR_3".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    top_funnel = parse_directory(sys.argv[1])
    middle_funnel = parse_directory(sys.argv[2])
    bottom_funnel = parse_directory(sys.argv[3])

    for domain, hosts in top_funnel.items():
        print("{} {}".format(domain, len(hosts)-1))
        #print(domain)
        #print(hosts)
        #print()

    # intersect(top_funnel, middle_funnel, bottom_funnel)
