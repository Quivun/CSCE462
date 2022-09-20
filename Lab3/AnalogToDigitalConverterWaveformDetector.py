from math import sin, pi
from time import sleep
from adafruit_mcp3xxx.analog_in import AnalogIn

#import os
import busio
import digitalio
import board
import adafruit_mcp4725
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO

'''
dac.raw_value = [0,4095]
Channel.value = [0,(2^16)-1] Integer
Channel.voltage = [0,3.3 (Or 5.0 maybe?)] Float 
//This shall be our reference within data.
'''

# Setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create spi bus
cs = digitalio.DigitalInOut(board.D22) # create chip select
mcp = MCP.MCP3008(spi, cs) # create mcp object
chan0 = AnalogIn(mcp, MCP.P0) # create analog input channel on pin 0

print('Raw ADC Value: ', chan0.value)

# Hardware dependent values
rPSInt = 1024 # Integer reads per second
iInt = 1 # Float time before next check
def s1DataGen():
    ret = {}
    return ret

def s2Eval():
    ret = "ans"
    return ret

def main():
    curWave = ""
    globalWave = ""
    while True:
        freqInt , waveArr = s1DataGen()
        print("Frequency : ",  freqInt)
        curWave = s2Eval(waveArr)
        if (globalWave != curWave):
            globalWave = curWave
            print("New Waveform detected : ", globalWave)
        sleep(iInt)

if __name__ == "__main__":
    main()
