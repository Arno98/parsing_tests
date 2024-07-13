import requests
import pandas as pd
from tabulate import tabulate

class CountriesAPI:
    def __init__(self, url="https://restcountries.com/v3.1/all"):
        # Ініціалізація класу з URL API
        self.url = url

    def fetch_data(self):
        # Метод для отримання даних з API
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Перевірка статусу відповіді
            return response.json()  # Повернення даних у форматі JSON
        except requests.exceptions.RequestException as e:
            # Обробка помилок запиту
            print(f"An error occurred: {e}")
            return []

    def process_data(self, data):
        # Метод для обробки отриманих даних
        countries_list = [
            {
                "Country": country.get("name", {}).get("common", "N/A"),  # Назва країни
                "Capital": country.get("capital", ["N/A"])[0],  # Столиця
                "Flag URL": country.get("flags", {}).get("png", "N/A")  # URL прапора
            }
            for country in data
        ]
        return countries_list

    def display_data(self, countries_list):
        # Метод для відображення даних у табличному форматі
        df = pd.DataFrame(countries_list)  # Створення DataFrame з оброблених даних
        print(tabulate(df, headers='keys', tablefmt='simple', showindex=False))  # Виведення таблиці

    def run(self):
        # Основний метод для виконання всіх операцій
        data = self.fetch_data()  # Отримання даних з API
        if data:
            processed_data = self.process_data(data)  # Обробка даних
            self.display_data(processed_data)  # Відображення даних

if __name__ == "__main__":
    # Запуск програми
    api = CountriesAPI()
    api.run()
