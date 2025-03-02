from app.movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv

def main():
    storage_type = input("Enter storage type (json/csv): ").strip().lower()

    if storage_type == "json":
        storage = StorageJson('movies.json')
    elif storage_type == "csv":
        storage = StorageCsv('package.csv')
    else:
        print("Invalid storage type. Please choose 'json' or 'csv'.")
        return

    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()
