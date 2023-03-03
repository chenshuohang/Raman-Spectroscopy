import serial
from serial.tools import list_ports
import numpy as np, matplotlib.pyplot as plt
class CCD:
    def __init__(self) -> bool:
        self.ser = serial.Serial("COM3", 9600, timeout = 1)


if __name__ == "__main__":
    list_ports.main()
