import datetime
import mongoengine

from data.bookings import Booking


class Event(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    name = mongoengine.StringField(required=True)
    rating_price = mongoengine.FloatField(required=True) # Minimum rating that the team maker is expecting to have for team members
    duration_minutes = mongoengine.FloatField(required=True)
    in_public_place = mongoengine.BooleanField(required=True)
    in_outdoors = mongoengine.BooleanField(required=True)
    allow_non_friends = mongoengine.BooleanField(default=False)

    bookings = mongoengine.EmbeddedDocumentListField(Booking)

    meta = {
        'db_alias': 'core',
        'collection': 'events'
    }

		