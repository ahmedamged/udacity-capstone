Motivation for the project

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

Start with installing all the required packages to your machine

```bash
pip install -r requirements.txt
```

Create a database an call it `udacitycapstone` and change the DATABASE_URL in setup file to have your Postgres user and password then run these commands in your terminal

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

Deployed Web app link

*https://final-capstone-fsnd.herokuapp.com*

To test the endpoints, use the JWT tokens provided in setup file for each role and use Postman to test them.

GET *https://final-capstone-fsnd.herokuapp.com/actors*

GET *https://final-capstone-fsnd.herokuapp.com/movies*

POST *https://final-capstone-fsnd.herokuapp.com/actors*

POST *https://final-capstone-fsnd.herokuapp.com/movies*

PATCH *https://final-capstone-fsnd.herokuapp.com/actors/3*

PATCH *https://final-capstone-fsnd.herokuapp.com/actors/3*

DELETE *https://final-capstone-fsnd.herokuapp.com/movies/2*

DELETE *https://final-capstone-fsnd.herokuapp.com/movies/2*

### Endpoints:
* GET /actors and /movies
* DELETE /actors/ and /movies/
* POST /actors and /movies and
* PATCH /actors/ and /movies/

### Models:
* Movies
  * title
  * release date
* Actors
  * name
  * age
  * gender
