from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

# engine = create_engine('postgresql://catalog:password@localhost/catalog')
engine = create_engine('sqlite:///catalog.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Caron Mullins", email="caronmullins2016@gmail.com", picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category 1 with 3 items
category1 = Category(user_id=1, name="Soccer", image="http://neobasketball.com/img/bballcourt.jpg")
session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Soccer Ball", description="Soccer balls for practicing and match games.", category=category1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Soccer Boots", description="Soccer boots to maxumise gameplay", category=category1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Whistles", description="Whistles for training sessions.", category=category1)
session.add(item3)
session.commit()



# Next Categories and its items
category2 = Category(user_id=1, name="Basketball", image="http://neobasketball.com/img/bballcourt.jpg")
session.add(category2)
session.commit()

item1 = Item(user_id=1, name="Crew Socks", description="Stretchy ribbed socks extending to mid calf", category_id = category2.id)
session.add(item1)
session.commit()


# Categories 3
category3 = Category(user_id=1, name="Baseball", image="http://totalsportscomplex.com/wp-content/uploads/2014/09/baseball-pic.jpg")
session.add(category3)
session.commit()

item1 = Item(user_id=1, name="Crew Socks", description="Stretchy ribbed socks extending to mid calf", category_id = category3.id)
session.add(item1)
session.commit()


# Categories 4
category4 = Category(user_id=1, name="Frisbee", image="http://uvmbored.com/wp-content/uploads/2015/10/how_the_frisbee_took_flight.jpg")
session.add(category4)
session.commit()

item1 = Item(user_id=1, name="Flying Disc", description="A Flying disc or a Flying Saucer", category_id = category4.id)
session.add(item1)
session.commit()


# Categories 5
category5 = Category(user_id=1, name="Snowboarding", image="https://pantherfile.uwm.edu/collins9/www/finalproject5/Project_5/snowboarding3.jpg")

session.add(category5)
session.commit()

item1 = Item(user_id=1, name="Snowboard", description="Wooden board suitable to glide on snow", category_id = category5.id)


session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Goggles", description="Anit-glare protective safety glasses",category_id = category5.id)


session.add(item2)
session.commit()

# Categories 6
category6 = Category(user_id=1, name="Rock Climbing", image="http://asme.berkeley.edu/wordpress/wp-content/uploads/2013/11/Rock-Climbing-Wallpaper-HD.jpg")

session.add(category6)
session.commit()

item1 = Item(user_id=1, name="Shoes", description="Superior performance shoew wtih excellent grip", category_id = category6.id)



session.add(item1)
session.commit()

# Categories 7
category7 = Category(user_id=1, name="Skating", image="http://www.ocasia.org/Images-OCA/During-the-Roller-Skating-XXX-contest-between-XXX-_53834132011574.jpg")

session.add(category7)
session.commit()

item1 = Item(user_id=1, name="Skates", description="Roller skates with bearing suitable for beginner and advanced skater", category_id = category7.id)


session.add(item1)
session.commit()

# Categories 8
category8 = Category(user_id=1, name="Hockey", image="http://www.picture-newsletter.com/street-hockey/street-hockey-39.jpg")

session.add(category8)
session.commit()

item1 = Item(user_id=1, name="Stick", description="Composite Stick favorable for both ice and street hockey", category_id = category8.id)


session.add(item1)
session.commit()


print "added menu items!"
