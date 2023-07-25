# Monitoring System

The monitoring system is expected to include real-time graphs, Control modules, and data visualization after processing.

## System Flow

The AC Energy data is communicated via MQTT between Arduino ESP32 and local server, and stored in the PostgreSQL database.
The data stored in the database is processed using FastAPI.

## System Configuration:

- Data Source: ESP32 DevkitC-V4 arduino board with PZEM-004t AC Energy monitor
- Back-end: FastAPI
- Database: PostgreSQL
- Sensor communication protocol: MQTT
  - Broker: Mosquitto
  - Client: paho.mqtt

### More Detail about this project

https://dnai-deny.tistory.com/category/Project/Monitoring%20System

## Usage

```
git clone https://github.com/melli0505/monitoring_system.git
```

```
pip install uvicorn paho-mqtt FastAPI sqlalchemy
```

```
cd Monitoring
```

```
uvicorn main:app --reload
```

### Wireless vibration data plotter

- `WLAN_daq/qt_server.py` is plotter for vibration data, implemented by pyqtgraph. It shows real-time original signal graph & fft result. This process communicate with mcc172 DAQ hats by high-speed wireless communication.
- If you want to use this, you need to modify sampling rate and IP Address.

### Starting MQTT

- This example is using PZEM-004t AC Energy monitor with ESP32 DevkitC-V4 arduino as a data source. You can check the source code for ESP32 in my another Repository `PTC_Control`.
- You can start MQTT Communication with ESP32(PZEM-004t) by running `Monitoring/core/mqtt/pzem_sub.py`.
- `Monitoring/core/mqtt/pzem_pub.py` is for control PZEM-004t, to reset energy state. It works with button

## Structure

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
  x └ ( -- not use ) sensor
      x └ sensor_crud.py
      x └ sensor_router.py
    └ data
        └ data_crud.py
        └ data_router.py
        └ data_schema.py
    └ utils
        └ utils.py
    └ mqtt
      └ pzem_pub.py
      └ pzem_sub.py
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
- WLAN_daq
  └ qt_server.py
  └ qt_stft.py
  └ matplotlib_server.py
  └ matplotlib_stft.py
└ .gitignore
└ README.md
```
