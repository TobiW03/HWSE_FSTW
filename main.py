from machine import I2C, Pin
import time
from ADXL345 import ADXL345_I2C

# Initialisierung des I2C-Busses (GPIO 21 für SDA, GPIO 22 für SCL)
i2c = I2C(scl=Pin(22), sda=Pin(21))

# Initialisierung des ADXL345
sensor = ADXL345_I2C(i2c)

# Schwellenwert für den Sprung (z.B. eine bestimmte Beschleunigung, die als "Sprung" definiert wird)
JUMP_THRESHOLD = 300  # Empfindlichkeit, kann je nach Bedarf angepasst werden

# Funktion zur Erkennung eines Sprungs
def detect_jump():
    while True:
        # Holen der Beschleunigungswerte
        x = sensor.xValue
        y = sensor.yValue
        z = sensor.zValue

        # Berechnung von Roll- und Pitch-Winkeln (optional, um Bewegungen zu analysieren)
        roll, pitch = sensor.RP_calculate(x, y, z)
        
        # Überprüfen, ob die Z-Achse eine starke Beschleunigung erfährt, die einen Sprung anzeigt
        if abs(z) > JUMP_THRESHOLD:
            print("Sprung")
            time.sleep(0.5)  # kleine Pause, um mehrfaches Erkennen desselben Sprungs zu verhindern

        time.sleep(0.1)  # Zeitverzögerung zwischen den Abfragen, um den Prozessor zu entlasten

# Sprung-Erkennung starten
detect_jump()
