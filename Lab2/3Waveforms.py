import board
import busio
import adafruit_mcp4725
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

from time import sleep
from math import sin

pins = {"SCL":3,"SDA":2}
btn = 4

"""

VDD is VCC Power Supply -> [2.7,5.5]V
GND is Circuit Common Ground
SDA will send data from Raspberry Pi to the
chip (0-4095)
SCL (clock) will control the output rate
A0 is A0 address bit
Vout is analog output -> To oscilloscope [0,3.3]V

"""

def setup():
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

def btnPress():
    waveform = int(input("Enter Waveform : 1 for Square, 2 for Triangle, and 3 for Sin"))
    frequency = int(input("Enter Frequency : 1 for 10Hz, 2 for 25Hz, and 3 for 50Hz"))
    voltageMax = int(input("Input maximum voltage"))
    voltageMin = int(input("Input minimum voltage"))

def waveformSquare(dac):
    return

def waveformTriangle(dac):
    # Note : This may be too wide, will have to increase step range on oscilloscope test phase
    for i in range(4095):
        dac.raw_value = i

    for i in range(4095, -1, -1):
        dac.raw_value = i

def waveformSin(dac):
    t = 0.0
    tStep = 0.05
    while True:
        voltage = 2048*(1.0+0.5*sin(6.2832*t))
        dac.set_voltage(int(voltage))
        t += tStep
        time.sleep(0.0005)




    
def main():
    setup()
    i2c = busio.I2C(board.SCL, board.SDA) # Initialize I2C bus.
    dac = adafruit_mcp4725.MCP4725(i2c) # Initialize MCP4725.
    # dac.value[0,65525], dac.raw_value[0,4095], dac.normalized_value[0,1.0](Floating Point)
    # "If you need the most precise output use the raw_output value for setting voltage." - Adafruit
    dac.raw_value = 0
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=btnPress)


if __name__ == "__main__":
    main()

# Main loop will go up and down through the range of DAC values forever.
while True:
    # Go up the 12-bit raw range.
    print("Going up 0-3.3V...")
    for i in range(4095):
        dac.raw_value = i
    # Go back down the 12-bit raw range.
    print("Going down 3.3-0V...")
    for i in range(4095, -1, -1):
        dac.raw_value = i
