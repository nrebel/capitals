from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CountryMap(db.Model):
    __tablename__ = 'country_maps'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), unique=True, nullable=False)
    city_with_most_capitals = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)  # JSON of the distances and city details

class CityMap(db.Model):
    __tablename__ = 'city_maps'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)  # JSON of the distances and capitals
    __table_args__ = (db.UniqueConstraint('country', 'city'),)
