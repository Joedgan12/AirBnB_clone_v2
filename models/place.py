#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """ The Place class """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary='place_amenity',
                             viewonly=False)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """ reviews getter for FileStorage """

            my_list = {}
            all_review = self.reviews
            for rev in all_review:
                if self.id == rev.id:
                    my_list.append(rev)
            return my_list

        @property
        def amenities(self):
            """getter amenity that returns list of Amenity"""

            my_ame = {}
            all_amenities = self.amenities
            for ame in all_amenities:
                if self.id == ame.id:
                    my_ame.append(ame)
            return my_ame

        @amenities.setter
        def amenities(sef, obj=None):
            """Setter amenities"""

            if obj.__class__name__ == 'Amenity':
                self.amenities_ids.append(obj.id)

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey
                             ('amenities.id'),
                             primary_key=True, nullable=False))
