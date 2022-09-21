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

def s1DataGens2DataClean():
    dxList, maxList, minList, waveTotal, waveArr = [],[],[],[],[]
    curVal, gloVal = 0,0
    curVal = channel.value
    waveTotal.append(curVal)
    curVal = channel.value
    waveTotal.append(curVal)
    dxList.append(1 if waveTotal[1] > waveTotal[0] else -1)
    gloVal = curVal
    for i in range(0, rPSInt+1,1):
        curVal = channel
        if (abs(curVal - gloVal) > int(tolInt)):
            gloVal = curVal
            waveTotal.append(gloVal)
            if(waveTotal[len(waveTotal)-1] - waveTotal[len(waveTotal)-2] > 0):
                dxList.append(1)
                if (dxList[len(dxList)-2] != 1):
                    minList.append(len(waveTotal)-1)
            else:
                dxList.append(-1)
                if(dxList[len(dxList)-2]!= -1):
                    maxList.append(len(waveTotal)-1)
        else:
            waveTotal.append(gloVal)
            dxList.append(dxList[len(dxList)-1])
    # waveTotal is all data points gathered within an entire second of an unknown waveform.
    if (maxList[1] > minList[1]):
        return (len(maxList)+len(minList))/2,waveTotal[maxList[1]:minList[2]+1]
    else :
        return (len(maxList)+len(minList))/2,waveTotal[maxList[1]:minList[2]+1]
def s3Eval(waveArr):
    # waveArr is a subsection of the array containing a the max and min of the single waveform from the 25% and 75% marker. 
    ret = "ans"
    return ret

def main():
    curWave = ""
    globalWave = ""
    while True:
        freqInt, waveArr = s1DataGens2DataClean()
        print("Frequency : ",  freqInt)
        curWave = s3Eval(waveArr)
        if (globalWave != curWave):
            globalWave = curWave
            print("New Waveform detected : ", globalWave)
        sleep(iInt)

if __name__ == "__main__":
    main()
