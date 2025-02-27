import json
from user import User
from film import Film

class DataHandler:
    def __init__(self, filename='cinema_data.json'):
        self.filename = filename

    def save_data(self, users, films):
        data = {
            "users": [{"username": user.username, "password": user.password, "is_admin": user.is_admin}
                      for user in users],
            "films": [{"title": film.title, "genre": film.genre, "year": film.year, "rating": film.rating}
                      for film in films]
        }
        with open(self.filename, 'w', encoding='utf-8') as f:

            json.dump(data, f, ensure_ascii= False)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                if len(f.readlines()) > 0:
                    data = json.load(f)
                    users = [User(d['username'], d['password'], d['is_admin']) for d in data['users']]
                    films = [Film(d['title'], d['genre'], d['year'], d['rating']) for d in data['films']]
                    return users, films
                return [], []
        except FileNotFoundError:
            print("Файл данных не найден, создается новый.")
            return [], []
