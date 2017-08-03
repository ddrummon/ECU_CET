#!/usr/bin/env python3
#
# ipv6check.py: This is small python program to check the existence
# of an AAAA DNS record for a qualified domain name.
#
# TODO: Add function to fetch the current .gov domain list from data.gov
# TODO: Add authoritative lookup logic
# TODO: Add IPv4 lookup and reporting
#

import argparse
import csv
import datetime
import dns.resolver
from time import sleep

def parse_arguments():

    filetime = datetime.datetime.now().strftime("%Y%m%d-%H%M")

    parser = argparse.ArgumentParser(description='IPv6 Record Check for list of domains.',
                                     add_help=True)
    parser.add_argument("-i", "--infile",
                      action="store",
                      dest="infile",
                      default="domains.csv",
                      help="input file to read list of domains from. In CSV format. Default is domains.csv")
    parser.add_argument("-o", "--outfile",
                      action="store",
                      dest="outfile",
                      default="domains-ipv6-" + filetime + ".csv",
                      help="output file to write IPv6 information to. In CSV format. Default is domains-ipv6-YYYYMMDD-HHmm.csv")
    parser.add_argument("-r", "--resolver",
                        action="store",
                        dest="resolver",
                        default='8.8.8.8',
                        help="DNS Server to query.")
    parser.add_argument("-d", "--display",
                        action="store_true",
                        dest="display",
                        default=False,
                        help="Print results to screen.")
    parser.add_argument("-v", "--version",
                        action="version",
                        version="%(prog)s BETA")
    args = parser.parse_args()
    return args

def get_domains(infile):
    with open(infile, 'r') as fin:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(fin)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value.lower())
                except KeyError:
                    data[header] = [value.lower()]
    domains = data['Domain Name']
    return domains

def ipv6check(outfile, resolver, display, domains):
    # Set some variables so we can get some statistics
    v6 = 0
    no_v6 = 0
    no_ns = 0
    dns_timeout = 0
    domain_ct = 0
    invalid = 0

    dns_resolver = dns.resolver.Resolver()
    dns_resolver.nameservers = [resolver]

    l = len(domains)


    with open(outfile, 'a') as fout:
        fout.write("{0},{1},{2}\n".format("Count","Domain","IPv6 Response"))
        printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
        for i, domain in enumerate(domains):
            fqdn = "www." + str(domain)
            try:
                idx = 0
                domain_ct += 1
                answers = dns_resolver.query(fqdn, 'AAAA')
                for rdata in answers:
                    while idx == 0:
                        if display is True:
                            print("{0:6} {1:45}: {2}".format(domain_ct, fqdn, rdata))
                            fout.write("{0},{1},{2}\n".format(domain_ct, fqdn, rdata))
                        else:
                            fout.write("{0},{1},{2}\n".format(domain_ct, fqdn, rdata))
                        v6 += 1
                        idx += 1
            except dns.resolver.NoAnswer:
                if display is True:
                    print("{0:6} {1:45}: No IPv6 Address for domain.".format(domain_ct, fqdn))
                    fout.write("{0},{1},No IPv6 address for domain.\n".format(domain_ct, fqdn))
                else:
                    fout.write("{0},{1},No IPv6 address for domain.\n".format(domain_ct, fqdn))
                no_v6 += 1
            except dns.resolver.NXDOMAIN:
                if display is True:
                    print("{0:6} {1:45}: Not a valid domain.".format(domain_ct, fqdn))
                    fout.write("{0},{1},Not a valid domain.\n".format(domain_ct, fqdn))
                else:
                    fout.write("{0},{1},Not a valid domain.\n".format(domain_ct, fqdn))
                invalid += 1
            except dns.resolver.NoNameservers:
                if display is True:
                    print("{0:6} {1:45}: No Name Servers for domain.".format(domain_ct, fqdn))
                    fout.write("{0},{1},No Name Servers for domain.\n".format(domain_ct, fqdn))
                else:
                    fout.write("{0},{1},No Name Servers for domain.\n".format(domain_ct, fqdn))
                no_ns += 1
            except dns.exception.Timeout:
                if display is True:
                    print("{0:6} {1:45}: DNS Query Timed Out.".format(domain_ct, fqdn))
                    fout.write("{0},{1},DNS Query Timed Out.\n".format(domain_ct, fqdn))
                else:
                    fout.write("{0},{1},DNS Query Timed Out.\n".format(domain_ct, fqdn))
                dns_timeout += 1
            sleep(0.1)
            # Update Progress Bar
            printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

    print("\nDomains with an IPv6 Address: {0}".format(v6))
    print("Domains with no IPv6 Address: {0}".format(no_v6))
    print("Domains with no nameservers: {0}".format(no_ns))
    print("Domains that timedout on query: {0}".format(dns_timeout))
    print("Domains that are not valid: {0}".format(invalid))
    print("Total Domains queried: {0}".format(v6 + no_v6 + no_ns + invalid + dns_timeout))

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()



if __name__ == "__main__":
    args = parse_arguments()
    ipv6check(args.outfile, args.resolver, args.display, get_domains(args.infile))



