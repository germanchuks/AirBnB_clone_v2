#!/usr/bin/python3
"""City Module for HBNB project"""
from models.base_model import BaseModel, Base
import os
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """This class defines Cities"""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship('Place', backref='cities',
                          cascade='all, delete-orphan')
