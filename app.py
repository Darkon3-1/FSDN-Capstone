import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth
from datetime import datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    # db_drop_and_create_all()

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Helper functions
    def return_json(db_object, table_type):
        try:
            items = [items.format() for items in db_object]
        except Exception:
            items = db_object.format()
        if len(items) == 0:
            abort(404)
        data = {
            "success": True,
            table_type: items
        }
        return jsonify(data), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def movies_get_all(payload):
        '''
            Gets all the movies
        '''
        movies_raw = Movie.query.all()
        return return_json(movies_raw, 'Movies')

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('read:movies')
    def movies_get(payload, movie_id):
        '''
            Gets the movie based on movie_-d
        '''
        movie_raw = Movie.query.filter(Movie.id == movie_id).first()
        return return_json(movie_raw, 'Movies')

    @app.route('/movies/<int:actor_id>/actors', methods=['GET'])
    @requires_auth('read:movies')
    def movies_get_actors(payload, actor_id):
        '''
            Gets all the movies with the actor in it
        '''
        movies_raw = Movie.query.filter(Movie.actor_id == actor_id)
        return return_json(movies_raw, 'Movies')

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def movies_patch(payload, movie_id):
        '''
            Updates a movie
        '''
        try:
            data = request.get_json()

            movie = Movie.query.filter(Movie.id == movie_id).first()

            release_date = data.get('release_date', None)
            title = data.get('title', None)
            actor_id = data.get('actor_id', None)

            if release_date:
                date_f = '%a, %b %d %Y'
                movie.release_date = datetime.strptime(release_date, date_f)

            if title:
                movie.title = title

            if actor_id:
                movie.actor_id = actor_id

            movie.update()
        except Exception as e:
            abort(404, "Movie not found")
        else:
            return jsonify({
                'success': True,
                'movie': Movie.format(movie)
                })

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def movies_post(payload):
        '''
            adds a movie
        '''
        try:
            data = request.get_json()

            release_date = data['release_date']
            title = data['title']
            actor_id = data['actor_id']

            new_movie = Movie(
                title=title,
                release_date=datetime.strptime(release_date, '%a, %b %d %Y'),
                actor_id=actor_id
            )

            new_movie.insert()
        except Exception:
            abort(422, 'Missing values')
        else:
            return jsonify({
                'success': True,
                'movie': new_movie.format()
                })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def movies_delete(payload, movie_id):
        '''
            Deletes a movie
        '''
        try:
            movie = Movie.query.find(Movie.id == movie_id).first()
            movie.delete()
        except Exception:
            abort(404, 'Movie not found')
        else:
            return jsonify({
                    'success': True,
                    'delete': movie_id
                })

    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def actors_get_all(payload):
        '''
            Gets all the actors
        '''
        actors_raw = Actor.query.all()
        return return_json(actors_raw, 'Actors')

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('read:actors')
    def actors_get(payload, actor_id):
        '''
            Gets actor based on id
        '''
        actor_raw = Actor.query.filter(Actor.id == actor_id).first()
        return return_json(actor_raw, 'Actors')

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def actors_patch(payload, actor_id):
        '''
            updates actor
        '''
        try:
            data = request.get_json()

            actor = Actor.query.filter(Actor.id == actor_id).first()

            age = data.get('age', None)
            gender = data.get('gender', None)
            name = data.get('name', None)

            if age:
                actor.age = age

            if gender:
                actor.gender = gender

            if name:
                actor.name = name

            actor.update()
        except Exception:
            abort(404, "Actor not found")
        else:
            return jsonify({
                'success': True,
                'actor': Actor.format(actor)
                })

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def actors_post(payload):
        '''
            adds new actor
        '''
        try:
            data = request.get_json()

            age = data['age']
            gender = data['gender']
            name = data['name']

            new_actor = Actor(
                age=age,
                gender=gender,
                name=name
            )

            new_actor.insert()
        except Exception:
            abort(422, 'Missing values')
        else:
            return jsonify({
                'success': True,
                'actor': new_actor.format()
                })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def actors_delete(payload, actor_id):
        '''
            deletes an actor
        '''
        try:
            actor = Actor.query.find(Actor.id == actor_id).first()
            actor.delete()
        except Exception:
            abort(404, 'Actor not found')
        else:
            return jsonify({
                    'success': True,
                    'delete': actor_id
                })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": str(error)
                        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": str(error)
                        }), 404

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
                    "success": False,
                    "error": AuthError.status_code,
                    "message": AuthError.error
                }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
