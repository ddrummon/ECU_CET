#!/usr/bin/env python

import socket

#domains = ("www.google.com", "www.facebook.com", "www.amazon.com", "test.test")

yes_v6 = 0
yes_v4 = 0
no_v6 = 0
no_v4 = 0
no_resp = 0
domainct = 0

with open('domains.txt', 'r') as f:
    domains = ["www." + line.lower().rstrip() for line in f]
#    domains = [line.lower().rstrip() for line in f]

print("-" * 153)
print(": {0:^6} : {1:45} : {2:45} : {3:45}:".format("Count", "Domain", "IPv6 Address", "IPv4 Address"))
print("-" * 153)
for domain in domains:
    try:
        domainct +=1
        alladdr = socket.getaddrinfo(domain, None)
        af_inet6 = filter(lambda x: x[0] == socket.AF_INET6, alladdr)
        af_inet = filter(lambda x: x[0] == socket.AF_INET, alladdr)
        ipv4 = list(af_inet)[0][4][0]
        ipv6 = list(af_inet6)[0][4][0]
        if ipv6 is not None and ipv4 is not None:
            yes_v6 +=1
            yes_v4 +=1
            print(": {0:^6} : {1:45} : {2:45} : {3:45}:".format(domainct, domain, ipv6, ipv4))
    except IndexError:
        no_v6 += 1
        print(": {0:^6} : {1:45} : {2:45} : {3:45}:".format(domainct, domain, "NONE", ipv4))
    except socket.gaierror:
        no_resp +=1
        print(": {0:^6} : {1:45} : {2:45} : {3:45}:".format(domainct, domain, "No response or invalid domain",
                                                "No response or invalid domain"))

print("-" * 153)
print(": {0:36} : {1:<111}:".format("Number of sites with INET6 record", yes_v6))
print(": {0:36} : {1:<111}:".format("Number of sites without INET6 record", no_v6))
print(": {0:36} : {1:<111}:".format("Number of sites with INET record", yes_v4))
print(": {0:36} : {1:<111}:".format("Number of sites without INET record", no_v4))
print(": {0:36} : {1:<111}:".format("Number of sites with no DNS response", no_resp))
print(": {0:36} : {1:<111}:".format("Total number of sites queried", (yes_v6 + no_v6 + no_resp)))
print("-" * 153)
