# FSND: Capstone Project
## Content
1.  [Motivation](#motivations)

2.  [Start Project locally](#start-project-locally)

3.  [Base URL](#base-url)

4.  [API Documentation](#endpoints)

5.  [Authentification](#authentification)

## Motivations

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course. For which I wanted to make sure my skills were up to date.

It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)

2. API to performance CRUD Operations on database with `Flask` (see `app.py`)

3. Automated testing with `Unittest` (see `test_app`)

4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)

5. Deployment on `Heroku`

## Start Project locally
Clone repository into a local folder.
Reqs: Python 3

To start and run the local development server,

1. Initialize, activate a virtualenv, and install dependencies:

```
virtualenv venv
source venv/scripts/activate
pip install -r requirements.txt
```
With the project being locally, we can setup a sqllite database



3. Change database config so it can connect to your local postgres database
    - Open `models.py` with your editor of choice.
    - Make sure the following lines are setup correctly for local
```
 7 # If run locally, uncomment the following below
 8 database_filename = "database.db"
 9 project_dir = os.path.dirname(os.path.abspath(__file__))
10 database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
11
12 # For running on Prod
13 #database_path = os.environ['DATABASE_URL']
```
4. Setup an account with Auth0 for permissions

5. Start the server:

```
$ python app.py
```

## API Documentation
In this next section, you will find all the endpoints for the project and requirements

### Base URL

**_https://udacity-capstone-dlee.herokuapp.com/_**

### Authentification

Please see [API Authentification](#authentification-bearer)



### Endpoints


### How to work with each endpoint



Click on a link to directly get to the ressource.


1. Movies
    -  [GET /movies](#get-'/movies')
    -  [GET /movies/movie_id](#get-'/movies/movie_id')
    -  [GET /movies/actor_id/actors](#get-'/movies/actor_id/actors')
    -  [POST /movies](#post-'/movies')
    -  [DELETE /movies/movie_id](#delete-'/movies/movie_id')
    -  [PATCH /movies/movie_id](#patch-'/movies/movie_id')

2. Actors
    -  [GET /actors](#get-'/actors')
    -  [GET /actors/actor_id](#get-'/actors/actor_id')
    -  [POST /actors](#post-'/actors')
    -  [DELETE /actors/actor_id](#delete-'/actors/actor_id')
    -  [PATCH /actors/actor_id](#patch-'/actors/actor_id')

##### GET '/movies'
- Fetches an array of movies that are in the DB
- Request Arguments: None
- Returns: An object with a single key, Movies, that contains a object of actor, id, release_date, title
```
{
    "Movies": [
        {
            "actor": {
                "id": 2,
                "name": "Chris"
            },
            "id": 1,
            "release_date": "Sat, Apr 29 2017",
            "title": "Raids of the ice"
        },
        {
            "actor": {
                "id": 3,
                "name": "Katie"
            },
            "id": 2,
            "release_date": "Sat, Apr 29 2017",
            "title": "up up and away"
        },
        {
            "actor": {
                "id": 3,
                "name": "Katie"
            },
            "id": 3,
            "release_date": "Sat, Apr 29 2017",
            "title": "finding katie"
        }
    ],
    "success": true
}
```
##### GET '/movies/movies_id'
- Fetches a dictionary of a movie (same structure as GET /movies)
- Request Arguments: None
- Returns: An object with 4 keys, actor, id, release_date, and title.
    * actor id:id of actor name:name of actor
    * relase_date: release date of movie
    * title: title of movie
    * id: id of movie
```
{
    "Movies": {
        "actor": {
            "id": 3,
            "name": "Katie"
        },
        "id": 2,
        "release_date": "Sat, Apr 29 2017",
        "title": "up up and away"
    },
    "success": true
}
```

##### GET '/movies/actor_id/actors'
- Gets all the movies with said actor
- Request Arguments: actor_id
- Returns: Same as GET /movies
'''
{
    "Movies": [
        {
            "actor": {
                "id": 3,
                "name": "Katie"
            },
            "id": 2,
            "release_date": "Sat, Apr 29 2017",
            "title": "up up and away"
        },
        {
            "actor": {
                "id": 3,
                "name": "Katie"
            },
            "id": 3,
            "release_date": "Sat, Apr 29 2017",
            "title": "finding katie"
        }
    ],
    "success": true
}
'''

##### POST '/movies'
- Adds a movie
- Request Arguments: title, release_date, actor_id
- Returns: dict indicating success with movie inserted
```
{
  "movie": {
    "actor": {
      "id": 2,
      "name": "Chris"
    },
    "id": 4,
    "release_date": "Sun, Apr 23 2006",
    "title": "late night writing code"
  },
  "success": "True"
}
```

##### DELETE '/movies/movie_id'
- Deletes a movie based on `movie_id` sent
- Request Arguments: movie_id
- Returns: None

##### PATCH '/movies/<int:movie_id>'
- Updates a movie with `movie_id`
- Request Arguments: one of the two title, release_date
- Returns: dict [Get '/movies](####GET-'/movies')
```
{
  "movie": {
    "actor": {
      "id": 2,
      "name": "Chris"
    },
    "id": 1,
    "release_date": "Sun, Apr 23 2006",
    "title": "Raids of the ice"
  },
  "success": "True"
}
```
##### GET '/actors'
- Gets all the actors in the DV
- Request Arguments: Nonoe
- Returns: dict with key:Actors with an array of dicts of actors keys: age, gender, id, name
```
{
    "Actors": [
        {
            "age": 45,
            "gender": "male",
            "id": 1,
            "name": "David"
        },
        {
            "age": 35,
            "gender": "male",
            "id": 2,
            "name": "Chris"
        },
        {
            "age": 30,
            "gender": "female",
            "id": 3,
            "name": "Katie"
        }
    ],
    "success": true
}
```
##### GET '/actors/actor_id'
- Gets an actor based on actor_id
- Request Arguments: actor_id
- Returns: see GET /actors(####GET-'/actors')
'''
{
    "Actors": {
        "age": 35,
        "gender": "male",
        "id": 2,
        "name": "Chris"
    },
    "success": true
}
'''

##### POST '/actors'
- Adds an actor based on the arguments
- Request Arguments: age, gender, name
- Returns: see GET /actors(####GET-'/actors')
'''
{
    "Actors": {
        "age": 40,
        "gender": "male",
        "id": 2,
        "name": "Billy"
    },
    "success": true
}
'''

##### DELETE '/actors/actor_id'
- Delete actor based on id
- Request Arguments: actor_id
- Returns: None

##### PATCH '/actors/actor_id'
- updates an actor based on the arguments
- Request Arguments: age, gender, or name
- Returns: see GET /actors(####GET-'/actors')
'''
{
    "Actors": {
        "age": 20,
        "gender": "male",
        "id": 2,
        "name": "Bill"
    },
    "success": true
}
'''
 ## Error Handling
```
{
  'success': False,
  'error': 404,
  'message': error_message
}
```
Api will return the following error
- 404: not found
- 422: Unprocessable Entity

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (get:actors): Can see all actors
  - GET /movies/actor_id/actors (get:movies): Can see all movies with actor
  - GET /movies (get:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (post:actors): Can create new Actors
  - PATCH /actors (patch:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (patch:movies): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (post:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

## Authentification Bearer
For example: (Bearer token for `Executive Producer`)
```
{
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRGMFB4M3A3ckI3S3h3cmk2bktreiJ9.eyJpc3MiOiJodHRwczovL3NydGtvb2xpY2UuYXV0aDAuY29tLyIsInN1YiI6IklpSExndlp2NENDT1picG9IcGNYQ0pOcU5uS3VOUVZVQGNsaWVudHMiLCJhdWQiOiJ1ZGFjaXR5LWNhcHN0b25lIiwiaWF0IjoxNTg4MDI3MDYwLCJleHAiOjE1OTA2MTkwNjAsImF6cCI6IklpSExndlp2NENDT1picG9IcGNYQ0pOcU5uS3VOUVZVIiwic2NvcGUiOiJkZWxldGU6bW92aWVzIHJlYWQ6bW92aWVzIHVwZGF0ZTptb3ZpZXMgYWRkOm1vdmllcyBkZWxldGU6YWN0b3JzIHJlYWQ6YWN0b3JzIHVwZGF0ZTphY3RvcnMgYWRkOmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptb3ZpZXMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTptb3ZpZXMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsInJlYWQ6YWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsImFkZDphY3RvcnMiXX0.GYggzM_VJiMB1Ty0JbtDBST_Cfa9mybV715yVwH7aNBZrZ-Em8QgkAKc_l1HKXoCXKV8oRJLmb5Uuiir8nQEb8MyF0X92lzi64GI2CHJvbwmXIol9E78W4uv4ylIqDM506tsacUE9JP8nBmRxDb0gZ0lik2IhxkhR7eAyJ9vDEcIHvcjI9Rf6iWmMRP4c3IE5FtOIufRbyEXR_hqGkhzRIysr0M0zXyOZOdaBckn1mKfQ0FaxXkj2w8AEO96Z6rzxoDcpFGhLHmAThveAajosAzEz_J25PcLeMTAK2ggIa03s1jA7hPlbsz_6FouVwofJUIK3GoaJV3STgqjBs9ezA"
}
```
