from storage.istorage import IStorage
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

class StorageJson(IStorage):
    def __init__(self, filename, db_dir='Database'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(os.path.dirname(script_dir), db_dir)
        self._db_path = os.path.join(base_path, filename)

        if not os.path.exists(self._db_path):
            with open(self._db_path, "w") as f:
                f.write('{}')

        with open(self._db_path) as fileobj:
            try:
                self._data = json.load(fileobj)
            except json.JSONDecodeError:
                self._data = {'Movies': {}}

    def list_movies(self):
        return self._data

    def add_movie(self, title):
        try:
            data = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")
            new_movie = data.json()
            new_movie_title = new_movie['Title']
            new_movie_rating = new_movie['imdbRating']
            new_movie_year = new_movie['Year']
            new_movie_poster = new_movie['Poster']
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f'Connection error, please try again later. More information: {e}')
        except KeyError:
            raise ValueError('Movie Not Found')

        self._data['Movies'][new_movie_title] = {'rating': new_movie_rating, 'year': new_movie_year, 'poster': new_movie_poster}

        with open(self._db_path, 'w') as json_file:
            json.dump(self._data, json_file, indent=4)

    def delete_movie(self, title):
        if title in self._data['Movies']:
            del self._data['Movies'][title]
            with open(self._db_path, 'w') as json_file:
                json.dump(self._data, json_file, indent=4)
        else:
            raise ValueError('Movie Not Found')

    def update_movie(self, title, rating):
        self._data['Movies'][title]['rating'] = rating
        with open(self._db_path, 'w') as json_file:
            json.dump(self._data, json_file, indent=4)

    def search_movie(self, query):
        pos_movies = [movie for movie in self._data['Movies'] if query.lower() in movie.lower()]
        return pos_movies
