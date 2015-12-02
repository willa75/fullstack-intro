#!/usr/bin/env python
# 
# restuarant.py -- implementation of restuarant menu system
#

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getRestaurants():
	"""Get a list of all restuarants and their ids"""
	restuarants = session.query(Restaurant).all()
	return restuarants

def addRestaurant(name):
	"""Adds restuarant to database"""
	newRestaurant = Restaurant(name=name)
	session.add(newRestaurant)
	session.commit()

def getRestaurantName(restaurantID):
	restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
	return restaurant.name

def updateRestaurantName(name,restaurantID):
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
    if restaurant != []:
        restaurant.name = name
        session.add(restaurant)
        session.commit()

def deleteRestaurant(restaurantID):
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
    if restaurant != []:
        session.delete(restaurant)
        session.commit()