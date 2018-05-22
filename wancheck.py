"""wancheck

Simple script to periodically check to see if a machine's external IP has
changed
"""

import socket
import sys
import time

import dns.exception

import config
import lookup
import sms

VERSION = str("0.0.1")

class WANCheckException(Exception): pass
class IPChangedException(WANCheckException):
	def __init__(self, new_ip):
		self.new_ip = new_ip

def check_ip(latest_ip,
		resolver_domain=config.resolver_domain,
		lookup_domain=config.lookup_domain):
	resolver_ip = lookup.ip(config.resolver_domain)

	ip = lookup.ip(lookup_domain, resolver_ip)
	if ip != latest_ip:
		raise IPChangedException(ip)

def ulog(stream, *args, **kwargs):
	"""Unbuffered write to stream"""
	stream.write(*args, **kwargs)
	stream.flush()

def main():
	print("wancheck v%s\n" % (VERSION))

	print("hostname: %s\n" % (config.hostname))
	print("using resolver: %s" % (config.resolver_domain))
	print("using lookup domian: %s" % (config.lookup_domain))

	latest_ip = None

	while True:
		ip = None
		try:
			check_ip(latest_ip, config.resolver_domain, config.lookup_domain)
			ulog(sys.stdout, ".")
		except IPChangedException as e:
			if latest_ip is None:
				print("\ninitial ip is %s" % (e.new_ip))
				sms.alert("new ip for %s: %s" % (config.hostname, e.new_ip))

			latest_ip = e.new_ip
		except dns.exception.DNSException as e:
			ulog(sys.stderr, "D")
		except Exception as e:
			ulog(sys.stderr, "E")

			if hasattr(e, "errno") and type(e.errno) is int:
				ulog(sys.stderr, "%i" % (e.errno))

		time.sleep(config.check_interval)

if __name__ == "__main__":
	main()
