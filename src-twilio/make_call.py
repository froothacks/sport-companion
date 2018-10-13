from twilio.rest import Client
import urllib.parse
import json

# Load secrets
with open('secrets.json') as secretsFile:
    secrets = json.loads(secretsFile.read())

# Initialize Twilio
account_sid = secrets["account_sid"]
auth_token = secrets["auth_token"]
client = Client(account_sid, auth_token)

# Custom message
message = "The rocket will launch in thirty minutes"
message = urllib.parse.quote_plus(message)
print(message)

# Create call from desired number to specified number (from secrets)
call = client.calls.create(
                        url='https://handler.twilio.com/twiml/EH2cf9a2f6ab735976090d24e9ca654d96?Message='+message,
                        to=secrets["to"],
                        from_=secrets["from"]
                    )
# Print call ID
print(call.sid)
