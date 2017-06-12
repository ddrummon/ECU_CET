#!/usr/bin/env python
#
# ipv6check.py: This is small python program to check the existance
# of a AAAA DNS record for a qualified domain name.


import os, sys, time, csv
import dns.message, dns.query, dns.resolver

DNSSERVERS = [
    ("Google", "8.8.8.8"),
    ]

RETRIES=3
TIMEOUT=3

# List of DNS names to test for presence of AAAA records
sitenames = [
    "www.bing.com.",
    "www.netflix.com.",
    ]


"""
"wwww.google.com",
"www.netflix.com.",
"""
yes_v6 = 0
no_v6 = 0
no_resp = 0

# Read csv in as a list LARGE list.
# TODO: convert this to a database where we can store the domains and the results
"""
with open('domains.txt', 'r') as f:
    sitenames = ["www." + line.lower().rstrip() for line in f]
#    sitenames = [line.lower().rstrip() for line in f]

print(sitenames)
"""

def send_query_udp(qname, res_name, res_ip, timeout, retries):
    gotresponse = False
    res = None
    msg = dns.message.make_query(qname, dns.rdatatype.AAAA)
    while (not gotresponse and (retries > 0)):
        retries -= 1
        try:
            ## print "DEBUG: query %s %s" % (res_ip, qname)
            res = dns.query.udp(msg, res_ip, timeout=timeout)
            gotresponse = True
        except dns.exception.Timeout:
            pass
    return res

for res_name, resp_ip in DNSSERVERS:
    for qname in sitenames:
        for rdata in dns.resolver.query(qname, 'AAAA'):
            if rdata == KeyError:
                print("{0}:{1} -> {2} DNS query timed out".format(res_name, res_ip, qname))
                continue
            elif rdata == dns.resolver.NoAnswer:
                print("{0}:{1} -> {2} No AAAA record returned".format(res_name, res_ip, qname))
                continue
            else:
                print("{0}:{1} -> {2} -> {3}".format(res_name, resp_ip, qname, rdata))

"""
for res_name, resp_ip in DNSSERVERS:
    for qname in sitenames:
        for rdata in dns.resolver.query(qname, 'AAAA'):
            if rdata is KeyError:
                print("{0}:{1} -> {2} DNS query timed out".format(res_name, res_ip, qname))
            elif rdata.address is dns.resolver.NoAnswer:
                print("{0}:{1} -> {2} DNS query timed out".format(res_name, res_ip, qname))
            else:
                print("{0}:{1} -> {2} -> {3}".format(res_name, resp_ip, qname, rdata.address))
"""
"""
for res_name, res_ip in DNSSERVERS:
    for qname in sitenames:
        res = send_query_udp(qname, res_name, res_ip, TIMEOUT, RETRIES)
        if res == None:
            rc = 1
            print("{0}:{1} -> {2} DNS query timed out".format(res_name, res_ip, qname))
            no_resp += 1
            continue
        for rrset in res.answer:
            #print(res)
            if rrset.rdtype == 28:             # RR type code for AAAA
                print("{0}:{1} -> {2} AAAA Record : {3}".format(res_name, res_ip, qname, res.answer))
                yes_v6 += 1
                break
        else:
            rc = 1
            print("{0}:{1} -> {2} No AAAA record returned".format(res_name, res_ip, qname))
            no_v6 += 1
"""
print("Number of sites with AAAA record: {0}".format(yes_v6))
print("Number of sites without  AAAA record: {0}".format(no_v6))
print("Number of sites with no DNS response: {0}".format(no_resp))
print("Total number of sites queried: {0}".format(yes_v6 + no_v6 + no_resp))

