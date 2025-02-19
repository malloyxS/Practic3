from cinema import Cinema

def main():
    cinema = Cinema()

    while True:
        print("\n--- Авторизация / Регистрация ---")
        action = input("Выберите 'войти' или 'зарегистрироваться': ").strip().lower()
        if action == 'зарегистрироваться':
            cinema.register_user()
        elif action == 'войти':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            if cinema.authenticate(username, password):
                print(f"Добро пожаловать{' (администратор)' if cinema.current_user.is_admin else ''}: {username}")
                while True:
                    cinema.show_film_menu()
                    choice = input("Выберите действие: ")
                    if choice == '0':
                        break
                    cinema.execute_action(choice)
            else:
                print("Неверное имя пользователя или пароль.")
        else:
            print("Некорректный выбор, пожалуйста, выберите 'войти' или 'зарегистрироваться.'")


if __name__ == "__main__":
    main()
