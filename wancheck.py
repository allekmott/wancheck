"""wancheck

Simple script to periodically check to see if a machine's external IP has
changed
"""

import sys
import time

import dns.message
import dns.opcode
import dns.rdatatype
import dns.rdataclass
import dns.query

VERSION = str("0.0.1")

_CHECK_INTERVAL = 10

_LOOKUP_DOMAIN = "myip.opendns.com"
_RESOLVER_DOMAIN = "resolver1.opendns.com"

def ip_lookup(domain, nameserver_ip="8.8.8.8"):
	"""Run DNS lookup against domain, return first result or None"""
	query_message = dns.message.make_query(
			qname=domain,
			rdtype=dns.rdatatype.A,
			rdclass=dns.rdataclass.IN,

			use_edns=None,
			want_dnssec=False,
			ednsflags=0,
			payload=0,

			request_payload=None,
			options=None)

	query_response = dns.query.udp(
			q=query_message,
			af=None,
			where=nameserver_ip,
			port=53,
			timeout=2,

			# source="", ???
			# source_port=0,

			ignore_unexpected=False,
			one_rr_per_rrset=True
			)

	query_answers = query_response.answer

	ip_address = None
	for answer in query_answers:
		ipv4_records = \
				filter(lambda r: r.rdtype == dns.rdatatype.A, answer.items)

		if len(ipv4_records):
			ip_address = ipv4_records[0].address
			break

	return ip_address

def alert(ip):
	pass

def main():
	print("wancheck v%s\n" % (VERSION))

	try:
		resolver_ip = ip_lookup(_RESOLVER_DOMAIN)
	except Exception as e:
		print("Unable to look up resolver IP: %s" % (e))
		return

	print("using resolver '%s' (%s)" % (_RESOLVER_DOMAIN, resolver_ip))
	print("using lookup domian '%s'" % (_LOOKUP_DOMAIN))

	ip_lastest = None
	while True:
		try:
			ip = ip_lookup(_LOOKUP_DOMAIN, resolver_ip)
		except Exception as e:
			if hasattr(e, "errno") and type(e.errno) is int:
				sys.stderr.write("E%i" % (e.errno))
			else:
				sys.stderr.write("E")

			sys.stderr.flush()

			time.sleep(_CHECK_INTERVAL)
			continue

		if ip is None:
			sys.stdout.write("x")
			sys.stdout.flush()

		if ip_lastest is None:
			print("\nstarting ip: %s" % (ip))
			ip_lastest = ip
		elif ip != ip_lastest:
			print("\nNEW IP: %s" % (ip))
			alert(ip)
		else:
			sys.stdout.write(".")
			sys.stdout.flush()

		time.sleep(_CHECK_INTERVAL)

if __name__ == "__main__":
	main()
