#!/usr/bin/python3
"""This module defines a class to manage data base storage for hbnb clone"""
import os
from models.base_model import Base, BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """This class manages MySQL db storage of hbnb models"""
    __engine: None
    __session: None

    def __init__(self):
        """Initializes the db storage"""
        user = os.getenv("HBNB_MYSQL_USER")
        passwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all stored models in a dictionary """
        stored_objects = {}
        stored_classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for class_name in stored_classes:
                query = self.__session.query(class_name)
                for obj in query.all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    stored_objects[key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                stored_objects[key] = obj
        return stored_objects

    def new(self, obj):
        """Add new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from database"""
        Base.metadata.create_all(self.__engine)
        curr_section = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(curr_section)
        self.__session = Session()

    def close(self):
        """Close the storage engine"""
        self.__session.close()
