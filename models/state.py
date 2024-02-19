#!/usr/bin/python3
"""State Module for HBNB project"""
from models.base_model import BaseModel, Base
import os
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ This class defines states """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """Return list of cities in file storage"""
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
