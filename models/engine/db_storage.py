#!/usr/bin/python3
"""This module defines a class to manage data base storage for hbnb clone"""
import os
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
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
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(os.getenv('HBNB_MYSQL_USER'),
                                              os.getenv('HBNB_MYSQL_PWD'),
                                              os.getenv('HBNB_MYSQL_HOST'),
                                              os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns all stored models in a dictionary """
        if not cls:
            data_list = self.__session.query(Amenity)
            data_list.extend(self.__session.query(City))
            data_list.extend(self.__session.query(Place))
            data_list.extend(self.__session.query(Review))
            data_list.extend(self.__session.query(State))
            data_list.extend(self.__session.query(User))
        else:
            data_list = self.__session.query(cls)
        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in data_list}

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
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        Session = scoped_session(self.__session)
        self.__session = Session()

    def close(self):
        """Close the storage engine"""
        self.__session.close()
