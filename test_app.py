import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

CASTING_ASSISTANT_JWT='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIcFhZN2ZaanMwNEVSeVpzY0loaiJ9.eyJpc3MiOiJodHRwczovL2FtZ2VkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGY1NzZkZTgwYzk5ODAwNjgyMDQ0YmUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyOTUyNzY5NiwiZXhwIjoxNjI5NTM0ODk2LCJhenAiOiJDcmVxYnNsNjkzdmNoZ1psUGFoNVRmQ0ROOFh0R0xYQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.ihpb4Mg6jyC6qo5XA-kBlPK0kKsY_RaCsnbA3gJEmZ-Yl-HKgVPI8oOiP4MIFMH0wVluBKw_eomnfudbbaLb5Xa1mijs9PoxLHTctWViEGQzwZTQ2xS6bxi4caQBnY5X6p-SqlE21jSkBpirucIN4EVH7VleYyW7BruMM5PA1E5RUChoGLutb_3TjBC8QsbBh9zbTALOWR-zpk8qEK0ycrXzGCtxDXrQGjtjqnuI7Ux-uoljbpxZMtX9qOlXLGTH4L3rcXzHhup3-ElX3gu2AqETs_zIQ93VoB9dycoIcy8_PGX_QdWQu_nMVM-LL8KM5oDpfe1uTRfZs30-5a6WHg'
EXECUTIVE_PRODUCER_JWT='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIcFhZN2ZaanMwNEVSeVpzY0loaiJ9.eyJpc3MiOiJodHRwczovL2FtZ2VkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGY4MTExNGM2MWZkNzAwNzdjZWEwYzciLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyOTUyNzc2MCwiZXhwIjoxNjI5NTM0OTYwLCJhenAiOiJDcmVxYnNsNjkzdmNoZ1psUGFoNVRmQ0ROOFh0R0xYQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIl19.gqqdOSCaqClb1x0S_EF0UyitfpQK19xpiDDSvsNZCAVBk6e48XYVtC4rOTOrmUVyHSAnHiU7cAHLTEObMPbgQkYgDukFRC4w2BMsqZJlfsFIPgnaje9tbBbLvB6sezyyU2R5mmsoX_ATcVi9XebyYbKv9MRAQW8aXLRl3o_0PzJeYQrdJFMGN3j72EUPZoUAhF--6oFJtBUcI8bHPjqaTlYNmiKl24gQiywDWp8dFSCRrK02cc2TnzLsBiT3xtvEf1_ZILvlO1LFEugP2POBP_qh84Q1II9F_ps6HVTnxgphLLMmY22fixxiwcH3xH0OQM2VObIWb5x_0aTgbeXMKQ'
CASTING_DIRECTOR_JWT='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIcFhZN2ZaanMwNEVSeVpzY0loaiJ9.eyJpc3MiOiJodHRwczovL2FtZ2VkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTFlZTUyMWQ3MjBiYzAwNjliOTEzOTYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyOTUyNzgyMCwiZXhwIjoxNjI5NTM1MDIwLCJhenAiOiJDcmVxYnNsNjkzdmNoZ1psUGFoNVRmQ0ROOFh0R0xYQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.StFzoyWbRjR0afDkIkO0Z_xx86RBCwPB7rI2qCxhR9fP9NT6XErFCQWij_iSHis9WnHMAutjI6HOeDTLyvp5l_sBQSqDiOt_vjOjILr15v0VOZz4bEdHf2WM6eKjRBlRfJmu3mmKlbfNlkNY6rVs2TsqiBdgIAC0yMBoPPIEkxQ-8yFfQCba8tbzHOG2x_wyu8ftQAcRxAGw0iTr7ouWifE7sUDwCiHYbZ3GuaBsezOcjGhhGo8BgUCgDmNDNDHPLXlFcRe53L3Z--6qlYY_t4S7OSgu2xiPLbBJwa965Nsi4su3u4DOhy3jQlNYaj3Ifq8ivLaX7TRFbIXjhPCF7w'

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "udacitycapstone"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            "postgres", "ahmed", "localhost:5432", self.database_name
        )

        setup_db(self.app)
        self.c_a_access_token={'Authorization': CASTING_ASSISTANT_JWT}
        self.c_d_access_token={'Authorization': CASTING_DIRECTOR_JWT}
        self.e_p_access_token={'Authorization': EXECUTIVE_PRODUCER_JWT}

        self.new_actor = {
            "name": "Jeremy",
            "age" : 23,
            "gender" : "male"
        }

        self.new_movie = {
            "title" : "Adrift",
            "release_date" : 2021
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_actors(self):
        res = self.client().get("/actors", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["actors"])

    def test_get_actor_not_allowed(self):
        res = self.client().get("/actors/99", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_movies(self):
        res = self.client().get("/movies", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["movies"])

    def test_get_movie_not_allowed(self):
        res = self.client().get("/movies/99", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_delete_actor(self):
        res = self.client().delete("/actors/7", headers=self.e_p_access_token)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 7).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 7)

    def test_failed_delete_actor(self):
        res = self.client().delete("/actors/99", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):
        res = self.client().delete("/movies/7", headers=self.e_p_access_token)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 7).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 7)

    def test_failed_delete_movie(self):
        res = self.client().delete("/movies/99", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_edit_actor(self):
        res = self.client().patch("/actors/8", json={"name": "Becca", "age": 22, "gender": "female"}, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated"], 8)

    def test_failed_edit_actor(self):
        res = self.client().patch('/actors/1', json={"name": "Becca", "age": 22, "gender": "female"}, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_edit_movie(self):
        res = self.client().patch('/movies/8', json={"title": "Titanic", "release_date": 2019}, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated"], 8)

    def test_failed_edit_movie(self):
        res = self.client().patch('/movies/1', json={"title": "Titanic", "release_date": 2019}, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_add_actor(self):
        res = self.client().post("/actors", json=self.new_actor, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_actors"])

    def test_add_actor_not_allowed(self):
        res = self.client().post("/actors/99", json=self.new_actor, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_add_movie(self):
        res = self.client().post("/movies", json=self.new_movie, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_movies"])

    def test_add_movie_not_allowed(self):
        res = self.client().post("/movies/99", json=self.new_movie, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

# EXECUTIVE_PRODUCER

    def test_get_actors_e_p(self):
        res = self.client().get("/actors", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["actors"])

    def test_get_movies_e_p(self):
        res = self.client().get("/movies", headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["movies"])

    def test_edit_actor_e_p(self):
        res = self.client().patch("/actors/8", json={"name": "Becca", "age": 22, "gender": "female"}, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated"], 8)

    def test_edit_movie_e_p(self):
        res = self.client().patch('/movies/8', json={"title": "Titanic", "release_date": 2019}, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated"], 8)

    def test_add_actor_e_p(self):
        res = self.client().post("/actors", json=self.new_actor, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_actors"])

    def test_add_movie_e_p(self):
        res = self.client().post("/movies", json=self.new_movie, headers=self.e_p_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_movies"])

# CASTING_DIRECTOR

    def test_get_actors_c_d(self):
        res = self.client().get("/actors", headers=self.c_d_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["actors"])

    def test_get_movies_c_d(self):
        res = self.client().get("/movies", headers=self.c_d_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["movies"])

    def test_edit_actor_c_d(self):
        res = self.client().patch("/actors/8", json={"name": "Becca", "age": 22, "gender": "female"}, headers=self.c_d_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated"], 8)

    def test_edit_movie_c_d(self):
        res = self.client().patch('/movies/8', json={"title": "Titanic", "release_date": 2019}, headers=self.c_d_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated"], 8)

    def test_add_actor_c_d(self):
        res = self.client().post("/actors", json=self.new_actor, headers=self.c_d_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_actors"])

    def test_add_movie_c_d(self):
        res = self.client().post("/movies", json=self.new_movie, headers=self.c_d_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

# CASTING_ASSISTANT

    def test_get_actors_c_a(self):
        res = self.client().get("/actors", headers=self.c_a_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["actors"])

    def test_get_movies_c_a(self):
        res = self.client().get("/movies", headers=self.c_a_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["movies"])

    def test_edit_actor_c_a(self):
        res = self.client().patch("/actors/8", json={"name": "Becca", "age": 22, "gender": "female"}, headers=self.c_a_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_edit_movie_c_a(self):
        res = self.client().patch('/movies/8', json={"title": "Titanic", "release_date": 2019}, headers=self.c_a_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_add_actor_c_a(self):
        res = self.client().post("/actors", json=self.new_actor, headers=self.c_a_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_add_movie_c_a(self):
        res = self.client().post("/movies", json=self.new_movie, headers=self.c_a_access_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

if __name__ == "__main__":
    unittest.main()
