wancheck
========
Wancheck is a nifty (hacky) solution to dealing with hosts confined to
dynamic IPs. It monitors a given host's internet-facing IP, notifying the
user by text message upon any change.

## Setup
Wancheck has two dependencies: `twilio` and `dnspython`. They can be installed
via PIP like so:

```
pip install -r requirements.txt
```

### Configuration
For now, this program is only designed to integrate with the Twilio API.

To connect it to your account, modify `config.py`:

1. Set `twilio_account_sid` to your Twilio account SID
2. Set `twilio_auth_token` to your Twilio auth token
3. Set `phone_source` to the phone number you wish to receive notifications
   from
4. Set `phone_target` to the phone number you wish the notifications to be
   sent to

`wancheck`'s IP test interval is set to `1` by default, meaning it will check
every second. To change this, modify the `check_interval` parameter in
`config.py`.

## Running
To run wancheck:

```
python wancheck.py
```

