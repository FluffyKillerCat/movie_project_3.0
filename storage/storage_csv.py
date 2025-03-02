from storage.istorage import IStorage
import csv
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')


class StorageCsv(IStorage):
    def __init__(self, filename, db_dir='Database'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(os.path.dirname(script_dir), db_dir)  # Move up one level
        self._db_path = os.path.join(base_path, filename)

        if not os.path.isfile(self._db_path):
            with open(self._db_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Rating", "Year", "Poster"])

        self._data = {"Movies": {}}
        with open(self._db_path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                title, rating, year, poster = row["title"], row["rating"], row["year"], row["poster"]
                self._data["Movies"][title] = {"rating": rating, "year": year, "poster": poster}

    def list_movies(self):
        if self._data['Movies']:
            return self._data
        else:
            raise ValueError('Database is empty')

    def add_movie(self, title):
        try:
            response = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")
            new_movie = response.json()

            if "Title" not in new_movie:
                raise ValueError("Movie not found")

            new_movie_title = new_movie['Title']
            new_movie_rating = new_movie['imdbRating']
            new_movie_year = new_movie['Year']
            new_movie_poster = new_movie['Poster']

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Connection error, please try again later. More info: {e}")

        self._data['Movies'][new_movie_title] = {'rating': new_movie_rating, 'year': new_movie_year,
                                                 'poster': new_movie_poster}
        self._save_data()

    def delete_movie(self, title):
        if title in self._data['Movies']:
            del self._data['Movies'][title]
            self._save_data()
        else:
            raise ValueError('Movie not found')

    def update_movie(self, title, rating):
        if title in self._data['Movies']:
            self._data['Movies'][title]['rating'] = rating
            self._save_data()
        else:
            raise ValueError('Movie not found')

    def search_movie(self, query):
        return [title for title in self._data['Movies'] if query.lower() in title.lower()]

    def _save_data(self):
        with open(self._db_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["title", "rating", "year", "poster"])
            for title, details in self._data['Movies'].items():
                writer.writerow([title, details['rating'], details['year'], details['poster']])
