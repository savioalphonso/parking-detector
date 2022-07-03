# Parking Enforcement Detector

## Installation on a Raspberry Pi

### Assuming Ubuntu 22.04 & Python 3

1. `sudo apt install python3-dev`
2. `sudo apt install libbluetooth-dev`
3. `sudo apt install gcc`
4. `sudo apt install python3.10-venv`
4. `git clone https://github.com/savioalphonso/parking-detector.git`
5. `cd parking-detector`
6. `python3 -m venv venv`
7. `source venv/bin/activate`
8. `cd ..`
9. `git clone https://github.com/pybluez/pybluez.git`
10. `cd pybluez`
11. `python3 setup.py install`
12. `cd ..`
13. `cd parking-detector`
14. `python3 BLE_inspector.py`
