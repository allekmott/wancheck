"""wancheck

Simple script to periodically check to see if a machine's external IP has
changed
"""

import socket
import sys
import time

import dns.exception
import lookup

VERSION = str("0.0.1")

_CHECK_INTERVAL = 1

_LOOKUP_DOMAIN = "myip.opendns.com"
_RESOLVER_DOMAIN = "resolver1.opendns.com"

def alert(ip):
	pass

class WANCheckException(Exception): pass
class IPChangedException(WANCheckException):
	def __init__(self, new_ip):
		self.new_ip = new_ip

def check_ip(latest_ip, resolver, lookup_domain="myip.opendns.com"):
	resolver_ip = lookup.ip(_RESOLVER_DOMAIN)

	ip = lookup.ip(lookup_domain, resolver_ip)
	if ip != latest_ip:
		raise IPChangedException(ip)

def ulog(stream, *args, **kwargs):
	"""Unbuffered write to stream"""
	stream.write(*args, **kwargs)
	stream.flush()

def main():
	print("wancheck v%s\n" % (VERSION))

	print("using resolver '%s'" % (_RESOLVER_DOMAIN))
	print("using lookup domian '%s'" % (_LOOKUP_DOMAIN))

	latest_ip = None

	while True:
		ip = None
		try:
			check_ip(latest_ip, _RESOLVER_DOMAIN, _LOOKUP_DOMAIN)
			ulog(sys.stdout, ".")
		except IPChangedException as e:
			if latest_ip is None:
				print("\ninitial ip is %s" % (e.new_ip))

			latest_ip = e.new_ip
		except dns.exception.DNSException as e:
			ulog(sys.stderr, "D")
		except Exception as e:
			ulog(sys.stderr, "E")

			if hasattr(e, "errno") and type(e.errno) is int:
				ulog(sys.stderr, "%i" % (e.errno))

		time.sleep(_CHECK_INTERVAL)

if __name__ == "__main__":
	main()
