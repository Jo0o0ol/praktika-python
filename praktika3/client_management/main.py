from user import User
from client import Client
from client_manager import ClientManager

def display_menu():
    print("\nМеню:")
    print("1. Добавить клиента")
    print("2. Удалить клиента")
    print("3. Поиск клиента")
    print("4. Сортировка клиентов")
    print("5. Фильтрация клиентов")
    print("6. Показать всех клиентов")
    print("7. Обновить данные клиента")
    print("8. Импорт клиентов")
    print("9. Экспорт клиентов")
    print("0. Выход")

def main():
    users = [
        User("admin", "password", True),
        User("user", "userpassword", False)
    ]

    client_manager = ClientManager()
    current_user = None

    while True:
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        current_user = next((user for user in users if user.login(username, password)), None)
        if current_user:
            break
        else:
            print("Неверный логин или пароль.")
    
    while True:
        display_menu()
        choice = input("Выберите действие: ")

        if choice == '1' and current_user.is_admin:
            name = input("Введите имя клиента: ")
            account_number = input("Введите номер счета клиента: ")
            client_manager.add_client(Client(name, account_number))

        elif choice == '2':
            account_number = input("Введите номер счета клиента для удаления: ")
            client_manager.delete_client(account_number)

        elif choice == '3':
            account_number = input("Введите номер счета клиента для поиска: ")
            found_clients = client_manager.search_client(account_number)
            if found_clients:
                print("Найденные клиенты:")
                for client in found_clients:
                    print(f"- Имя: {client.name}, Номер счета: {client.account_number}")
            else:
                print("Клиенты не найдены.")

        elif choice == '4':
            client_manager.sort_clients()

        elif choice == '5':
            keyword = input("Введите ключевое слово для фильтрации (по имени): ")
            filtered_clients = client_manager.filter_clients(keyword)
            if filtered_clients:
                print("Отфильтрованные клиенты:")
                for client in filtered_clients:
                    print(f"- Имя: {client.name}, Номер счета: {client.account_number}")
            else:
                print("Клиенты не найдены.")

        elif choice == '6':
            client_manager.show_clients()

        elif choice == '7':
            account_number = input("Введите номер счета клиента для обновления: ")
            new_name = input("Введите новое имя клиента: ")
            client_manager.update_client(account_number, new_name)

        elif choice == '8':
            file_path = input("Введите путь для импорта клиентов: ")
            client_manager.import_clients(file_path)

        elif choice == '9':
            file_path = input("Введите путь для экспорта клиентов: ")
            client_manager.export_clients(file_path)

        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Ошибка: Неверный ввод. Пожалуйста, выберите действие из меню.")

if __name__ == "__main__":
    main()
