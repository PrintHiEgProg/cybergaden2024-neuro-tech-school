import asyncio
import requests
import random
from typing import List
from collections import deque
from statistics import mean, stdev

# Конфигурация API
API_URL = "https://4ade-188-162-144-139.ngrok-free.app/api/calibri/"

# Функция для обновления данных устройства
async def update_or_insert_rr(name: str):
    try:
        response = requests.get(f"{API_URL}{name}/", timeout=10)

        if response.status_code == 200:
            # Если устройство существует, обновляем данные
            new_rr = random.randint(50, 400)  # Генерация нового значения RR
            new_stress_num = random.randint(1, 10)  # Рандомное значение stress_num
            new_stress_level = random.choice(["low", "medium", "high"])  # Рандомное stress_level

            update_data = {
                "RR": new_rr,
                "stress_num": new_stress_num,
                "stress_level": new_stress_level,
            }
            update_response = requests.put(f"{API_URL}{name}/", json=update_data, timeout=10)

            if update_response.status_code == 200:
                print(f"Updated {name}: RR={new_rr}, stress_num={new_stress_num}, stress_level={new_stress_level}")
            else:
                print(f"Failed to update {name}: {update_response.status_code} {update_response.text}")
        elif response.status_code == 404:
            # Если устройство не существует, создаём запись
            new_rr = random.randint(50, 400)  # Генерация нового значения RR
            new_stress_num = random.randint(1, 10)
            new_stress_level = random.choice(["low", "medium", "high"])

            create_data = {
                "name": name,
                "RR": new_rr,
                "stress_num": new_stress_num,
                "stress_level": new_stress_level,
            }
            create_response = requests.post(API_URL, json=create_data, timeout=10)

            if create_response.status_code == 201:
                print(f"Inserted new record for {name}: RR={new_rr}, stress_num={new_stress_num}, stress_level={new_stress_level}")
            else:
                print(f"Failed to create record for {name}: {create_response.status_code} {create_response.text}")
        else:
            print(f"Failed to fetch {name}: {response.status_code} {response.text}")
    except requests.RequestException as e:
        print(f"Error during API request for {name}: {e}")


# Асинхронный контроллер для работы с устройствами
class CallibriControllerAPI:
    def __init__(self):
        self.devices = ["John Doe", "Jane Doe", "Alice"]

    async def process_devices(self):
        while True:
            # Асинхронно обрабатываем каждое устройство
            await asyncio.gather(*(update_or_insert_rr(name) for name in self.devices))
            await asyncio.sleep(2)  # Интервал между обновлениями

    async def start(self):
        try:
            print("Начало работы с устройствами через API...")
            await self.process_devices()
        except KeyboardInterrupt:
            print("Программа остановлена вручную.")
        finally:
            print("Остановка работы.")


# Запуск основного процесса
async def main():
    controller = CallibriControllerAPI()
    await controller.start()


if __name__ == "__main__":
    asyncio.run(main())
