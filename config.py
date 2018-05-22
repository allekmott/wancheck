"""wancheck.config

Configuration parameters
"""

import socket

# hostname for reference in alert messages
hostname = socket.gethostname()

# how often to run the DNS check (seconds)
check_interval = 1.0

# twilio account sid, auth token
twilio_account_sid = None
twilio_auth_token = None
twilio_api_key = (twilio_account_sid, twilio_auth_token)

# phone # to receive alerts
phone_source = None
phone_target = None

# lookup & resolver domain
#
# resolver "resolver1.opendns.com" will resolve "myip.opendns.com" to the
# host's external ip
lookup_domain = "myip.opendns.com"
resolver_domain = "resolver1.opendns.com"
