# IoT Light Scheduler

A real-time, web-based IoT dashboard to schedule and control a light using WebSocket and MQTT, built for the Rwanda Coding Academy Embedded Systems Software Integration course.

## 🚀 Features
- 🌐 Web-based UI using HTML, CSS, JS
- 🔌 Real-time WebSocket communication
- 📡 MQTT integration using Mosquitto
- 🔧 Arduino UNO-based relay switching


## 📦 Project Structure
├── index.html         # Frontend UI  
├── styles.css         # Styling  
├── script.js          # WebSocket logic  
├── server.py          # WebSocket + MQTT logic  
├── subscriber.py      # MQTT to Serial to Arduino  
├── README.md



## 🛠️ Setup Instructions

1. Arduino Setup

Connect your relay module to the Arduino UNO:
- VCC → 5V  
- GND → GND  
- IN → Pin 8  

Then upload this code using the Arduino IDE:

int relayPin = 8;

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // OFF
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "ON") digitalWrite(relayPin, LOW);  // ON
    else if (cmd == "OFF") digitalWrite(relayPin, HIGH);  // OFF
  }
}

2. Backend Setup
Install required Python libraries:

pip install websockets paho-mqtt pyserial

Start the backend services:

python server.py
python subscriber.py

Make sure your Mosquitto broker is running (locally or on a remote server), and update the IP address if needed in the code.

3. Frontend UI
Open the index.html file in any modern browser.

Use the form to set ON and OFF times, then press "Schedule Light".
The system will automatically send MQTT messages at the scheduled times to control the light.

📩 Author
Your Name
📧 igiranezakkeren16@gmail.com