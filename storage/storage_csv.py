from storage.istorage import IStorage
import csv
import os
class StorageCsv(IStorage):
    def __init__(self, filename, db_dir='Database'):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(os.path.dirname(script_dir), db_dir)  # Move up one level
        db_path = os.path.join(base_path, filename)

        with open(db_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)


        fields = next(csv_reader)
        self._data = {'Movies': {}}
        for row in csv_reader:
            row = list(row)
            title, rating, year = row.split(',')
            self._data['Movies'][title] = {'year': year, 'rating': rating}





    def list_movies(self):
        """
            Returns a dictionary of dictionaries that
            contains the movies information in the database.

            The function loads the information from the JSON
            file and returns the data.

            For example, the function may return:
            {
              "Titanic": {
                "rating": 9,
                "year": 1999
              },
              "..." {
                ...
              },
            }
            """

        return self._data['Movies']


    def add_movie(self, title, year, rating, poster):
        """
            Adds a movie to the movies database.
            Loads the information from the JSON file, add the movie,
            and saves it. The function doesn't need to validate the input.
        """

        self._data['Movies'][title] = {'year': int(year), 'rating': int(rating), 'poster': poster}

    def delete_movie(self, title):
        """
           Deletes a movie from the movies database.
           Loads the information from the JSON file, deletes the movie,
           and saves it. The function doesn't need to validate the input.
        """

        del self._data['Movies'][title]

    def update_movie(self, title, rating):
        """
            Updates a movie from the movies database.
            Loads the information from the JSON file, updates the movie,
            and saves it. The function doesn't need to validate the input.
        """

        self._data['Movies'][title]['rating'] = rating