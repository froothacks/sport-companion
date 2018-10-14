import mongoengine
import datetime

class Booking(mongoengine.EmbeddedDocument):
    tmember_owner_id = mongoengine.ObjectIdField()
    tmember_sport_id = mongoengine.ObjectIdField()

    booked_date = mongoengine.DateTimeField() # When the match happens
    check_in_time = mongoengine.DateTimeField(required=True) #When the match starts
    check_out_time = mongoengine.DateTimeField(required=True) #when the match ends

    review = mongoengine.StringField()
    price_rating = mongoengine.IntField(default=0)

    @property
    def duration_in_minutes(self):
        dt = self.check_out_time - self.check_in_time
        return dt
		