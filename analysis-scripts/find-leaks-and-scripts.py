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
    return publicsuffix2.get_sld(fqdn)

def has_eth_addr(url):
    """Return True if the given URL contains our Ethereum address."""
    # TODO: Check for popular encodings.
    url = url.lower()
    return ETH_ADDR in url

def is_irrelevant(req):
    """Return True if the given request is irrelevant to our data analysis."""
    if EXT_ADDR in req["url"]:
        return True
    return False

def are_unrelated(domain, origin):
    """Return True if the two given domains are likely independent."""
    if domain in ONE_INCH_DOMAINS and origin in ONE_INCH_DOMAINS:
        return False
    if domain in BALANCER_DOMAINS and origin in BALANCER_DOMAINS:
        return False
    return domain != origin

def analyse_reqs(origin, reqs):
    """Analyze the given requests for the given origin."""
    script_domains = set()
    req_dst = {}
    leaks = {}
    origin = get_etld1(origin)
    log("Analyzing requests for origin: {}".format(origin))

    for req in reqs:
        if is_irrelevant(req):
            continue
        url = req["url"]
        domain = get_etld1(url)

        if req["type"] == "script" and domain != origin:
            G.add_node(domain)
            script_domains.add(domain)
            script_nodes.add(domain)
            edges.append(tuple([origin, domain]))

        if are_unrelated(domain, origin) and has_eth_addr(url):
            log("Found leak: {}".format(url))
            addr_leaks[origin] = addr_leaks.get(origin, 0) + 1

        req_dst[domain] = req_dst.get(domain, 0) + 1

    log("Sourced {} scripts from: {}".format(len(script_domains),
                                             script_domains))

def print_leaks():
    """Print the number of Ethereum address leaks per DeFi origin."""
    log("Number of 3rd party leaks per origin:")
    for origin, num_leaks in sorted(addr_leaks.items(),
                                    key=lambda x: x[1],
                                    reverse=True):
        print("{} & {} \\\\".format(origin, num_leaks))

def print_sourced_script_popularity():
    """Print the domains whose scripts are sourced by DeFi sites."""

    sorted_script_domains = sorted(script_nodes, key=lambda x:
                                   len([edge for edge in set(edges)]),
                                   reverse=True)
    log("# of embedded 3rd party domains: {}".format(len(sorted_script_domains)))
    for script_domain in sorted_script_domains:
        num = len([e for e in set(edges) if script_domain in e])
        print("{} & {} \\\\".format(script_domain, num))

    n = len(set([edge[0] for edge in edges]))
    log("# of DeFi sites that embed at least one script: {} ({:.0%})".format(
        n, n / len(defi_nodes)))

    # Find all edges that point to Google.
    n = len(set([edge[0] for edge in edges if "google" in edge[1]]))
    log("# of DeFi sites that embed Google scripts: {} ({:.0%})".format(
        n, n / len(defi_nodes)))

def create_connectivity_graph():
    """Create a connectivity graph of DeFi sites and their sourced scripts."""
    pos = nx.bipartite_layout(G, defi_nodes, align="horizontal")
    options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
    nx.draw_networkx_nodes(G, pos, nodelist=list(defi_nodes), node_color="tab:blue", **options)
    nx.draw_networkx_nodes(G, pos, nodelist=script_nodes, node_color="tab:red", **options)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.3, edge_color="tab:gray")

    labels = {key: key for key in defi_nodes}
    text = nx.draw_networkx_labels(G, pos, labels, font_size=22)
    for _, t in text.items():
        t.set_rotation('vertical')

    labels = {key: key for key in script_nodes}
    text = nx.draw_networkx_labels(G, pos, labels, font_size=22)
    for _, t in text.items():
        t.set_rotation('vertical')

    plt.tight_layout()
    plt.show()

def parse_directory(directory):
    """Iterate over the given directory and parse its JSON files."""
    for file_name in os.listdir(directory):
        file_name = os.path.join(directory, file_name)
        if not os.path.isfile(file_name) or not file_name.endswith(".json"):
            log("Skipping {}; not a JSON file.".format(file_name))
            continue

        log("Parsing file: {}".format(file_name))
        json_data = parse_file(file_name)
        log("Extracted {} reqs from file: {}".format(
              len(json_data["requests"]), file_name))

        # Add DeFi site as new node to dependency graph.

        defi_domain = get_etld1(json_data["url"])
        G.add_node(defi_domain)
        defi_nodes.add(defi_domain)

        analyse_reqs(json_data["url"], json_data["requests"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} DIRECTORY".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    parse_directory(sys.argv[1])

    # create_connectivity_graph()
    print_leaks()
    print_sourced_script_popularity()
