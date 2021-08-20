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

    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    try:
      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()
      selection = Actor.query.order_by(Actor.id).all()
      total_actors = len(Actor.query.all())

      return jsonify({
        "success": True,
        "created": actor.id,
        "total_actors": total_actors
      })
    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(jwt):
    body = request.get_json()

    title = body.get('title')
    release_date = body.get('release_date')

    try:
      movie = Movie(title=title, release_date=release_date)
      movie.insert()
      selection = Movie.query.order_by(Movie.id).all()
      total_movies = len(Movie.query.all())

      return jsonify({
        "success": True,
        "created": movie.id,
        "total_movies": total_movies
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

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('edit:actors')
  def edit_actor(jwt, id):
    body = request.get_json()

    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if actor is None:
      abort (404)

    actor.name = name
    actor.age = age
    actor.gender = gender

    try:
      actor.update()

      return jsonify({
        "success": True,
        "updated": actor.id
      })
    except:
      abort(422)

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('edit:movies')
  def edit_movie(jwt, id):
    body = request.get_json()

    title = body.get('title', None)
    release_date = body.get('release_date', None)

    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie is None:
      abort (404)

    movie.title = title
    movie.release_date = release_date

    try:
      movie.update()

      return jsonify({
        "success": True,
        "updated": movie.id
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

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

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
