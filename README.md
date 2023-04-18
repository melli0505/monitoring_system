# Monitoring System

The monitoring system is expected to include real-time graphs, sensor-specific information, and data visualization after processing.

## System Flow

The temperature sensor data is communicated via MQTT and stored in the PostgreSQL database.
The data stored in the database is processed using FastAPI.
The frontend will be implemented later. An authentication system is being developed.

## System Configuration:

- Back-end: FastAPI
- Database: PostgreSQL
- Sensor communication protocol: MQTT
  - Broker: Mosquitto
  - Client: paho.mqtt

### More Detail about this project

https://dnai-deny.tistory.com/category/Project

## Usage

```
git clone https://github.com/melli0505/monitoring_system.git
```

```
pip install uvicorn paho-mqtt FastAPI sqlalchemy
```

```
uvicorn main:app --reload
```

## Structure

- `udp_server.py` is temporary data receiver, it shows real-time original signal graph & fft result. This process communicate with mcc172 DAQ hats by UDP socket.
- If you want to use this, you need to modify sampling rate and IP Address.

```
- Monitoring
  └ core
    └ db
        └ base.py
        └ models.py
        └ schemas.py
    └ user
        └ user_crud.py
        └ user_router.py
        └ user_schema.py
    └ sensor
        └ sensor_crud.py
        └ sensor_router.py
    └ data
        └ data_crud.py
        └ data_router.py
        └ data_schema.py
    └ utils
        └ utils.py
    └ subscriber.py
  └ static
    └ js
    └ css
    └ scss
    └ images
    └ fonts
  └ templates
    └ chart.html
    └ index.html
    └ signup.html
  └ main.py
└ publisher.py
└ .gitignore
└ README.md
└ udp_server.py
```
