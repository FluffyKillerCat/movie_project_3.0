from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
import random
from sf.sf import SF
import os
class MovieApp:
    """A class to manage a movie database with various functionalities.

    Color Constants for terminal text coloring.
    """
    RESET = "\033[0m"  # Normal Color, needed to revert back after changing color (Can be used in f string to revert)
    # List of colors used here; for more colors  https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"

    def __init__(self, storage):
        """Initialize the MovieApp with a storage object."""
        self._storage = storage
        self._movies = self._storage.list_movies()

    def _command_list_movies(self) -> None:
        """List all movies in the database."""
        self._print_movies(self._movies['Movies'].keys())


    def _print_movies(self, movies):
        """Print movies with their details.
        """
        if movies:
            for movie in movies:
                print(f"{movie} ({self._movies['Movies'][movie]['year']}): {self._movies['Movies'][movie]['rating']}")
        else:
            raise ValueError('No Movies to show right now')

    def _command_movie_stats(self) -> None:
        """Calculate and print average, median, best, and worst movie ratings."""
        if len(self._movies['Movies']) > 0:
            ratings = sorted(float(self._movies['Movies'][movie]['rating']) for movie in self._movies['Movies'])
            num_of_movies = len(ratings)

            average_rating = sum(ratings) / num_of_movies

            if num_of_movies % 2 != 0:
                median_rating = ratings[num_of_movies // 2]
            else:
                median_rating = sum(ratings[num_of_movies // 2 - 1:num_of_movies // 2 + 1]) / 2

            best_rating = max(ratings)
            worst_rating = min(ratings)

            best_rated_movies = [name for name, movie in self._movies['Movies'].items() if float(movie['rating']) == best_rating]
            worst_rated_movies = [name for name, movie in self._movies['Movies'].items() if float(movie['rating']) == worst_rating]

            print(f'{MovieApp.GREEN}Average rating: {average_rating:.1f}{MovieApp.RESET}')
            print(f'{MovieApp.GREEN}Median rating: {median_rating:.1f}{MovieApp.RESET}')
            print(f'{MovieApp.GREEN}Best movies: {", ".join(best_rated_movies)}, {best_rating}{MovieApp.RESET}')
            print(f'{MovieApp.RED}Worst movies: {", ".join(worst_rated_movies)}, {worst_rating}{MovieApp.RESET}')
        else:
            raise ValueError('Cannot get stats on an empty DB')

    def _generate_website(self):
        """function for website generation method."""
        movie_grid = ""
        self._movies = self._storage.list_movies()

        for title, details in self._movies['Movies'].items():
            movie_grid += f'''
                <li class="movie-item">
                    <img src="{details['poster']}" alt="{title} Poster">
                    <div class="movie-info">
                        <h2>{title}</h2>
                        <p>Year: {details['year']}</p>
                        <p>Rating: {details['rating']}</p>
                    </div>
                </li>
                '''
        db_dir = 'template'

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(os.path.dirname(script_dir), db_dir)  # Move up one level
        db_path = os.path.join(base_path, 'index.html')
        with open(db_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        updated_html = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)


        db_dir = '_static'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(os.path.dirname(script_dir), db_dir)  # Move up one level
        db_path = os.path.join(base_path, 'index.html')

        with open(db_path, "w", encoding="utf-8") as file:
            file.write(updated_html)
            print("HTML file updated successfully!")




    def run(self) -> None:
        """Run the MovieApp, displaying the menu and handling user input."""
        while True:
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
                11. {MovieApp.GREEN}Generate Website{MovieApp.RESET}
            """)

            try:
                user_input = input(f"{MovieApp.CYAN}Enter choice (0-11):  {MovieApp.RESET}")
                if user_input.lower() == 'exit()' or user_input == '0':
                    exit()

                if user_input.isdigit():
                    user_command = int(user_input)
                    if 0 <= user_command <= 11:
                        match user_command:
                            case 1:
                                self._command_list_movies()
                            case 2:
                                title = input('Enter movie name: ')
                                self._storage.add_movie(title)
                            case 3:
                                title = input('Enter movie name: ')
                                self._storage.delete_movie(title)
                            case 4:
                                title = input('Enter movie name: ')
                                rating = int(input('Enter new rating: '))
                                self._storage.update_movie(title, rating)
                            case 5:
                                self._command_movie_stats()
                            case 6:
                                r = random.randint(0, len(self._movies['Movies']) - 1)
                                idx = [title for title in self._movies['Movies'].keys()]
                                random_movie = idx[r]
                                print(f"{MovieApp.YELLOW}Your Movie for the night is {random_movie} with a rating of {self._movies['Movies'][random_movie]['rating']}{MovieApp.RESET}")
                            case 7:
                                query = input('Enter a search term: ')
                                movies = self._storage.search_movie(query)
                                if not movies:
                                    print('We found nothing to match your query')
                                else:
                                    self._print_movies(movies)
                            case 8:
                                SF.sort_rating(self._storage)
                            case 9:
                                SF.sort_year(self._storage)
                            case 10:
                                SF.movie_filter(self._storage)
                            case 11:
                                self._generate_website()


                        input('Press Enter to Continue')
                    else:
                        print(f'{MovieApp.RED}!!!Please enter a valid choice!!!{MovieApp.RESET}\n')
                else:
                    print(f'{MovieApp.RED}!!!Please enter a valid choice!!!{MovieApp.RESET}\n')
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")




