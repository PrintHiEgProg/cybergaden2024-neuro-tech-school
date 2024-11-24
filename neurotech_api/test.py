from collections import deque
import asyncio
import queue
import time
from typing import List
from enum import Enum
from dataclasses import dataclass
from statistics import stdev, mean
import requests

from neurosdk.callibri_sensor import CallibriSensor
from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.cmn_types import *
from callibri_ecg.callibri_ecg_lib import CallibriMath


hr_past = 0


class ConnectionState(Enum):
    Connection = 0
    Connected = 1
    Disconnection = 2
    Disconnected = 3
    Error = 4


@dataclass
class CallibriInfo:
    Name: str
    Address: str
    sensor_info: SensorInfo


class CallibriAdditional:
    def __init__(self, need_reconnect: bool, sensor: CallibriSensor):
        self.need_reconnect: bool = need_reconnect
        self.is_signal = False
        self.callibri: CallibriSensor = sensor
        self.ecg_math: CallibriMath = CallibriMath(1000, int(500), 30)
        self.ecg_math.init_filter()
        self.buf_size = int(1000 / 10)
        self.signal_data = queue.Queue()
        self.hr_values = []
        self.stress_values = []
        self.calibration_data = []
        self.calibration_stress = None
        self.stress_buffer = deque(maxlen=10)  # For smoothing stress level


class CallibriController:
    def __init__(self):
        super().__init__()
        self.__scanner = Scanner([SensorFamily.LECallibri, SensorFamily.LEKolibri])
        self.__connected_devices = {}
        self.connected_devices = list()

    async def search_with_result(self, seconds: int, addresses: List[str]):
        def __device_scan():
            print("Начало сканирования устройств...")
            self.__scanner.start()
            time.sleep(seconds)
            self.__scanner.stop()
            print("Сканирование завершено.")
            founded = self.__scanner.sensors()
            filtered_sensors = []
            for si in founded:
                if len(addresses) < 1 or si.Address in addresses:
                    filtered_sensors.append(CallibriInfo(Name=si.Name,
                                                         Address=si.Address,
                                                         sensor_info=si))
            return filtered_sensors

        return await asyncio.to_thread(__device_scan)

    async def connect_to(self, info: CallibriInfo, need_reconnect: bool = False):
        def __device_connection():
            try:
                print(f"Подключение к устройству {info.Name} ({info.Address})")
                sensor = self.__scanner.create_sensor(info.sensor_info)
                sensor.signal_type = CallibriSignalType.ECG
                sensor.sampling_frequency = SensorSamplingFrequency.FrequencyHz1000
                sensor.hardware_filters = [SensorFilter.HPFBwhLvl1CutoffFreq1Hz,
                                           SensorFilter.BSFBwhLvl2CutoffFreq45_55Hz,
                                           SensorFilter.BSFBwhLvl2CutoffFreq55_65Hz]
                self.__connected_devices.update({info.Address: CallibriAdditional(need_reconnect, sensor)})
                self.connected_devices.append(info.Address)
                print(f"Устройство {info.Name} подключено успешно.")
            except Exception as err:
                print(f"Ошибка при подключении к устройству {info.Name}: {err}")

        await asyncio.to_thread(__device_connection)

    async def calibrate_device(self, address: str):
        print(f"Калибровка устройства {address}...")
        device = self.__connected_devices[address]
        sensor = device.callibri

        def collect_calibration_data(sensor: Sensor, data: List[CallibriSignalData]):
            try:
                for sample in data:
                    device.calibration_data.extend(sample.Samples)
                    if len(device.calibration_data) >= device.buf_size * 5:  # More data for stability
                        sensor.signalDataReceived = None
                        print(f"Калибровка устройства {address} завершена.")
                        break
            except Exception as err:
                print(f"Ошибка при сборе данных для калибровки: {err}")

        sensor.signalDataReceived = collect_calibration_data
        await self.__execute_command(sensor, SensorCommand.StartSignal)

        while len(device.calibration_data) < device.buf_size * 5:
            await asyncio.sleep(0.1)

        await self.__execute_command(sensor, SensorCommand.StopSignal)

        # Calibration data analysis
        if device.calibration_data:
            mean_value = mean(device.calibration_data)
            stdev_value = stdev(device.calibration_data)
            print(f"Среднее значение сигнала: {mean_value:.2f}")
            print(f"СКО сигнала: {stdev_value:.2f}")
            if stdev_value < 10:  # Calibration success condition
                print(f"Устройство {address} откалибровано успешно.")
                rr_intervals = [device.calibration_data[i + 1] - device.calibration_data[i]
                                for i in range(len(device.calibration_data) - 1)]
                rr_intervals = [v for v in rr_intervals if v > 300 and v < 2000]  # Outlier filtering
                device.calibration_stress = self.calculate_stress_index(rr_intervals)
                print(f"Базовый уровень стресса для устройства {address}: {device.calibration_stress:.2f}")
            else:
                print(f"Калибровка устройства {address} не удалась. Проверьте подключение.")
        else:
            print(f"Недостаточно данных для калибровки устройства {address}.")

    async def start_calculations(self):
        async def handle_device(address: str):
            def on_signal_received(sensor: Sensor, data: List[CallibriSignalData]):
                try:
                    global hr_past
                    device = self.__connected_devices[address]
                    math = device.ecg_math
                    buf_size = device.buf_size
                    buffer = device.signal_data
                    calibration_stress = device.calibration_stress

                    for sample in data:
                        for value in sample.Samples:
                            buffer.put(value)
                    if buffer.qsize() > buf_size:
                        raw_data = [buffer.get() for _ in range(buf_size)]
                        math.push_data(raw_data)
                        math.process_data_arr()
                        rr_detected = math.rr_detected()

                        if rr_detected:
                            hr = math.get_hr()
                            stress_index = self.calculate_stress_index(raw_data)
                            adjusted_stress = stress_index - (calibration_stress or 0)
                            device.stress_buffer.append(adjusted_stress)

                            # Smoothing
                            smoothed_stress = mean(device.stress_buffer)
                            stress_level = self.get_stress_level(smoothed_stress)

                            device.hr_values.append(hr)
                            device.stress_values.append(smoothed_stress)

                            # Device and stress level highlighting
                            device_color = self.get_device_color(sensor.name)
                            stress_color = self.get_stress_color(smoothed_stress)

                            print(f"{device_color}[Устройство: {sensor.name} ({sensor.address})]{device_color}")
                            print(f"  ЧСС: {hr:.2f} уд./мин")
                            print(
                                f"  Индекс стресса (сглаженный): {stress_color}{smoothed_stress:.2f} ({stress_level}){stress_color}")
                            print("\033[0m")  # Reset color
                            if hr != hr_past:
                                self.send_to_server(self, sensor.name, sensor.address, hr,
                                                    smoothed_stress, stress_level)
                                hr_past = hr

                except Exception as err:
                    print(f"Ошибка при обработке сигнала для {sensor.address}: {err}")

            sensor = self.__connected_devices[address].callibri
            sensor.signalDataReceived = on_signal_received
            await self.__execute_command(sensor, SensorCommand.StartSignal)
            self.__connected_devices[address].is_signal = True

        await asyncio.gather(*[handle_device(address) for address in self.connected_devices])

    @staticmethod
    def calculate_stress_index(rr_intervals: List[int]) -> float:
        if len(rr_intervals) < 2:
            return 0
        # Use heart rate variability (HRV) measure for a more reliable stress index
        mean_rr = mean(rr_intervals)
        rr_stdev = stdev(rr_intervals)
        stress_index = mean_rr / rr_stdev if rr_stdev > 0 else 0
        return stress_index

    @staticmethod
    def get_stress_level(stress_index: float) -> str:
        if stress_index < 1.5:
            return "Низкий"
        elif stress_index < 3.0:
            return "Средний"
        else:
            return "Высокий"

    @staticmethod
    def get_device_color(sensor_name: str) -> str:
        color_map = {
            "Callibri": "\033[94m",  # Blue for Callibri
            "Kolibri": "\033[92m",  # Green for Kolibri
        }
        return color_map.get(sensor_name, "\033[0m")  # Default color reset

    @staticmethod
    def get_stress_color(stress_value: float) -> str:
        if stress_value < 1.5:
            return "\033[92m"  # Green for low stress
        elif stress_value < 3.0:
            return "\033[93m"  # Yellow for moderate stress
        else:
            return "\033[91m"  # Red for high stress

    async def __execute_command(self, sensor: Sensor, command: SensorCommand):
        def execute_command():
            try:
                sensor.exec_command(command)
            except Exception as err:
                print(f"Ошибка выполнения команды: {err}")

        await asyncio.to_thread(execute_command)

    def stop_all(self):
        self.__scanner.stop()
        for device in self.__connected_devices.values():
            device.callibri.disconnect()
            device.callibri = None
        self.__connected_devices.clear()
        self.connected_devices.clear()

    @staticmethod
    def send_to_server(self, name: str, address: str, hr, stress_num, stress_level: str):
        try:
            url = f"https://4ade-188-162-144-139.ngrok-free.app/api/calibri/{name}/"
            url_i = f"https://4ade-188-162-144-139.ngrok-free.app/api/calibri/"
            headers = {"Content-Type": "application/json"}

            # Проверяем, существует ли устройство на сервере
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Если устройство существует, обновляем данные через PUT
                update_data = {
                    "name": name,
                    "RR": hr,
                    "stress_num": stress_num,
                    "stress_level": stress_level,
                }
                update_response = requests.put(url, json=update_data, headers=headers, timeout=10)
                if update_response.status_code == 200:
                    print(
                        f"Updated {name} ({address}): HR={hr}, stress_num={stress_num:.2f}, stress_level={stress_level}")
                else:
                    print(f"Failed to update {name}: {update_response.status_code} {update_response.text}")
            elif response.status_code == 404:
                # Если устройства нет, создаём новую запись через POST
                create_data = {
                    "name": name,
                    "RR": hr,
                    "stress_num": stress_num,
                    "stress_level": stress_level,
                }
                create_response = requests.post(url_i, json=create_data, headers=headers, timeout=10)
                if create_response.status_code == 201:
                    print(
                        f"Inserted new record for {name} ({address}): HR={hr}, stress_num={stress_num:.2f}, stress_level={stress_level}")
                else:
                    print(f"Failed to create record for {name}: {create_response.status_code} {create_response.text}")
            else:
                print(f"Failed to fetch {name}: {response.status_code} {response.text}")
        except requests.RequestException as e:
            print(f"Error during API request for {name}: {e}")


async def main():
    controller = CallibriController()
    print("Поиск устройств...")
    devices = await controller.search_with_result(5, [])

    if not devices:
        print("Устройства не найдены.")
        return

    print(f"Найдено устройств: {len(devices)}")
    for device in devices:
        print(f"- {device.Name} ({device.Address})")

    await asyncio.gather(*[controller.connect_to(device) for device in devices])

    print("Калибровка устройств...")
    await asyncio.gather(*[controller.calibrate_device(device.Address) for device in devices])

    print("Начало сбора данных. Нажмите Ctrl+C для завершения.")
    try:
        await controller.start_calculations()
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Завершение программы...")
    finally:
        controller.stop_all()


if __name__ == '__main__':
    asyncio.run(main())
