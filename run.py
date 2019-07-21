from app import app, db, Vote_option

db.create_all()

donald = Vote_option(name="Donald Trump")
hillary = Vote_option(name="Hillary Clinton")

db.session.add(donald)
db.session.add(hillary)
db.session.commit()

app.run()
