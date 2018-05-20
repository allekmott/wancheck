"""wancheck

Simple script to periodically check to see if a machine's external IP has
changed
"""

import time

import dns.message
import dns.opcode
import dns.rdatatype
import dns.rdataclass
import dns.query

VERSION = str("0.0.1")
_CHECK_INTERVAL = 1

def check_ip():
	print("check ip")
	query_message = dns.message.make_query(
			qname="www.google.com",
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
			where="8.8.8.8",
			port=53,
			timeout=2,

			# source="", ???
			# source_port=0,

			ignore_unexpected=False,
			one_rr_per_rrset=True
			)

	query_answers = query_response.answer
	for answer in query_answers:
		for address in answer.items:
			print("%i %s" % (address.rdtype, address.address))

	return query_response


def main():
	print("wancheck v%s" % (VERSION))

	# while True:
	check_ip()
	# 	time.sleep(_CHECK_INTERVAL)

if __name__ == "__main__":
	main()
