#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
import os
from models.city import City
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City',
            cascade='all, delete, delete-orphan',
            backref='state'
        )
    else:
        @property
        def cities(self):
            """Returns the list of City instances"""
            list_of_cities = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    list_of_cities.append(city)
            return list_of_cities
