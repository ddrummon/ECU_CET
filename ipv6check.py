#!/usr/bin/env python
#
# ipv6check.py: This is small python program to check the existence
# of an AAAA DNS record for a qualified domain name.


import dns.resolver
import datetime

dns_resolver = dns.resolver.Resolver()
dns_resolver.nameservers = ['8.8.8.8']

v6 = 0
no_v6 = 0
no_ns = 0
dns_timeout = 0
domain_ct = 0

fn = "ipv6-domains_20170729-1523.txt"

with open('domains.txt', 'r') as f:
    domains = ["www." + line.lower().rstrip() for line in f]

for domain in domains:
    try:
        idx = 0
        domain_ct += 1
        answers = dns_resolver.query(domain, 'AAAA')
        for rdata in answers:
            while idx == 0:
                print("{0:6} {1:45}: {2}".format(domain_ct, domain, rdata))
                with open(fn, 'a') as f:
                    f.write(domain + "\n")
                v6 += 1
                idx += 1
    except dns.resolver.NoAnswer:
        print("{0:6} {1:45}: No IPv6 Address for domain.".format(domain_ct, domain))
        no_v6 += 1
    except dns.resolver.NXDOMAIN:
        print("{0:6} {1:45}: Not a valid domain.".format(domain_ct, domain))
        invalid += 1
    except dns.resolver.NoNameservers:
        print("{0:6} {1:45}: No Name Servers for domain.".format(domain_ct, domain))
        no_ns += 1
    except dns.exception.Timeout:
        print("{0:6} {1:45}: DNS Query Timed Out.".format(domain_ct, domain))
        dns_timeout += 1

print("\nDomains with an IPv6 Address: {0}".format(v6))
print("Domains with no IPv6 Address: {0}".format(no_v6))
print("Domains with no nameservers: {0}".format(no_ns))
print("Domains that timedout on query: {0}".format(dns_timeout))
print("Total Domains queried: {0}".format(v6 + no_v6 + no_ns + dns_timeout))



