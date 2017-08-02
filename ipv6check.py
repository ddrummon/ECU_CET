#!/usr/bin/env python
#
# ipv6check.py: This is small python program to check the existence
# of an AAAA DNS record for a qualified domain name.
#
# TODO: Add CLI flags so we are able to pass in input and output filenames
# TODO: Add IPv4 lookup and reporting
#

import datetime
import dns.resolver
from optparse import OptionParser


dns_resolver = dns.resolver.Resolver()
dns_resolver.nameservers = [
                            '10.100.0.2',
#                            '8.8.8.8'
                            ]

def ipv6check(infile='domains.txt', outfile='domains.csv'):
    # Set some variables so we can get some statistics
    v6 = 0
    no_v6 = 0
    no_ns = 0
    dns_timeout = 0
    domain_ct = 0
    invalid = 0

    with open(infile, 'r') as f:
        domains = ["www." + line.lower().rstrip() for line in f]

    with open(outfile, 'a') as fout:
        fout.write("{0},{1},{2}\n".format("Count","Domain","IPv6 Response"))
        for domain in domains:
            try:
                idx = 0
                domain_ct += 1
                answers = dns_resolver.query(domain, 'AAAA')
                for rdata in answers:
                    while idx == 0:
                        print("{0:6} {1:45}: {2}".format(domain_ct, domain, rdata))
                        fout.write("{0},{1},{2}\n".format(domain_ct, domain, rdata))
                        v6 += 1
                        idx += 1
            except dns.resolver.NoAnswer:
                print("{0:6} {1:45}: No IPv6 Address for domain.".format(domain_ct, domain))
                fout.write("{0},{1},No IPv6 address for domain.\n".format(domain_ct, domain))
                no_v6 += 1
            except dns.resolver.NXDOMAIN:
                print("{0:6} {1:45}: Not a valid domain.".format(domain_ct, domain))
                fout.write("{0},{1},Not a valid domain.\n".format(domain_ct, domain))
                invalid += 1
            except dns.resolver.NoNameservers:
                print("{0:6} {1:45}: No Name Servers for domain.".format(domain_ct, domain))
                fout.write("{0},{1},No Name Servers for domain.\n".format(domain_ct, domain))
                no_ns += 1
            except dns.exception.Timeout:
                print("{0:6} {1:45}: DNS Query Timed Out.".format(domain_ct, domain))
                fout.write("{0},{1},DNS Query Timed Out.\n".format(domain_ct, domain))
                dns_timeout += 1

    print("\nDomains with an IPv6 Address: {0}".format(v6))
    print("Domains with no IPv6 Address: {0}".format(no_v6))
    print("Domains with no nameservers: {0}".format(no_ns))
    print("Domains that timedout on query: {0}".format(dns_timeout))
    print("Domains that are not valid: {0}".format(invalid))
    print("Total Domains queried: {0}".format(v6 + no_v6 + no_ns + invalid + dns_timeout))

if __name__ == "__main__":
    """parser = OptionParser()
    parser.add_option('-i', '--infile', dest="infile", action="store", help="File containing a list of domain names.")
    parser.add_option('-o', '--outfile', dest="outfile", action="store", help="File with results of lookup, CSV format.")
    parser.add_option('-d', '--display', dest="display", action="store_true", help="show all emails")
    (options, args) = parser.parse_args()

    # validation
    if options.action and not options.email:
        parser.error("option -a requires option -e")
    elif options.email and not options.action:
        parser.error("option -e requires option -a")
    try:
        print(main(options)[1])
    except InvalidEmail:
        parser.error("option -e requires a valid email address")"""
    ipv6check()




