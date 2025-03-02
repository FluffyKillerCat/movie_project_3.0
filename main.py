from app.movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv

storage = StorageCsv('package.csv')
movie_app = MovieApp(storage)
movie_app.run()