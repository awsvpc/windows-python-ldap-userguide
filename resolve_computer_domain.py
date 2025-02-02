#!/usr/bin/env python
# resolve domain computers by @3xocyte

import argparse
import sys
import string

# requires dnspython and ldap3
import dns.resolver
from ldap3 import Server, Connection, NTLM, ALL, SUBTREE

def resolve(nameserver, host_fqdn):
    resolver = dns.resolver.Resolver();
    resolver.nameservers = [nameserver]
    answer = resolver.query(host_fqdn, "A")
    return answer

def get_domain_dn(domain):
    base_dn = ''
    domain_parts = domain.split('.')
    for i in domain_parts:
        base_dn += 'DC=%s,' % i
    base_dn = base_dn[:-1]
    return base_dn

def ldap_login(dc_ip, username, password, ssl, domain):
    if ssl == True:
        s = Server(dc_ip, port = 636, use_ssl = True, get_info=ALL)
    else:
        s = Server(dc_ip, get_info=ALL)
    domain_user = "%s\\%s" % (domain, username)
    try:
        c = Connection(s, user = domain_user, password = password, authentication=NTLM)
        if c.bind() != True:
            print "[!] unable to bind"
            sys.exit()
    except Exception, e:
        print "[!] unable to connect, exception: %s" % str(e)
        sys.exit()
    return c

def get_computers(ldap_connection, domain, dns_ip, dc_ip):
    dn = get_domain_dn(domain)
    filter = "(samAccountType=805306369)" # or (objectCategory=computer)
    try:
        ldap_connection.search(search_base=dn, search_filter=filter, search_scope=SUBTREE, attributes=['dnsHostName'])
        for entry in ldap_connection.entries:
            computer = str(entry['dNSHostName'])
            try:
                answer = ''
                result = resolve(dns_ip, computer)
                for i in result:
                    result_string = ''.join([str(i), answer])
                    print '%s\t%s' % (result_string, computer)
            except Exception as e:
                # failed to resolve the hostname so no need to pollute the file
                pass

    except Exception, e:
        print "[!] exception raised: %s" % str(e)
        ldap_connection.unbind()
        sys.exit()

def main():
    parser = argparse.ArgumentParser(add_help = True, description = "script to produce /etc/hosts entries for domain-joined computers (requires valid domain credentials and an IP address for a DC acting as a DNS server)")
    parser.add_argument('-d', '--domain', action="store", default='', help='valid fully-qualified domain name', required=True)
    parser.add_argument('-u', '--username', action="store", default='', help='valid username', required=True)
    parser.add_argument('--ssl', action="store_true", default=False, help="connect to ldap over SSL")
    password_or_ntlm = parser.add_mutually_exclusive_group(required=True)
    password_or_ntlm.add_argument('-p', '--password', action="store", default='', help='valid password')
    password_or_ntlm.add_argument('-n', '--nthash', action="store", default='', help='valid nt hash (32 hex chars)')
    parser.add_argument('target_dc', help='ip address or hostname of DC')
    parser.add_argument('dns_ip', help='ip address or hostname of DNS server')
    options = parser.parse_args()

    domain = options.domain
    username = options.username
    password = options.password
    nthash = options.nthash
    dc_ip = options.target_dc
    ssl = options.ssl
    dns_ip = options.dns_ip

    if nthash:
        password = '00000000000000000000000000000000:%s' % nthash

    ldap_connection = ldap_login(dc_ip, username, password, ssl, domain)
    computer_results = get_computers(ldap_connection, domain, dns_ip, dc_ip)

if __name__ == '__main__':
    main()
