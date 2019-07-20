from flask import Flask, render_template, request, url_for, flash, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import string
from random import choice
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./votes.db"
app.config['SECRET_KEY'] = 'bouncingblueberries'

db = SQLAlchemy(app)

class Vote_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String)
    vote_option_id = db.Column(db.Integer, db.ForeignKey('vote_option.id'))

class Keys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True)
    used = db.Column(db.Boolean, default=False)

def generate_key():
    chars = string.ascii_lowercase + "0123456789"
    return "".join(choice(chars) for i in range(5))

def key_exists(key_name):
    q = db.session.query(Keys)
    if key_name in [i.key for i in q]:
        return True
    return False 

def key_is_used(keyName):
    q = db.session.query(Keys).filter_by(used=True)
    if keyName in [i.key for i in q]:
        return True
    return False

def is_populated(lst, index):
    try:
        dummy = lst[index]
    except IndexError:
        return False
    return True

def init_db(option1, option2):
    os.system('nul > votes.db')
    db.create_all()
    option = Vote_option(name=option1)
    other_option = Vote_option(name=option2)
    db.session.add(option)
    db.session.add(other_option)
    db.session.commit()

@app.route('/')
def index():
    total_votes = db.session.query(Vote).count()
    voting_options = db.session.query(Vote_option).group_by(Vote_option.id)
    option1 = db.session.query(Vote).filter_by(option=voting_options[0].name).count()
    option2 = db.session.query(Vote).filter_by(option=voting_options[1].name).count()
    vote_counts = [option1, option2]
    response = make_response(render_template('index.html', vote_counts=vote_counts, options=voting_options, total_votes=total_votes))
    if not request.cookies.get("voteKey"):
        key = generate_key()
        while key_exists(key):
            key = generate_key()
        expire_date = datetime.datetime(2019, 7, 20, 23, 59, 59)
        response.set_cookie("voteKey", key, expires=expire_date)
        new_key = Keys(key=key, used=False)
        db.session.add(new_key)
        db.session.commit()
    return response

    

@app.route("/submit_vote", methods=["POST"])
def submit_vote():
    vote_key = request.cookies.get('voteKey')
    if not request.form['timerState']:
        flash("This poll has already expired", "info")
        return redirect(url_for('index'))

    if key_exists(vote_key):
        if not key_is_used(vote_key):
            db.session.query(Keys).filter_by(key=vote_key).first().used = True
            vote_value = request.form['person']
            vote = Vote(option=vote_value)
            db.session.add(vote)
            db.session.commit()
            flash("Your vote has been submitted", "success")
            return redirect(url_for('index'))
        else:
            flash("You have already voted on this poll!", "danger")
            return redirect(url_for('index'))
    else:
        flash("A cookie error has occured :(", "danger")
        return redirect(url_for('index'))

if __name__ == "__main__":
    init_db("Donald Trump", "Hillary Clinton")
    app.run(debug=True)
