class MovieApp:
    """Color Constants"""
    RESET = "\033[0m"  # Normal Color, needed to revert back after changing color (Can be used in f string to revert)
    # List of colors used here; for more colors  https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    def __init__(self, storage):
        self._storage = storage


    def _command_list_movies(self):
        movies = self._storage.list_movies()
        if movies:
            for movie in movies:
                print(f"{movie} ({movies['Movies'][movie]['year']}): {movies['Movies'][movie]['rating']}")
        else:
            raise ValueError('Database is empty, please add movies')



    def _command_movie_stats(self):
        stats = 1

    def _generate_website(self):
        pass

    def run(self):

        print(f"""

           {MovieApp.CYAN}********** My Movies Database **********{MovieApp.RESET}

        Menu:
        0. {MovieApp.GREEN}Exit{MovieApp.RESET}
        1. {MovieApp.GREEN}List movies{MovieApp.RESET}
        2. {MovieApp.GREEN}Add movie{MovieApp.RESET}
        3. {MovieApp.GREEN}Delete movie{MovieApp.RESET}
        4. {MovieApp.GREEN}Update movie{MovieApp.RESET}
        5. {MovieApp.GREEN}Stats{MovieApp.RESET}
        6. {MovieApp.GREEN}Random movie{MovieApp.RESET}
        7. {MovieApp.GREEN}Search movie{MovieApp.RESET}
        8. {MovieApp.GREEN}Movies sorted by rating{MovieApp.RESET}
        9. {MovieApp.GREEN}Movies sorted by year{MovieApp.RESET}
        10. {MovieApp.GREEN}Filter Movies{MovieApp.RESET}
        11. {MovieApp.GREEN}Create Rating Histogram{MovieApp.RESET}


        """)
        while True:

            user_input = input(f"{MovieApp.CYAN}Enter choice (0-11):  {MovieApp.RESET}")
            if user_input.lower() == 'exit()':
                exit()

            if user_input.isdigit():
                user_command = int(user_input)
                if 0 <= user_command <= 11:

                    if user_command == 1:




                else:
                    print(f'{MovieApp.RED}!!!Please enter a valid choice!!!{MovieApp.RESET}\n')





from storage.storage_json import StorageJson

storage = StorageJson('package.json')
movie_app = MovieApp(storage)
movie_app.run()