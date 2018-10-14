import datetime
import mongoengine

from data.bookings import Booking


class Event(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    name = mongoengine.StringField(required=True)
    location = mongoengine.StringField(required=True)
    startDate = mongoengine.DateTimeField(required=True)
    minutes = mongoengine.FloatField(required=True)

    userIds = mongoengine.ListField()


    meta = {
        'db_alias': 'core',
        'collection': 'events'
    }
