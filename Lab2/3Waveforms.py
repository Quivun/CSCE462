import board
import busio
import adafruit_mcp4725
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

from busio import l2c
from time import sleep
from math import sin,pi

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

# Globals delta,waveform,frequency,voltageMax

funcDict = {"1" : waveformSquare, "2" : waveformTriangle, "3" : waveformSin}

def setup():
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

def btnPress():
    global delta
    if (delta):
        delta = False
    global waveform
    global frequency
    global voltageMax
    waveform = input("Enter Waveform : 1 for Square, 2 for Triangle, and 3 for Sin : ")
    frequency = int(input("Enter, in hertz, the frequency of the wave : "))
    voltageMax = float(input("Input maximum voltage [Less than or equal to 3.3V, will default to [0,3.3] if beyond either bounds : "))
    delta = True
    return (funcDict[waveform]())

def waveformSquare():
    global delta
    global dac
    halfCycle = 1.0/(2.0*frequency)
    while delta:
        dac.set_voltage(int(voltageMax))
        sleep(halfCycle)
        dac.set_voltage(int(voltageMax))
    return

def waveformTriangle():
    global dac
    halfCycle = 1.0/(2.0*frequency)
    maxVal = int(4095.0*voltageMax/3.3)
    tStep = halfCycle/maxVal
    while delta:
        for i in range(maxVal):
            dac.raw_value = i
            sleep(tStep)
        for i in range(maxVal, -1, -1):
            dac.raw_value = i
            sleep(tStep)
    return
        

def waveformSin():
    global dac
    t = 0.0
    fullCycle = 1.0/frequency
    maxVal = int(4095.0*voltageMax/3.3)
    tStep = fullCycle/maxVal
    while delta:
        if (t > 1):
            t-=1
        dac.raw_value(int((maxVal*sin(pi*2*t)+1)/2.0))
        t += tStep
        sleep(tStep)
    return
    
def main():
    global dac
    setup()
    i2c = busio.I2C(board.SCL, board.SDA) # Initialize I2C bus.
    dac = adafruit_mcp4725.MCP4725(i2c) # Initialize MCP4725.
    # dac.value[0,65525], dac.raw_value[0,4095], dac.normalized_value[0,1.0](Floating Point)
    # "If you need the most precise output use the raw_output value for setting voltage." - Adafruit
    dac.raw_value = 0
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=btnPress)


if __name__ == "__main__":
    main()
