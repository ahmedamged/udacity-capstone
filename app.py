import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/')
  def get_greeting():
    excited = os.environ['EXCITED']
    greeting = "Hello"
    if excited == 'true': greeting = greeting + "!!!!!"
    return greeting

  @app.route('/coolkids')
  def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"

  @app.route('/actors')
  @requires_auth("get:actors")
  def show_actors(payload):
    actors_query = Actor.query.order_by(Actor.id).all()
    actors = [actor.short() for actor in actors_query]

    return jsonify({
        "success": True,
        "actors": actors
    }), 200

  return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
