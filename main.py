import ubluetooth
from machine import I2C, Pin
import time
from ADXL345 import ADXL345_I2C
import network

# Abrufen der MAC-Adresse des ESP32
mac = network.WLAN(network.STA_IF).config('mac')
print("MAC-Adresse des ESP32:", ':'.join(['{:02x}'.format(b) for b in mac]))

# Initialisierung des I2C-Busses (GPIO 21 für SDA, GPIO 22 für SCL)
i2c = I2C(scl=Pin(22), sda=Pin(21))

# Initialisierung des ADXL345
sensor = ADXL345_I2C(i2c)

# Schwellenwert für den Sprung
JUMP_THRESHOLD = 300  # Empfindlichkeit, kann je nach Bedarf angepasst werden

# BLE Setup
ble = ubluetooth.BLE()
ble.active(True)

# Accelerometer Service UUID (0x1818)
SERVICE_UUID = ubluetooth.UUID(0x1818)  # Accelerometer Service UUID
CHARACTERISTIC_UUID = ubluetooth.UUID(0x2A58)  # Accelerometer Data Characteristic UUID
CHARACTERISTIC_UUID_HEX = 0x2A58

# GATT-Services und Charakteristiken erstellen
ble.gatts_register_services([(SERVICE_UUID, [(CHARACTERISTIC_UUID, ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY)])])

# Werbung starten
def start_advertise():
    advertising_payload = b'\x02\x01\x06\x03\x03' + SERVICE_UUID
    ble.gap_advertise(100, advertising_payload)

# Funktion zur Erkennung eines Sprungs
def detect_jump():
    while True:
        # Holen der Beschleunigungswerte
        x = sensor.xValue
        y = sensor.yValue
        z = sensor.zValue

        # Überprüfen, ob die Z-Achse eine starke Beschleunigung erfährt, die einen Sprung anzeigt
        if abs(z) > JUMP_THRESHOLD:
            # Sende "Sprung" via BLE (CHARACTERISTIC_UUID muss als bytearray übergeben werden)
            ble.gatts_notify(0, CHARACTERISTIC_UUID_HEX, bytearray(b"0000"))
            print("Sprung gesendet")
            time.sleep(0.5)  # kleine Pause, um mehrfaches Erkennen desselben Sprungs zu verhindern

        time.sleep(0.1)  # Zeitverzögerung zwischen den Abfragen, um den Prozessor zu entlasten

# BLE-Werbung starten
start_advertise()

# Sprung-Erkennung starten
detect_jump()