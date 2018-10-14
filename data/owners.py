import datetime
import mongoengine

"""
Here owners refers to both event owner (a.k.a team makers)
and booking owner (a.k.a team members)
"""

class Owner(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    password = mongoengine.StringField(required=True)

    sport_ids = mongoengine.ListField() # team member
    event_ids = mongoengine.ListField() # team maker

    meta = {
        'db_alias': 'core',
        'collection': 'owners'
    }
