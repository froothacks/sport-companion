from typing import List
from pdb import set_trace as keyboard
import datetime

import bson

from data.bookings import Booking
from data.events import Event # a.k.a sportevent
from data.owners import Owner
from data.sports import Sport # from the tmember side query


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner


def register_event(active_account: Owner,
                  name, allow_non_friends, in_public_place,
                  in_outdoors, duration_minutes, rating_price, location) -> Event:
    event = Event()

    event.name = name
    event.location = location
    event.duration_minutes = duration_minutes
    event.in_public_place = in_public_place
    event.in_outdoors = in_outdoors
    event.allow_non_friends = allow_non_friends
    event.rating_price = rating_price

    event.save()

    account = find_account_by_email(active_account.email)
    account.event_ids.append(event.id)
    account.save()

    return event


def find_events_for_user(account: Owner) -> List[Event]:
    query = Event.objects(id__in=account.event_ids)
    events = list(query)

    return events


def add_available_date(event: Event,
                       start_date: datetime.datetime, tiime: int) -> Event:
    booking = Booking()
    booking.check_in_time = start_date
    booking.check_out_time = start_date + datetime.timedelta(minutes=tiime)

    event = Event.objects(id=event.id).first()
    event.bookings.append(booking)
    event.save()

    return event


def add_sport(account, name, duration_minutes, location, is_outdoors, is_public) -> Sport:
    sport = Sport()
    sport.name = name
    sport.duration_minutes = duration_minutes
    sport.location = location
    sport.is_outdoors = is_outdoors
    sport.is_public = is_public
    sport.save()

    owner = find_account_by_email(account.email)
    owner.sport_ids.append(sport.id)
    owner.save()

    return sport


def get_sports_for_user(user_id: bson.ObjectId) -> List[Sport]:
    owner = Owner.objects(id=user_id).first()
    sports = Sport.objects(id__in=owner.sport_ids).all()

    return list(sports)


def get_available_events(checkin: datetime.datetime,
                        checkout: datetime.datetime, sport: Sport) -> List[Event]:
    min_size = sport.duration_minutes
    location = sport.location

    query = Event.objects() \
        .filter(duration_minutes__lte=min_size) \
        .filter(bookings__check_in_time__lte=checkin) \
        .filter(bookings__check_out_time__gte=checkout) 
        
    #if sport.allow_non_friends:
     #   query = query.filter(allow_non_friends=True)

    events = query.order_by('rating_price', '-duration_minutes')

    final_events = []
    for c in events:
        for b in c.bookings:
            if b.check_in_time <= checkin and b.check_out_time >= checkout and b.tmember_sport_id is None:
                final_events.append(c)

    return final_events


def book_event(account, sport, event, checkin, checkout):
    booking: Booking = None

    for b in event.bookings:
        if b.check_in_time <= checkin and b.check_out_time >= checkout and b.tmember_sport_id is None:
            booking = b
            break

    booking.tmember_owner_id = account.id
    booking.tmember_sport_id = sport.id
    booking.booked_date = datetime.datetime.now()

    keyboard()
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