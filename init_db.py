from app import db, Vote_option

# Create all the tables
db.create_all()

# create fighters
trump = Vote_option(name='Donald Trump')
clinton = Vote_option(name='Hillary Clinton')

# add fighters to session
db.session.add(trump)
db.session.add(clinton)

# commit the fighters to database
db.session.commit()