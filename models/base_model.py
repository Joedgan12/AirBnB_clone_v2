#!/usr/bin/python3
"""This module defines base class for all models in our hbnb clone"""
import uuid
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initialize of base model class
        """
        from datetime import datetime
        from models import storage
        if kwargs:
            if self.id is None:
                self.id = str(uuid.uuid4())
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
                if self.created_at is None:
                    self.created_at = datetime.now()
                if self.updated_at is None:
                    self.updated_at = datetime.now()

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary['created_at'] = self.created_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del(dictionary['_sa_instance_state'])
        return dictionary

    def delete(self):
        from models import storage
        models.storage.delete(self)
