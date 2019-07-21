from app import app, db, Vote_option
import os

db.create_all()

donald = Vote_option(name="Donald Trump")
hillary = Vote_option(name="Hillary Clinton")

db.session.add(donald)
db.session.add(hillary)
db.session.commit()

port = os.environ.get("PORT", 5000)

app.run(host="0.0.0.0", port=port)
