class Film:
    def __init__(self, title, genre, year, rating):
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating

    def __str__(self):
        return f"{self.title} | Жанр: {self.genre} | Год: {self.year} | Рейтинг: {self.rating}"
