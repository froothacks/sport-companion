import datetime
import mongoengine

"""
The sports query from the probable team member
"""


class Sport(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    species = mongoengine.StringField(required=True)

    length = mongoengine.FloatField(required=True) #duration in minutes
    location = mongoengine.StringField(required=True)
    is_outdoors = mongoengine.BooleanField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'sports'
    }
