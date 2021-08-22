#FSND: Capstone Project

Capstone project for Udacity's Full-stack Nanodegree.

###Main objectives achieved by this project

*Coding in Python 3
*Relational Database Architecture
*Modeling Data Objects with SQLAlchemy
*Internet Protocols and Communication
*Developing a Flask API
*Authentication and Access
*Authentication with Auth0
*Authentication in Flask
*Role-Based Access Control (RBAC)
*Testing Flask Applications
*Deploying Applications

###Project Setup

Start with Initializing a virtual environment

```bash
cd PROJECT_DIRECTORY_PATH
virtualenv venv
source venv/bin/activate
```

Then install all the required packages to your machine

```bash
pip install -r requirements.txt
```

Create a database and call it `udacitycapstone` and change the DATABASE_URL in setup file to have your Postgres user and password then run these commands in your terminal

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Run the development server

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --reload
```

###Deployed app link on Heroku

*https://final-capstone-fsnd.herokuapp.com*

To test the endpoints, use the JWT tokens provided in setup file for each role and use Postman to test them or use the Postman collection provided.

### Endpoints:

GET */actors*
Returns a list of all the actors stored in the database

GET */movies*
Returns a list of all the movies stored in the database

POST */actors*
Add a new actor to the database

POST */movies*
Add a new movie to the database

PATCH */actors/3*
Edits the actor with id 3 from the database

PATCH */movies/3*
Edits the movie with id 3 from the database

DELETE */actors/2*
Deletes the actor with id 2 from the database

DELETE */movies/2*
Deletes the movie with id 2 from the database

### Models:
* Movies
  * title
  * release date
* Actors
  * name
  * age
  * gender

### Roles:
* CASTING_ASSISTANT
  * Can view actors
  * Can view movies
  * Can't add an actor
  * Can't add a movie
  * Can't delete an actor
  * Can't delete a movie
  * Can't edit an actor
  * Can't edit a movie


* CASTING_DIRECTOR
  * Can view actors
  * Can view movies
  * Can add an actor
  * Can't add a movie
  * Can delete an actor
  * Can't delete a movie
  * Can edit an actor
  * Can edit a movie


* EXECUTIVE_PRODUCER
  * Can view actors
  * Can view movies
  * Can add an actor
  * Can add a movie
  * Can delete an actor
  * Can delete a movie
  * Can edit an actor
  * Can edit a movie
