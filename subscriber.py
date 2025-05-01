import paho.mqtt.client as mqtt
import serial
import time

USB_PORT = 'COM3'  # Adjust as needed
USB_BAUD = 9600
arduino_serial = serial.Serial(USB_PORT, USB_BAUD, timeout=1)

BROKER_ADDRESS = '157.173.101.159'
BROKER_PORT = 1883
TOPIC = 'light/control'  # Adjust the topic as needed
LOG_FILE = 'relay.txt'

def mqtt_connected(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed with code {rc}")

def mqtt_received(client, userdata, msg):
    command = msg.payload.decode().strip()
    print(f"Received MQTT command: {command} at {time.strftime('%H:%M')}")
    with open(LOG_FILE, 'w') as f:
        f.write(command)
    if command == '1':
        arduino_serial.write(b"ON\n")
        time.sleep(0.1)
        print(f"Sent to Arduino: ON at {time.strftime('%H:%M')}")
    elif command == '0':
        arduino_serial.write(b"OFF\n")
        print(f"Sent to Arduino: OFF at {time.strftime('%H:%M')}")
    else:
        print(f"Unknown command: {command}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = mqtt_connected
client.on_message = mqtt_received

client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Shutting down...")
    client.loop_stop()
    client.disconnect()
    arduino_serial.close()
