from math import sin, pi
from time import sleep
import wave
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
//Will create 3 functions for sine triangle and square if needed.
'''

# Setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create spi bus
cs = digitalio.DigitalInOut(board.D22) # create chip select
mcp = MCP.MCP3008(spi, cs) # create mcp object
channel = AnalogIn(mcp, MCP.P0) # create analog input channel on pin 0

print('Raw ADC Value: ', channel.value)

# Hardware dependent values
rPSInt = 1024 # Integer reads per second
iInt = 1 # Float time before next check
tolInt = 0 # Integer tolerance value 

def s1DataGen():
    waveTotal = []
    for i in range(0,rPSInt+1,1):
        waveTotal.append(channel.value)
    return waveTotal

def s2DataClean(waveTotal):
    # waveTotal is all data points gathered within an entire second of an unknown waveform
    freqInt = 0
    waveArr = []
    return freqInt,waveArr

def s3Eval(waveArr):
    # waveArr is a subsection of the array containing a single full cycle of an unknown waveform.
    ret = "ans"
    return ret

def main():
    curWave = ""
    globalWave = ""
    while True:
        waveTotal = s1DataGen()
        
        freqInt , waveArr = s2DataClean(waveTotal)
        print("Frequency : ",  freqInt)

        curWave = s3Eval(waveArr)
        if (globalWave != curWave):
            globalWave = curWave
            print("New Waveform detected : ", globalWave)
        sleep(iInt)

if __name__ == "__main__":
    main()
