import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime, timedelta

# If run locally, uncomment the following below
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

# For running on Prod
#database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}/{}".format(database_setup["user_name"], database_setup["password"], database_setup["port"], database_setup["database_name_test"]))

db = SQLAlchemy()

def setup_db(app):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    '''
    db_drop_and_create_all()
        drops the database tables and starts fresh
        can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    add_records()


class Actor(db.Model):
    '''
    Actor
    a persistent actor entity, extends the base SQLAlchemy Model
    '''
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name' : self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    '''
    Movie
    a persistent movie entity, extends the base SQLAlchemy Model
    '''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)

    def __init__(self, title, release_date, actor_id):
        self.title = title
        self.release_date = release_date
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title' : self.title,
            'release_date': datetime.strftime(self.release_date, '%a, %b %d %Y'),
            'actor': {
              'name' : Actor.query.filter(Actor.id == self.actor_id).first().name,
              'id': self.actor_id
            }
        }


def add_records():
    print('Creating actors and movies')

    actor_david = (Actor(
        age = 45,
        gender = 'male',
        name="David"
    ))

    actor_chris = (Actor(
        age = 35,
        gender = 'male',
        name = "Chris"
    ))

    actor_katie = (Actor(
        age = 30,
        gender = 'female',
        name="Katie"
    ))
    actor_david.insert()
    actor_chris.insert()
    actor_katie.insert()

    raids_movie = (Movie(
        title = 'Raids of the ice',
        release_date = datetime.now() - timedelta(days=3*365),
        actor_id = actor_chris.id
    ))

    up_movie = (Movie(
        title = 'up up and away',
        release_date = datetime.now() - timedelta(days=3*365),
        actor_id = actor_katie.id
    ))

    find_movie = (Movie(
        title = 'finding katie',
        release_date = datetime.now() - timedelta(days=3*365),
        actor_id = actor_katie.id
    ))
    raids_movie.insert()
    up_movie.insert()
    find_movie.insert()
