from peewee import OperationalError
from models import Business
from models import Review
from models import User
from models import Checkin
from models import Neighborhood
from models import Category
import json
import decimal
from datetime import datetime

def iterate_file(model_name, shortcircuit=True, status_frequency=500):
    i = 0
    jsonfilename = "json/yelp_training_set_%s.json" % model_name.lower()
    with open(jsonfilename) as jfile:
        for line in jfile:
            i += 1
            yield json.loads(line)
            if i % status_frequency == 0:
                print("Status >>> %s: %d" % (jsonfilename, i))
                if shortcircuit and i == 10:
                    raise StopIteration()
                    
    
def save_businesses():
    for bdata in iterate_file("business", shortcircuit=False):
        business = Business()
        business.business_id = bdata['business_id']
        business.name = bdata['name']
        business.full_address = bdata['full_address']
        business.city = bdata['city']
        business.state = bdata['state']
        business.latitude = bdata['latitude']
        business.longitude = bdata['longitude']
        business.stars = decimal.Decimal(bdata.get('stars', 0))
        business.review_count = int(bdata['review_count'])
        business.is_open = True if bdata['open'] == "True" else False
        business.save()

        save_categories(bdata['business_id'], bdata['categories'])
        save_neighborhoods(bdata['business_id'], bdata['neighborhoods'])


def save_categories(business_id, cat_jarray):
    for name in cat_jarray:
        category = Category()
        category.business_id = business_id
        category.category_name = name
        category.save()


def save_neighborhoods(business_id, hood_jarray):
    for hood in hood_jarray:
        neighborhood = Neighborhood()
        neighborhood.business_id = business_id
        neighborhood.neighborhood_name = hood
        neighborhood.save()

def save_reviews():
    for rdata in iterate_file("review", shortcircuit=False):
        rev = Review()
        rev.business_id = rdata['business_id']
        rev.user_id = rdata['user_id']
        rev.stars = int(rdata.get('stars', 0))
        rev.text = rdata['text']
        rev.date = datetime.strptime(rdata['date'], "%Y-%m-%d")
        rev.useful_votes = int(rdata['votes']['useful'])
        rev.funny_votes = int(rdata['votes']['funny'])
        rev.cool_votes = int(rdata['votes']['cool'])
        rev.save()

def save_users():
    for udata in iterate_file("user", shortcircuit=False):
        user = User()
        user.user_id = udata['user_id']
        user.name = udata['name']
        user.review_count = int(udata['review_count'])
        user.average_stars = decimal.Decimal(udata.get('average_stars', 0))
        user.useful_votes = int(udata['votes']['useful'])
        user.funny_votes = int(udata['votes']['funny'])
        user.cool_votes = int(udata['votes']['cool'])
        user.save()

def save_checkins():
    for cdata in iterate_file("checkin", shortcircuit=False):
        checkin = Checkin()
        checkin.business_id = cdata['business_id']
        for day in range(7):
            for hour in range(24):
                number = int(cdata['checkin_info'].get("%s-%s" % (hour, day), 0))
                if day is 0:
                    checkin.sunday_count += number
                elif day is 1:
                    checkin.monday_count += number
                elif day is 2:
                    checkin.tuesday_count += number
                elif day is 3:
                    checkin.wednesday_count += number
                elif day is 4:
                    checkin.thursday_count += number
                elif day is 5:
                    checkin.friday_count += number
                elif day is 6:
                    checkin.saturday_count += number
                    checkin.save()

def reset_database():
    tables = (Business, Review, User, Checkin, Neighborhood, Category,)
    for table in tables:
        # Nuke the Tables
        try:
            table.drop_table()
        except OperationalError:
            pass
        # Create the Tables
        try:
            table.create_table()
        except OperationalError:
            pass
    
if __name__ == "__main__":
    reset_database()

    save_businesses()
    save_users()
    save_checkins()
    save_review()

    
