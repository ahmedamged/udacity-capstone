from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

# DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
# DB_USER = os.getenv('DB_USER', 'postgres')
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'ahmed')
# DB_NAME = os.getenv('DB_NAME', 'udacitycapstone')
# DB_PATH = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

database_path = os.environ['DATABASE_URL'].replace("://", "ql://", 1)
# database_name = "udacitycapstone"
# database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'ahmed', 'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Integer, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

    def long(self):
        return {
            "title": self.title,
            "release_date": self.release_date
        }

    def __repr__(self):
        return "<Movie {} {} />".format(self.title, self.release_date)

class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def long(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    def __repr__(self):
        return "<Actor {} {} {} />".format(self.name, self.age, self.gender)
