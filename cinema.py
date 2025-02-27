from data_handler import DataHandler
from user import User, Admin
from film import Film

class Cinema:
    def __init__(self):
        self.data_handler = DataHandler()
        self.users, self.films = self.data_handler.load_data()
        self.current_user = None

    def add_user(self, username, password):
        new_user = User(username, password)
        self.users.append(new_user)
        self.data_handler.save_data(self.users, self.films)

    def add_admin(self, username, password):
        new_admin = Admin(username, password)
        self.users.append(new_admin)
        self.data_handler.save_data(self.users, self.films)

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                return True
        return False

    def register_user(self):
        user_type = input("Хотите зарегистрироваться как 'пользователь' или 'администратор'? ").strip().lower()
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")

        if user_type == 'пользователь':
            self.add_user(username, password)
            print(f"Пользователь '{username}' успешно зарегистрирован.")
        elif user_type == 'администратор':
            self.add_admin(username, password)
            print(f"Администратор '{username}' успешно зарегистрирован.")
        else:
            print("Некорректный ввод. Пожалуйста, выберите 'пользователь' или 'администратор'.")

    def add_film(self, title, genre, year, rating):
        new_film = Film(title, genre, year, rating)
        self.films.append(new_film)
        self.data_handler.save_data(self.users, self.films)

    def remove_film(self, title):
        self.films = [film for film in self.films if film.title != title]
        self.data_handler.save_data(self.users, self.films)

    def view_films(self):
        return self.films

    def sort_films(self, key):
        return sorted(self.films, key=lambda film: getattr(film, key))

    def filter_films(self, **criteria):
        filtered_films = self.films
        for key, value in criteria.items():
            if value:
                if key == 'жанр':
                    filtered_films = [film for film in filtered_films if film.genre.lower() == value.lower()]
                elif key == 'Год выпуска':
                    filtered_films = [film for film in filtered_films if film.year == value]
                elif key == 'Рейтинг':
                    filtered_films = [film for film in filtered_films if film.rating >= value]
        return filtered_films

    def show_film_menu(self):
        print("\n--- Меню фильмов ---")
        print("1. Просмотреть все фильмы")
        print("2. Сортировать фильмы")
        print("3. Фильтровать фильмы")
        if self.current_user.is_admin:
            print("4. Добавить фильм")
            print("5. Удалить фильм")
        print("0. Выйти")

    def execute_action(self, choice):
        actions = {
            '1': self.display_films,
            '2': self.sort_films_interface,
            '3': self.filter_films_interface,
        }

        if self.current_user.is_admin:
            actions['4'] = self.add_film_interface
            actions['5'] = self.remove_film_interface

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Некорректный выбор, пожалуйста, попробуйте снова.")

    def add_film_interface(self):
        title = input("Введите название фильма: ")
        genre = input("Введите жанр фильма: ")
        year = self.get_valid_year_input("Введите год выпуска фильма: ")
        rating = self.get_valid_rating_input("Введите рейтинг фильма: ")
        self.add_film(title, genre, year, rating)
        print(f"Фильм '{title}' добавлен.")

    def remove_film_interface(self):
        title = input("Введите название фильма для удаления: ")
        self.remove_film(title)
        print(f"Фильм '{title}' удален.")

    def display_films(self):
        films = self.view_films()
        if films:
            print("\nСписок фильмов:")
            for film in films:
                print(film)
        else:
            print("Нет доступных фильмов.")

    def sort_films_interface(self):
        key = input("Введите критерий сортировки (title, year, rating): ")
        sorted_films = self.sort_films(key)
        self.display_films_from_list(sorted_films)

    def filter_films_interface(self):
        genre = input("Введите жанр для фильтрации (или оставьте пустым): ")
        year = self.get_valid_year_input("Введите год (или оставьте пустым): ", allow_empty=True)
        rating = self.get_valid_rating_input("Введите минимальный рейтинг (или оставьте пустым): ", allow_empty=True)

        criteria = {}
        if genre:
            criteria['жанр'] = genre
        if year:
            criteria['Год выпуска'] = year
        if rating:
            criteria['Рейтинг'] = rating

        filtered_films = self.filter_films(**criteria)
        self.display_films_from_list(filtered_films)

    def display_films_from_list(self, films):
        if films:
            print("\nФильмы по заданным критериям:")
            for film in films:
                print(film)
        else:
            print("Нет доступных фильмов по заданным критериям.")

    def get_valid_year_input(self, prompt, allow_empty=False):
        while True:
            user_input = input(prompt)
            if allow_empty and user_input == '':
                return None
            if user_input.isdigit() and 1900 <= int(user_input) <= 2024:
                return int(user_input)
            print("Пожалуйста, введите корректный год от 1900 до 2024.")

    def get_valid_rating_input(self, prompt, allow_empty=False):
        while True:
            user_input = input(prompt)
            if allow_empty and user_input == '':
                return None
            try:
                rating = float(user_input)
                if 0 <= rating <= 10:
                    return rating
                print("Рейтинг должен быть в диапазоне от 0 до 10.")
            except ValueError:
                print("Пожалуйста, введите корректное значение рейтинга.")
