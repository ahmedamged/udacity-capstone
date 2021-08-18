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
  def show_actors(payload):
    actors_query = Actor.query.order_by(Actor.id).all()
    actors = [actor.short() for actor in actors_query]

    return jsonify({
        "success": True,
        "actors": actors
    }), 200

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
