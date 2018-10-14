import datetime
import mongoengine

"""
The sports query from the probable team member
"""


class Sport(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    location = mongoengine.StringField(required=True)

    duration_minutes = mongoengine.FloatField(required=True) #duration in minutes
    name = mongoengine.StringField(required=True)
    is_outdoors = mongoengine.BooleanField(required=True)
    is_public = mongoengine.BooleanField(required=True)
    allow_non_friends = mongoengine.BooleanField(required=True)
    meta = {
        'db_alias': 'core',
        'collection': 'sports'
    }
