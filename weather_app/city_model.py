from db import db


class City(db.Model):
    __tablename__ = "city"

    _id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True, nullable=False)
    temp = db.Column(db.Float, nullable=False, default=0.00)
    state = db.Column(db.String, nullable=False, default="Unknown")

    def __init__(self, city, temp=0.00, state="Unknown", _id=None):
        self._id = _id
        self.city = city
        self.temp = temp
        self.state = state

    def json(self):
        return {"_id": self._id, "city": self.city, "temp": self.temp, "state": self.state}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def find_by_city(cls, _city):
        return cls.query.filter_by(city=_city).first()

    @classmethod
    def find_all(cls):
        return [item.json() for item in cls.query.all()]

    @classmethod
    def find_between(cls, start, end):
        return [event.json() for event in cls.query.filter(cls.date.between(start, end)).all()]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
