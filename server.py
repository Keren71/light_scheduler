import asyncio
import websockets
import json
import paho.mqtt.publish as mqtt_publish
from datetime import datetime

MQTT_HOST = '157.173.101.159'
MQTT_PORT = 1883
MQTT_CHANNEL = 'light/control'  # Adjust the topic as needed

timing_data = {'start_time': None, 'stop_time': None}

async def ws_handler(socket, _):
    try:
        async for raw_data in socket:
            parsed_data = json.loads(raw_data)
            start_time = parsed_data['onTime']
            stop_time = parsed_data['offTime']

            timing_data['start_time'] = start_time
            timing_data['stop_time'] = stop_time

            await socket.send(f"Scheduled: ON at {start_time}, OFF at {stop_time}")
            print(f"Received schedule: ON at {start_time}, OFF at {stop_time}")
    except Exception as err:
        await socket.send(f"Error: {str(err)}")
        print(f"WebSocket error: {err}")

async def timing_loop():
    while True:
        current_time = datetime.now().strftime('%H:%M')
        if timing_data['start_time'] == current_time:
            print(f"Triggering ON at {current_time}")
            mqtt_publish.single(MQTT_CHANNEL, payload='1', hostname=MQTT_HOST, port=MQTT_PORT)
        if timing_data['stop_time'] == current_time:
            print(f"Triggering OFF at {current_time}")
            mqtt_publish.single(MQTT_CHANNEL, payload='0', hostname=MQTT_HOST, port=MQTT_PORT)
        await asyncio.sleep(30)

async def main():
    server = await websockets.serve(ws_handler, "localhost", 8765)
    print("WebSocket server running on ws://localhost:8765")
    asyncio.create_task(timing_loop())
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped")
