from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add Restaurant
myFirstRestaurant = Restaurant(name="Fish of Bangladesh")
session.add(myFirstRestaurant)

# Add Shrimp dopiaza
shrimp_dopiaza = MenuItem(name='Shrimp Dopiaza',course='Entree',
    description = 'Made with lots of onion and spicy curry powder', 
    price = 'BDT 200', restaurant=myFirstRestaurant)

# Query/Read
vegburg = session.query(MenuItem).filter_by(name='Veggie Burger')
for item in vegburg:
    print item.id,item.name,item.price,item.restaurant.name
session.query(MenuItem).all()
session.query(MenuItem).first()
somemenu = session.query(MenuItem).slice(2,5)
for item in somemenu:
    print item.id,item.name,item.price,item.restaurant.name
urbanvb = session.query(MenuItem).filter_by(id=10).one()
print urbanvb.price

# Delete
spinach=session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
print spinach.restaurant.name
session.delete(spinach)

session.commit()

session.query(Restaurant).all()