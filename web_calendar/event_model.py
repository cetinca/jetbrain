import datetime

from db import db


class EventModel(db.Model):
    __tablename__ = "events"

    _id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, event, date, _id=None):
        self._id = _id
        self.event = event
        self.date = date

    def json(self):
        return {"id": self._id, "event": self.event, "date": datetime.datetime.strftime(self.date, "%Y-%m-%d")}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def find_all(cls):
        return [event.json() for event in cls.query.all()]

    @classmethod
    def find_between(cls, start, end):
        return [event.json() for event in cls.query.filter(cls.date.between(start, end)).all()]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
