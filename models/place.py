#!/usr/bin/python
""" Place Module for HBNB project """
import os
import models
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
from models.amenity import Amenity
from models.review import Review


if os.getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id',
                                 String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id',
                                 String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """This class defines places"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review', backref='place',
                               cascade='all, delete-orphan')
        amenities = relationship('Amenity',
                                 secondary='place_amenity',
                                 backref='places', viewonly=False)
    else:
        @property
        def reviews(self):
            """Returns list of Review instances"""
            return [review for review in models.storage.all(Review)
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """Returns list of Amenities instances"""
            return [amenity for amenity in models.storage.all(Amenity)
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Adds an Amenity id"""
            if (type(obj) == Amenity):
                self.amenity_ids.append(obj.id)
