import peewee
from peewee import *


db = MySQLDatabase('yelp_data_mining', user='USERNAME',passwd='PASSWORD')

class Business(peewee.Model):
    """
    {
      'type': 'business',
      'business_id': (encrypted business id),
      'name': (business name),
      'neighborhoods': [(hood names)],
      'full_address': (localized address),
      'city': (city),
      'state': (state),
      'latitude': latitude,
      'longitude': longitude,
      'stars': (star rating, rounded to half-stars),
      'review_count': review count,
      'categories': [(localized category names)]
      'open': True / False (corresponds to permanently closed, not business hours),
    }
    """
    bid = peewee.PrimaryKeyField()
    business_id = peewee.CharField()  # encrypted ID with letters, numbers, and symbols
    name = peewee.CharField()
    full_address = peewee.CharField()
    city = peewee.CharField()
    state = peewee.CharField(max_length=3)  # XGL
    latitude = peewee.CharField()
    longitude = peewee.CharField()
    stars = peewee.DecimalField()  # star rating rounded to half-stars
    review_count = peewee.BigIntegerField()
    is_open = peewee.BooleanField()
    # neighborhoods = None # list of hood names
    # categories = None # list of category names

    class Meta:
        database = db

class Category(peewee.Model):
    """
    Derived from Business.categories Field.
    """
    id = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    category_name = peewee.CharField()

    class Meta:
        database = db

class Neighborhood(peewee.Model):
    '''
    Derived from Business.neighborhoods Field.
    '''
    id = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    neighborhood_name = peewee.CharField()

    class Meta:
        database = db

class Review(peewee.Model):
    """
    {
      'type': 'review',
      'business_id': (encrypted business id),
      'user_id': (encrypted user id),
      'stars': (star rating),
      'text': (review text),
      'date': (date, formatted like '2012-03-14', %Y-%m-%d in strptime notation),
      'votes': {'useful': (count), 'funny': (count), 'cool': (count)}
    }
    """
    rid = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    user_id = peewee.CharField()
    stars = peewee.IntegerField()
    text = peewee.TextField()
    date = peewee.DateField(formats="%Y-%m-%d")  # '2012-03-14', %Y-%m-%d in strptime notation
    useful_votes = peewee.IntegerField()
    funny_votes = peewee.IntegerField()
    cool_votes = peewee.IntegerField()

    class Meta:
        database = db

class User(peewee.Model):
    """
    {
      'type': 'user',
      'user_id': (encrypted user id),
      'name': (first name),
      'review_count': (review count),
      'average_stars': (floating point average, like 4.31),
      'votes': {'useful': (count), 'funny': (count), 'cool': (count)}
    }
    """
    uid = peewee.PrimaryKeyField()
    user_id = peewee.CharField()
    name = peewee.CharField()
    review_count = peewee.IntegerField()
    average_stars = peewee.FloatField()
    useful_votes = peewee.IntegerField()
    funny_votes = peewee.IntegerField()
    cool_votes = peewee.IntegerField()

    class Meta:
        database = db

class Checkin(peewee.Model):
    """
    {
      'type': 'checkin',
      'business_id': (encrypted business id),
      'checkin_info': {
            '0-0': (number of checkins from 00:00 to 01:00 on all Sundays),
            '1-0': (number of checkins from 01:00 to 02:00 on all Sundays), 
            ... 
            '14-4': (number of checkins from 14:00 to 15:00 on all Thursdays),
            ...
            '23-6': (number of checkins from 23:00 to 00:00 on all Saturdays)
      } # if there was no checkin for an hour-day block it will not be in the dict
    }
    """
    cid = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    sunday_count = peewee.IntegerField(default=0)
    monday_count = peewee.IntegerField(default=0)
    tuesday_count = peewee.IntegerField(default=0)
    wednesday_count = peewee.IntegerField(default=0)
    thursday_count = peewee.IntegerField(default=0)
    friday_count = peewee.IntegerField(default=0)
    saturday_count = peewee.IntegerField(default=0)

    class Meta:
        database = db

class Tip(peewee.Model):
    """
    {
        'type': 'tip',
        'text': (tip text),
        'business_id': (encrypted business id),
        'user_id': (encrypted user id),
        'date': (date, formatted like '2012-03-14'),
        'likes': (count),
    }
    """
    tip_id = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    text = peewee.TextField()
    user_id = peewee.CharField()
    date = peewee.DateField(formats="%Y-%m-%d")  # '2012-03-14', %Y-%m-%d in strptime notation
    likes = peewee.IntegerField()

    class Meta:
        database = db