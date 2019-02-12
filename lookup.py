"""wancheck.lookup

Simplify DNS address lookups
"""

import dns.message
import dns.opcode
import dns.rdatatype
import dns.rdataclass
import dns.query

def ip(domain, nameserver_ip="8.8.8.8"):
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
			timeout=5,

			# source="", ???
			# source_port=0,

			ignore_unexpected=False,
			one_rr_per_rrset=True
		)

	query_answers = query_response.answer

	ip_address = None
	for answer in query_answers:
		ipv4_records = list(filter(
			lambda r: r.rdtype == dns.rdatatype.A, answer.items))

		if len(ipv4_records):
			ip_address = ipv4_records[0].address
			break

	return ip_address
