from twilio.rest import Client
import urllib.parse
import json
import os, time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import dateutil.parser

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
def call(callMessage):
	call = client.calls.create(
        url='https://handler.twilio.com/twiml/EH2cf9a2f6ab735976090d24e9ca654d96?Message='+callMessage,
        to=secrets["to"],
        from_=secrets["from"]
    )

	# Print call ID
	print(call.sid)

def tick(text):
    print(text + '! The time is: %s' % datetime.now())


scheduler = BackgroundScheduler()
dd = dateutil.parser.parse("2018-10-13T12:11:50")
scheduler.add_job(call, 'date',run_date=dd, args=[message])

scheduler.start()
try:
    # Simulate application activity
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
