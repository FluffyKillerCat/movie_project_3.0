class SF:
    def __init__(self, data):
        self._data = data

    def movie_filter(self):
        """
        Filters movies based on rating and/or year.
        Prompts the user to input minimum rating, minimum year, and maximum year to filter the movies.
        Prints the filtered movies along with their ratings and years.
        """

        if len(self._data['Movies']) != 0:
            while True:
                rating = input('Enter minimum rating or leave blank: ')
                min_year = input("Enter minimum year or leave blank: ")
                if isinstance(min_year, str):
                    max_year = input("Enter max year or leave blank: ")
                if rating == "" and min_year == "":
                    print('Please enter either a year or a rating filter to continue...')
                else:
                    try:
                        rating = float(rating) if rating else None
                        min_year = int(min_year) if min_year != "" else None
                        if min_year:
                            max_year = int(max_year) if max_year != "" else None
                        else:
                            max_year = None
                        break
                    except ValueError:
                        print("Invalid Input!!")

            filtered_movies = [
                (title, details) for title, details in self._data['Movies'].items()
                if (rating is None or float(details['rating']) >= rating) and
                   (min_year is None or float(details['year']) >= min_year) and
                   (max_year is None or float(details['year']) <= max_year)
            ]

            for movie_name, details in filtered_movies:
                print(f"{movie_name} ({details['year']}): {details['rating']}")
        else:
            print('Empty DB')


    def sort_year(self):
        # Sorts movies based on years


        if len(self._data['Movies']) != 0:
            while True:
                reverse_order = input('Do you want the latest movies first? (Y/N): ')
                if reverse_order.lower() == "y":
                    reverse_order = True
                    break

                elif reverse_order.lower() == "n":

                    reverse_order = False
                    break
                else:
                    print('Invalid Input!!')

            sorted_movies = sorted(self._data['Movies'].items(), key=lambda x: float(x[1]['year']), reverse=reverse_order)
            for movie in sorted_movies:
                print(f"{movie[0]} ({movie[1]['year']}): {movie[1]['rating']}")
        else:
            raise ValueError('Empty DB')

    def sort_rating(self):
        # Sorts movies based on ratings

        if len(self._data['Movies']) != 0:

            while True:
                reverse_order = input('Do you want the best movies first? (Y/N): ')
                if reverse_order.lower() == "y":
                    reverse_order = True
                    break

                elif reverse_order.lower() == "n":

                    reverse_order = False
                    break
                else:
                    print('Invalid Input!!')

            sorted_movies = sorted(self._data['Movies'].items(), key=lambda x: float(x[1]['rating']), reverse=reverse_order)
            for movie in sorted_movies:
                print(f"{movie[0]} ({movie[1]['year']}): {movie[1]['rating']}")
        else:
            raise ValueError('Empty DB')



