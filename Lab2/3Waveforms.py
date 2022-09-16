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
funcDict = {"1": waveformSquare, "2": waveformTriangle, "3": waveformSin}
i2c = I2C(board.SCL, board.SDA)  # Initialize I2C bus.

#Globals
dac = adafruit_mcp4725.MCP4725(i2c)  # Initialize MCP4725.
delta = False
waveform = "NULL"
frequency = 0
voltageMax = 0.01
absMax = 3.3

def setup():
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
    return (funcDict[waveform]())

def waveformSquare():
    halfCycle = 1.0/(2.0*frequency)
    while changeCheck():
        dac.set_voltage = int(4095.0*voltageMax/absMax)
        sleep(halfCycle)
        dac.set_voltage = 0
        sleep(halfCycle)
    return

def waveformTriangle():
    halfCycle = 1.0/(2.0*frequency)
    maxVal = int(4095.0*voltageMax/absMax)
    stepAmt = 29
    increment = maxVal//stepAmt
    tStep = halfCycle//stepAmt
    overHeadConstant = 0.0003
    if (tStep < overHeadConstant):
        while changeCheck():
            for i in range(0, maxVal+1, increment):
                dac.raw_value = i
            for i in range(stepAmt*maxVal, -1, increment):
                dac.raw_value = i
    else:
        while delta:
            for i in range(0, maxVal+1, increment):
                dac.raw_value = i
                sleep(tStep - overHeadConstant)
            for i in range(stepAmt*maxVal, -1, increment):
                dac.raw_value = i
                sleep(tStep - overHeadConstant)
    return


def waveformSin():
    fullCycle = 1.0/frequency
    maxVal = int(4095.0*voltageMax/absMax)
    tStep = fullCycle/maxVal
    stepAmt = 16 # Powers of 4 should be the step amount for balanced demonstration
    while changeCheck():
        for i in range(0,stepAmt+1,1):
            dac.raw_value(int(maxVal*(sin(pi*2*i/float(stepAmt))+1)/2.0))
    return


def main():
    setup()
    dac.raw_value = 0
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=btnPress)
    while(True):
        pass


if __name__ == "__main__":
    main()
