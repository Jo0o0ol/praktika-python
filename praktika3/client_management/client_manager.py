import json
from client import Client 

class ClientManager:
    def __init__(self):
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)
        print(f"Клиент '{client.name}' добавлен.")

    def delete_client(self, account_number):
        self.clients = [client for client in self.clients if client.account_number != account_number]
        print(f"Клиент с номером счета '{account_number}' удален.")

    def search_client(self, account_number):
        found_clients = [client for client in self.clients if client.account_number == account_number]
        return found_clients

    def sort_clients(self):
        self.clients.sort(key=lambda client: client.name)
        print("Клиенты отсортированы по имени.")

    def filter_clients(self, keyword):
        return [client for client in self.clients if keyword.lower() in client.name.lower()]

    def show_clients(self):
        if self.clients:
            print("Список клиентов:")
            for client in self.clients:
                print(f"- Имя: {client.name}, Номер счета: {client.account_number}")
        else:
            print("Список клиентов пуст.")

    def update_client(self, account_number, new_name):
        for client in self.clients:
            if client.account_number == account_number:
                client.name = new_name
                print(f"Данные клиента с номером счета '{account_number}' обновлены.")
                return
        print(f"Клиент с номером счета '{account_number}' не найден.")

    def import_clients(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            clients_data = json.load(file)
            for data in clients_data:
                self.add_client(Client(data['name'], data['account_number']))

    def export_clients(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([{'name': client.name, 'account_number': client.account_number} for client in self.clients], file)
            print("Клиенты экспортированы.")
