#!/usr/bin/python
""" Review Module for HBNB project """
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        nullable=False,
        primary_key=True
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        nullable=False,
        primary_key=True
    )
)


class Place(BaseModel, Base):
    """This class defines places"""
    __tablename__ = 'places'
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review",
            cascade="all, delete, delete-orphan",
            backref="place")
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            backref="place_amenities",
            viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def reviews(self):
            """Returns the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """ Returns list of Amenities instances """
            from models.amenity import Amenity
            amenities_list = []
            all_amenities = models.storage.all(Amenity)
            for value in all_amenities.values():
                if value.id in self.amenity_ids:
                    amenities_list.append(value)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """Adds an Amenity id"""
            from models.amenity import Amenity
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
