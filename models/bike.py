from datetime import datetime

from app import db


class Bike(db.Model):
    __tablename__ = "bike"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    secondary_phone = db.Column(db.String)
    city = db.Column(db.String)
    brand = db.Column(db.String)
    color = db.Column(db.String)
    bike_id = db.Column(db.String)
    assets = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())
