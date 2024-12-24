import asyncio
from bleak import BleakClient

# Die Adresse des ESP32-BLE-Servers (ersetzte mit der richtigen MAC-Adresse des ESP32)
ESP32_ADDRESS = "XX:XX:XX:XX:XX:XX"

# Die UUID des BLE-Services und der Charakteristik
SERVICE_UUID = "12345678-9abc-def0-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-9abc-def0-1234-56789abcdef0"

async def run():
    async with BleakClient(ESP32_ADDRESS) as client:
        print(f"Verbindung zu {ESP32_ADDRESS} hergestellt")

        # Warten auf Benachrichtigungen (sprung)
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        # Solange laufen lassen, um Benachrichtigungen zu empfangen
        while True:
            await asyncio.sleep(1)

def notification_handler(sender: int, data: bytearray):
    print(f"Empfangen: {data.decode('utf-8')}")

# Starte das BLE-Client-Programm
asyncio.run(run())
