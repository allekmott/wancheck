"""wancheck.sms

SMS messaging routines
"""

import twilio.rest

import config

def twilio_send(body, to=config.phone_target, from_=config.phone_source):
	client = twilio.rest.Client(*config.twilio_api_key)
	message = client.messages.create(body=body, to=to, from_=from_)

	return message

def alert(message, phone_target=config.phone_target): pass
	#twilio_send(message, to=phone_target)

if __name__ == "__main__":
	alert("test")
