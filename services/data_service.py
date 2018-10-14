from typing import List

import datetime

import bson

from data.bookings import Booking
from data.events import Event # a.k.a sportevent
from data.owners import Owner
from data.sports import Sport # from the tmember side query


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

scheduler = BackgroundScheduler()



def create_account(name: str, email: str, password: str, phone: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email
    owner.password = password
    owner.phone = phone

    owner.save()

    return owner
def joinEvent(eventId, userId):
    query = Event.objects(id=eventId)
    userNumber = Owner.objects(email=userId)[0].phone
    print(userNumber)
    print("Q")
    print(query)
    events = list(query)
    print(events)
    print(events[0])
    if userId not in events[0].userIds:
        events[0].userIds.append(userId)
        print(events[0].userIds)
        print(len(events[0].userIds))
        events[0].save()

        # Custom message
        message = "The rocket will launch in thirty minutes"
        message = urllib.parse.quote_plus(message)
        print(message)
        print(str(events[0].startDate))
        scheduler.add_job(call, 'date', run_date=events[0].startDate, args=[message, userNumber])

        scheduler.start()

    return True

def getEvents():
    print(Event.objects())
    return Event.objects()

def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner

 # Create call from desired number to specified number (from secrets)
def call(callMessage, toNumber):
    call = client.calls.create(
        url='https://handler.twilio.com/twiml/EH2cf9a2f6ab735976090d24e9ca654d96?Message=' + callMessage,
        to=toNumber,
        from_=secrets["from"]
    )

    # Print call ID
    print(call.sid)
def register_event(email,
                   startDate, name, minutes, loc) -> Event:
    event = Event()

    event.name = name
    event.startDate = startDate
    event.minutes = minutes
    event.location = loc

    event.save()

    account = find_account_by_email(email)
    account.event_ids.append(event.id)
    account.save()

    return event


def find_events_for_user(account: Owner) -> List[Event]:
    query = Event.objects(id__in=account.event_ids)
    events = list(query)

    return events


# def add_available_date(event: Event,
#                        start_date: datetime.datetime, days: int) -> Event:
#     booking = Booking()
#     booking.check_in_date = start_date
#     booking.check_out_date = start_date + datetime.timedelta(days=days)
#
#     event = Event.objects(id=event.id).first()
#     event.bookings.append(booking)
#     event.save()
#
#     return event


def add_sport(account, name, length, location, is_outdoors) -> Sport:
    sport = Sport()
    sport.name = name
    sport.length = length
    sport.location = location
    sport.is_outdoors = is_outdoors
    sport.save()

    owner = find_account_by_email(account.email)
    owner.sport_ids.append(sport.id)
    owner.save()

    return sport


def get_sports_for_user(user_id: bson.ObjectId) -> List[Sport]:
    owner = Owner.objects(id=user_id).first()
    sports = Sport.objects(id__in=owner.sport_ids).all()

    return list(sports)


# def get_available_events(checkin: datetime.datetime,
#                         checkout: datetime.datetime, sport: Sport) -> List[Event]:
#     min_size = sport.length / 4
#
#     query = Event.objects() \
#         .filter(duration_minutes__gte=min_size) \
#         .filter(bookings__check_in_date__lte=checkin) \
#         .filter(bookings__check_out_date__gte=checkout)
#
#     if sport.is_outdoors:
#         query = query.filter(is_outdoors=True)
#
#     events = query.order_by('rating_price', '-duration_minutes')
#
#     final_events = []
#     for c in events:
#         for b in c.bookings:
#             if b.check_in_date <= checkin and b.check_out_date >= checkout and b.tmember_sport_id is None:
#                 final_events.append(c)
#
#     return final_events


def book_event(account, sport, event, checkin, checkout):
    booking: Booking = None

    for b in event.bookings:
        if b.check_in_date <= checkin and b.check_out_date >= checkout and b.tmemeber_sport_id is None:
            booking = b
            break

    booking.tmember_owner_id = account.id
    booking.tmember_sport_id = sport.id
    booking.booked_date = datetime.datetime.now()

    event.save()


def get_bookings_for_user(email: str) -> List[Booking]:
    account = find_account_by_email(email)

    booked_events = Event.objects() \
        .filter(bookings__tmember_owner_id=account.id) \
        .only('bookings', 'name')

    def map_event_to_booking(event, booking):
        booking.event = event
        return booking

    bookings = [
        map_event_to_booking(event, booking)
        for event in booked_events
        for booking in event.bookings
        if booking.tmember_owner_id == account.id
    ]

    return bookings