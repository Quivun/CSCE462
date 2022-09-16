from math import sin, pi
from time import sleep
from busio import I2C
import board
import adafruit_mcp4725
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# dac.value[0,65525], dac.raw_value[0,4095], dac.normalized_value[0,1.0](Floating Point)
# "If you need the most precise output use the raw_output value for setting voltage." - Adafruit

"""

VDD is VCC Power Supply -> [2.7,5.5]V
GND is Circuit Common Ground
SDA will send data from Raspberry Pi to the
chip (0-4095)
SCL (clock) will control the output rate
A0 is A0 address bit
Vout is analog output -> To oscilloscope [0,3.3]V

"""

btn = 4
i2c = I2C(board.SCL, board.SDA)  # Initialize I2C bus.

#Globals
dac = adafruit_mcp4725.MCP4725(i2c)  # Initialize MCP4725.
delta = False
waveform = "NULL"
frequency = 0
voltageMax = 0.01
absMax = 5

def setup():
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def changeCheck():
    return delta

def btnPress():
    global delta
    global waveform
    global frequency
    global voltageMax
    global absMax
    if (delta):
        delta = False
    sleep(.25)
    waveform = input("Enter Waveform : 1 for Square, 2 for Triangle, and 3 for Sin : ")
    frequency = int(input("Enter, in hertz, the frequency of the wave : "))
    voltageMax = float(input("Input maximum voltage [Less than or equal to 3.3V, will default to [0,3.3] if beyond either bounds : "))
    delta = True
    funcDict[waveform]()
    return

def waveformSquare():
    halfCycle = 1.0/(2.0*frequency)
    maxVal = int(4095.0*voltageMax/absMax)
    stepAmt = int(36/(frequency/24))
    increment = maxVal//stepAmt
    tStep = halfCycle/stepAmt
    overHeadConstant = 0.000625
    while True:
        if (GPIO.input(btn) == 0):
            return
        for i in range(0, maxVal+1, increment):
            dac.raw_value = maxVal
        for i in range(stepAmt*increment, -1, -increment):
            dac.raw_value = 0
    return

def waveformTriangle():
    halfCycle = 1.0/(2.0*frequency)
    maxVal = int(4095.0*voltageMax/absMax)
    stepAmt = int(36/(frequency/24))
    increment = maxVal//stepAmt
    tStep = halfCycle/stepAmt
    overHeadConstant = 0.000625
    while True:
        if (GPIO.input(btn) == 0):
            return
        for i in range(0, maxVal+1, increment):
            dac.raw_value = i
        for i in range(stepAmt*increment, -1, -increment):
            dac.raw_value = i
    return

def waveformSin():
    fullCycle = 1.0/frequency
    maxVal = int(4095.0*voltageMax/absMax)
    stepAmt = int(35/(frequency/50))
    tStep = fullCycle/stepAmt
    while True:
        if (GPIO.input(btn) == 0):
            return
        for i in range(0,stepAmt+1,1):
            dac.raw_value=int(maxVal*(sin(pi*2*i/float(stepAmt))+1)/2.0)

    return
funcDict = {"1": waveformSquare, "2": waveformTriangle, "3": waveformSin}

def main():
    setup()
    dac.raw_value = 0
    while True:
        if (GPIO.input(btn) == 0):
            btnPress()

if __name__ == "__main__":
    main()
