import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from uuid import uuid4
import json
import bcrypt

config = json.loads(open('config.json', 'r').read())

app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret_key']
# DB Config settings (sqlite for testing)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gymnastics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Default login session timeout set for 7 days
app.permanent_session_lifetime = timedelta(days=7)

# -----------------------------------------------------------------------------
# DB MODELS
# -----------------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    pw_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_judge = db.Column(db.Boolean, nullable=False, default=False)
    is_user = db.Column(db.Boolean, nullable=False, default=True)


class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    level =  db.Column(db.String(255))
    date_of_birth = db.Column(db.DateTime())
    phone = db.Column(db.String(255))
    mobile = db.Column(db.String(255))
    address = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club =  db.Column(db.String(255))
    contact = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    address =  db.Column(db.String(255))


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    sponsor = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, nullable=False, default=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vault_1 = db.Column(db.Integer())
    vault_2 = db.Column(db.Integer())
    vault_3 = db.Column(db.Integer())
    vault_4 = db.Column(db.Integer())
    vault_5 = db.Column(db.Integer())
    vault_comment = db.Column(db.String(255))
    bars_1 = db.Column(db.Integer())
    bars_2 = db.Column(db.Integer())
    bars_3 = db.Column(db.Integer())
    bars_4 = db.Column(db.Integer())
    bars_5 = db.Column(db.Integer())
    bars_comment = db.Column(db.String(255))
    beam_1 = db.Column(db.Integer())
    beam_2 = db.Column(db.Integer())
    beam_3 = db.Column(db.Integer())
    beam_4 = db.Column(db.Integer())
    beam_5 = db.Column(db.Integer())
    beam_comment = db.Column(db.String(255))
    floor_1 = db.Column(db.Integer())
    floor_2 = db.Column(db.Integer())
    floor_3 = db.Column(db.Integer())
    floor_4 = db.Column(db.Integer())
    floor_5 = db.Column(db.Integer())
    floor_comment = db.Column(db.String(255))
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))


# -----------------------------------------------------------------------------
# APP ROUTES
# -----------------------------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    return 'Gymnastics Club Score'


@app.route('/register')
def register():
    return 'register an athlete'


@app.route('/results')
def results():
    #results =
    return 'score'


@app.route('/athletes')
def athletes():
    athletes = Athlete.query.all()
    return render_template('athletes.html',
                            athletes=athletes)


@app.route('/athlete/<int:id>', methods=['GET'])
def athlete(id):
    result = Athlete.query.get(id)
    events = Event.query.filter_by(athlete_id=id)
    #vault_score = sum([x for x in events if x.isnumeric()])

    return render_template('athlete.html',
                           title='Results',
                           result=result,
                           events=events)#,
                           #vault_score=vault_score)


# -----------------------------------------------------------------------------
"""
APP INIT & BACKEND COMMANDS
flask initdb
    -> drops and initalizes empty databases

flask bootstrap
    -> drops and reinitalizes databases with dummy testing data
"""
# -----------------------------------------------------------------------------
@app.cli.command('initdb')
def reset_db():
    """ Drops and creates fresh database """
    db.drop_all()
    db.create_all()
    print('Initialized default app DB.')


@app.cli.command('bootstrap')
def bootstrap_data():
    """ Populates DB with data for testing """
    db.drop_all()
    db.create_all()

    db.session.add(
        User(
            first_name='admin',
            last_name='admin',
            email='admin@example.com',
            pw_hash=bcrypt.hashpw(b'1234', bcrypt.gensalt(10)),
            is_admin=True,
            is_judge=True,
            is_user=True
        )
    )
    db.session.commit()

    db.session.add(
        Club(
            club ='Tamworth',
            contact='john citizen',
            phone='0267656565',
            email='club@example.com',
            website='https://tamworthgym.com.au',
            address='Greg Norman Dr, Tamworth'
        )
    )
    db.session.commit()

    anne = Athlete(first_name='anne', last_name='smith', gender='female', level='1', date_of_birth=date(2014, 1, 14), phone='0267622622', mobile='0418335555', address='85 Garden Street, Tamworth', club_id=1)
    mary = Athlete(first_name='mary', last_name='lou', gender='female', level='1', date_of_birth=date(2014, 4, 23), phone='0267622888', mobile='0402335555', address='835 Peel Street, Tamworth', club_id=1)
    rose = Athlete(first_name='rose', last_name='brown', gender='female', level='1', date_of_birth=date(2015, 6, 18), phone='0267622444', mobile='0418356740', address='43 Wattle Drive, Tamworth', club_id=1)
    eve = Athlete(first_name='eve', last_name='thompson', gender='female', level='1', date_of_birth=date(2014, 12, 29), phone='0267622228', mobile='0402334444', address='335 Noondah Cres, Tamworth', club_id=1)
    peter = Athlete(first_name='peter', last_name='parker', gender='male', level='1', date_of_birth=date(2013, 11, 17), phone='0267621111', mobile='0418234400', address='401 Gunnedah Road, Tamworth', club_id=1)

    db.session.add(anne)
    db.session.add(mary)
    db.session.add(rose)
    db.session.add(eve)
    db.session.add(peter)
    db.session.commit()

    db.session.add(
        Competition(
            name='Test Competition One',
            sponsor='NICU',
            is_active=True
        )
    )
    db.session.commit()

    db.session.add(
        Event(
            vault_1=25,
            vault_2=25,
            vault_3=25,
            vault_4=25,
            vault_5=25,
            vault_comment='little wobble on landing deducted',
            bars_1=24,
            bars_2=24,
            bars_3=24,
            bars_4=24,
            bars_5=24,
            bars_comment='slipped on second change marked down',
            beam_1=23,
            beam_2=23,
            beam_3=23,
            beam_4=23,
            beam_5=23,
            beam_comment='great performance',
            floor_1=22,
            floor_2=22,
            floor_3=22,
            floor_4=22,
            floor_5=22,
            floor_comment='need to hold longer on presentation',
            athlete_id=1,
            competition_id=1
        )
    )
    db.session.commit()
    print('Bootstrap of DB initialized...')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
