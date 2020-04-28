import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db_drop_and_create_all
from sqlalchemy import desc
from datetime import date

bearer_tokens = {
    "casting_assistant" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRGMFB4M3A3ckI3S3h3cmk2bktreiJ9.eyJpc3MiOiJodHRwczovL3NydGtvb2xpY2UuYXV0aDAuY29tLyIsInN1YiI6IkZDeHhRTTZ1TEZna3pqcnk1VGFLMW9CRFFEVGhHVG1iQGNsaWVudHMiLCJhdWQiOiJ1ZGFjaXR5LWNhcHN0b25lIiwiaWF0IjoxNTg4MDI2ODc2LCJleHAiOjE1OTA2MTg4NzYsImF6cCI6IkZDeHhRTTZ1TEZna3pqcnk1VGFLMW9CRFFEVGhHVG1iIiwic2NvcGUiOiJyZWFkOm1vdmllcyByZWFkOmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInJlYWQ6bW92aWVzIiwicmVhZDphY3RvcnMiXX0.BIPxeSX9bCidde8xl64AznZPMYvQdKU-hUBhS6vj6gwsYpmnPnLzGMuWX9RwrzsSaMNgTgkFZ1gFDpqyNuLA8pt1yuDxbAhXQCB_akYw2QvDcY95wsBEGqq3wgE8I82HzmgGe94qZjG8SqcytCuAvMu1GP19Vi_hs7dkiD_Ix_S7SICYcnjcrMFSn5PIe721rSG7eRmr7JM5fDoZo8uz4Y2g6oLKY0D9b6SC9A7YD3pfDBAdnCtd41aEphkJ-Rxz7EME4ogYQ8kWehQjlb_pmWGU44rU771hunWJeqQV2do72IVfxDNoD7a36FjfBPCZlLkPZxjPc8lQpkcti2yVUw",
    "casting_director" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRGMFB4M3A3ckI3S3h3cmk2bktreiJ9.eyJpc3MiOiJodHRwczovL3NydGtvb2xpY2UuYXV0aDAuY29tLyIsInN1YiI6IkxCVFZoaW1TWTNuM1Y4UE9QYlcySVpYcXVCMUd0VGV2QGNsaWVudHMiLCJhdWQiOiJ1ZGFjaXR5LWNhcHN0b25lIiwiaWF0IjoxNTg4MDI2OTk2LCJleHAiOjE1OTA2MTg5OTYsImF6cCI6IkxCVFZoaW1TWTNuM1Y4UE9QYlcySVpYcXVCMUd0VGV2Iiwic2NvcGUiOiJyZWFkOm1vdmllcyB1cGRhdGU6bW92aWVzIGRlbGV0ZTphY3RvcnMgcmVhZDphY3RvcnMgdXBkYXRlOmFjdG9ycyBhZGQ6YWN0b3JzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsicmVhZDptb3ZpZXMiLCJ1cGRhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsInJlYWQ6YWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsImFkZDphY3RvcnMiXX0.Z-Jw2u8Vzx-sSj0GVaOOu1Bn8lHoHU-DUfwqHQ-Mmyx9oetjl1FMn3xZhtLZ55U1v6oaSMd1-dgI-27MOstVfkHPZO6FHH-Bptz5x4hrxJp63uVvOJlQIxE7E0Emii_4C1SUtMA2OmqftLTsVviO-sIa3axz-cBgC2XWaMmPO_lbYYT1_9lqPIUO1rR5vPB_evOxMv82Ope6qqdlHWVQx4kttr5pZ2KTt_usfud4g4wKEwu_AalX40cmXw8Op1eDSHXdgA1wGXDEv-25EiMMTtyX7923iOa1y0xP3hRzENn4IDLBQTkTP2q9zJucDyog9BrMZ-xUAUbDfFGVgJJV0g",
    "executive_producer" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRGMFB4M3A3ckI3S3h3cmk2bktreiJ9.eyJpc3MiOiJodHRwczovL3NydGtvb2xpY2UuYXV0aDAuY29tLyIsInN1YiI6IklpSExndlp2NENDT1picG9IcGNYQ0pOcU5uS3VOUVZVQGNsaWVudHMiLCJhdWQiOiJ1ZGFjaXR5LWNhcHN0b25lIiwiaWF0IjoxNTg4MDI3MDYwLCJleHAiOjE1OTA2MTkwNjAsImF6cCI6IklpSExndlp2NENDT1picG9IcGNYQ0pOcU5uS3VOUVZVIiwic2NvcGUiOiJkZWxldGU6bW92aWVzIHJlYWQ6bW92aWVzIHVwZGF0ZTptb3ZpZXMgYWRkOm1vdmllcyBkZWxldGU6YWN0b3JzIHJlYWQ6YWN0b3JzIHVwZGF0ZTphY3RvcnMgYWRkOmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptb3ZpZXMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTptb3ZpZXMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsInJlYWQ6YWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsImFkZDphY3RvcnMiXX0.GYggzM_VJiMB1Ty0JbtDBST_Cfa9mybV715yVwH7aNBZrZ-Em8QgkAKc_l1HKXoCXKV8oRJLmb5Uuiir8nQEb8MyF0X92lzi64GI2CHJvbwmXIol9E78W4uv4ylIqDM506tsacUE9JP8nBmRxDb0gZ0lik2IhxkhR7eAyJ9vDEcIHvcjI9Rf6iWmMRP4c3IE5FtOIufRbyEXR_hqGkhzRIysr0M0zXyOZOdaBckn1mKfQ0FaxXkj2w8AEO96Z6rzxoDcpFGhLHmAThveAajosAzEz_J25PcLeMTAK2ggIa03s1jA7hPlbsz_6FouVwofJUIK3GoaJV3STgqjBs9ezA"
}

assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

#############################################################
######################## Movies #############################
#############################################################

######################## GET #############################
    def test_get_all_movies(self):
        res = self.client().get('/movies/2/actors', headers = assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['Movies']) > 0)
        self.assertTrue(data['success'])

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers = assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['Movies']) > 0)
        self.assertTrue(data['success'])

    def test_get_all_movies_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Missing Authorization header.')

    def test_get_movies_404(self):
        res = self.client().get('/movies/50', headers = assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , '404 Not Found: No Movies found')

######################## POST #############################
    def test_post_movie(self):
        new_movie = {
            'title' : 'late night writing code',
            'release_date' : 'Wed, Apr 23 2006',
            'actor_id': 2
        }

        res = self.client().post('/movies', json = new_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['id'], 4)

    def test_post_movie_422(self):
        new_movie = {
            'release_date' : 'Wed, Apr 23 2006'
        }

        res = self.client().post('/movies', json = new_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], '422 Unprocessable Entity: Missing values')

######################## PATCH #############################
    def test_patch_movie(self):
        json_edit_movie = {
            'release_date' : 'Wed, Apr 23 2006'
        }
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_patch_movie_404(self):
        json_edit_movie = {
            'release_date' : 'Wed, Apr 23 2006'
        }
        res = self.client().patch('/movies/5', json = json_edit_movie, headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , '404 Not Found: Movie not found')

######################## DELETE #############################
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['delete'], 1)

    def test_delete_movie_401(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Missing Authorization header.')

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/5', headers = producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , '404 Not Found: Movie not found')

#############################################################
######################## Actors #############################
#############################################################

######################## GET #############################
    def test_get_all_actors(self):
        res = self.client().get('/actors', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['Actors']) > 0)

    def test_get_all_movies(self):
        res = self.client().get('/actors/5/movies', headers = assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , '404 Not Found: No Movies found')


    def test_get_all_actors_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Missing Authorization header.')

    def test_get_actors_404(self):
        res = self.client().get('/actors/4', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , '404 Not Found: No Actors found')

######################## POST #############################
    def test_post_actor(self):
        new_actor = {
            'name' : 'Billy',
            'gender': 'male',
            'age' : 20
        }

        res = self.client().post('/actors', json = new_actor, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['id'], 4)

    def test_post_401(self):
        new_actor = {
            'name' : 'Billy',
            'gender': 'male',
            'age' : 20
        }

        res = self.client().post('/actors', json = new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Missing Authorization header.')

    def test_post_actor_422(self):
        new_actor = {
            'name': 'Billy',
            'age' : 20
        }

        res = self.client().post('/actors', json = new_actor, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], '422 Unprocessable Entity: Missing values')

######################## PATCH #############################
    def test_patch_actor(self):
        json_edit_actor_with_new_age = {
            'age' : 34
        }
        res = self.client().patch('/actors/1', json = json_edit_actor_with_new_age, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['actor']['id'], 1)

    def test_patch_actor_404(self):
        json_edit_actor_with_new_age = {
            'age' : 30
        }
        res = self.client().patch('/actors/5', json = json_edit_actor_with_new_age, headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , '404 Not Found: Actor not found')

######################## POST #############################
    def test_delete_actor_401(self):
        res = self.client().delete('/actors/1', headers = assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permissions not in JWT.')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['delete'], 1)

    def test_error_404_delete_actor(self):
        res = self.client().delete('/actors/4', headers = director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , '404 Not Found: Actor not found')

if __name__ == "__main__":
    unittest.main()