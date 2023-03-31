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

## Usage

`git clone https://github.com/melli0505/monitoring_system.git`
`pip install uvicorn paho-mqtt FastAPI sqlalchemy`
`uvicorn main:app --reload`
