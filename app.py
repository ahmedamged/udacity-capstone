import os
from flask import Flask, request, abort, jsonify, render_template, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
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
  @cross_origin()
  def welcome_page():
  	return render_template('index.html'), 200

  @app.route('/coolkids')
  def be_cool():
    return "Be cool, man, be coooool! You're almost a FSND grad!"

  @app.route('/actors')
  @requires_auth("get:actors")
  def show_actors(jwt):
    actors_query = Actor.query.order_by(Actor.id).all()
    actors = [actor.short() for actor in actors_query]

    return jsonify({
        "success": True,
        "actors": actors
    }), 200

  @app.route('/movies')
  @requires_auth("get:movies")
  def show_movies(jwt):
    movies_query = Movie.query.order_by(Movie.id).all()
    movies = [movie.short() for movie in movies_query]

    return jsonify({
        "success": True,
        "movies": movies
    }), 200

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(jwt):
    body = request.get_json()
    if not ('name' in body and 'age' in body and 'gender' in body):
      abort(422)

    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    try:
      actor=Actor(name=name, age=age, gender=gender)
      actor.insert()
      return jsonify({
        "success": True,
        "created": actor.id,
        "actor": [actor.format()]
      })
    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(jwt):
    body = request.get_json()
    if not('title' in body and 'release_date' in body):
      abort(422)

    title = body.get('title')
    release_date = body.get('release_date')

    try:
      movie=Movie(title=title, release_date=release_date)
      movie.insert()
      return jsonify({
        "success": True,
        "created": movie.id,
        "movies": [movie.format()]
      })
    except:
      abort(422)

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, id):
    movie = Movie.query.get(id)
    if not movie:
      abort(404)
    try:
      movie.delete()
      return jsonify({
        "success": True,
        "deleted": id
      })
    except:
      abort(422)

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, id):
    actor = Actor.query.get(id)
    if not actor:
      abort(404)
    try:
      actor.delete()
      return jsonify({
        "success": True,
        "deleted": id
      })
    except:
      abort(422)

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable request"
    }), 422

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(AuthError)
  def not_authenticated(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error
    }), 401

  return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
