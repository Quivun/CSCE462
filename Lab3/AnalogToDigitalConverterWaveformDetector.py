from math import sin, pi
from re import X
import time
import wave
from adafruit_mcp3xxx.analog_in import AnalogIn

# import os
import busio
import digitalio
import board
import matplotlib.pyplot as plt
# import adafruit_mcp4725
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO

"""
dac.raw_value = [0,4095]
Channel.value = [0,(2^16)-1] Integer
Channel.voltage = [0,3.3 (Or 5.0 maybe?)] Float 
"""

# Setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)  # create spi bus
cs = digitalio.DigitalInOut(board.D22)  # create chip select
mcp = MCP.MCP3008(spi, cs)  # create mcp object
channel = AnalogIn(mcp, MCP.P0)  # create analog input channel on pin 0

# Hardware dependent values
rPSInt = 1000  # Integer reads per second
iInt = 1.0  # Float time before next check
tolInt = 0  # Integer tolerance of RAW value [0,65535]
tolDx = tolInt*13  # Integer tolerance of slope value [0,65535]
freq = 0
ran = 0
def s1DataGens2DataClean():
    global tolDX
    global ran
    dxList, maxList, minList, xList, yList = (
        [],
        [],
        [],
        [],
        [],
    )  # dx is to determine slope direction to populate maxList and minList (That will also provide the returned frequency and a sample of a wave). xList are the raw values taken in by reads from the ADC
    curVal, gloVal = (
        0,
        0,
    )  # curVal is an instance of ADC's read value while gloVal maintains consistency within a threshold tolerance.
    tolEffect = 1
    curVal = channel.value
    xList.append(curVal)
    curVal = channel.value
    xList.append(curVal)
    yList.append(len(yList))
    yList.append(len(yList))
    dxList.append(1 if xList[1] > xList[0] else -1)
    gloVal = curVal
    sTime = time.perf_counter()
    for i in range(
        0, rPSInt, 1
    ):  # Cycle a tested amount that is guaranteed 1 second real time for as many times we can read the channel value and populate each list accordingly.
        curVal = channel.value
        if (abs(curVal - gloVal) > int(tolInt)):
            tolEffect = 1
            gloVal = curVal
            xList.append(gloVal)
            yList.append(len(yList))
            if xList[len(xList) - 1] - xList[len(xList) - 2] > 0:
                dxList.append(1)
                if dxList[len(dxList) - 2] != 1:
                    minList.append(len(xList) - 2)
            else:
                dxList.append(-1)
                if dxList[len(dxList) - 2] != -1:
                    maxList.append(len(xList) - 2)
        else:
            xList.append(gloVal)
            yList.append(len(yList))
            dxList.append(dxList[len(dxList) - 1])
    eTime = time.perf_counter()
    """
    maxAvg = sum(maxList)/len(maxList)
    minAvg = sum(minList)/len(minList)
    
    varMax = 0
    for i in maxAvg:
        varMax += abs(xList[i] - maxAvg)
    varMax /= len(maxList)
    stdMax = varMax**0.5
    
    varMin = 0
    for i in minAvg:
        varMin += abs(xList[i] - minAvg)
    varMin /= len(minList)
    stdMin = varMin**0.5
    """
    """
    maxVals = []
    minVals = []
    for i in maxList:
        maxVals.append(xList[i])
    for i in minList:
        minVals.append(xList[i])
    maxVals.sort()
    minVals.sort()
    maxQ1 = maxVals[int(0.25*(len(maxVals)-1))]
    maxQ3 = maxVals[int(0.75*(len(maxVals)-1))]
    maxIQR = maxQ3 - maxQ1
    itr = 0
    while (itr < len(maxList)):
        if xList[maxList[itr]] > maxQ3+maxIQR*1.5:
            maxList.remove(maxList[itr])
            itr-=1
        elif xList[maxList[itr]] < maxQ1-maxIQR*1.5:
            maxList.remove(maxList[itr])
            itr-=1
        itr+=1
    minQ1 = minVals[int(0.25*(len(minVals)-1))]
    minQ3 = minVals[int(0.75*(len(minVals)-1))]
    minIQR = minQ3 - minQ1
    itr = 0
    while (itr < len(minList)):
        if xList[minList[itr]] > minQ3+minIQR*1.5:
            minList.remove(minList[itr])
            itr-=1
        elif xList[minList[itr]] < minQ1-minIQR*1.5:
            minList.remove(minList[itr])
            itr-=1
        itr+=1
    """
    sMax = 0
    sMin = 0
    for i in maxList:
        sMax+=xList[i]
    for i in minList:
        sMin+=xList[i]
    #print(sMax/len(maxList))
    #print(sMin/len(minList))
    ran = sMax/len(maxList) - sMin/len(minList)
    #print("Max List", maxList)
    #print("Min List", minList)
    #print("X List", xList)
    #print("dx List", dxList)
    #(eTime-sTime, " is the Elapsed time it took for ", rPSInt, " value reads")
    plt.plot(yList,xList,label="L1")
    plt.show()
    maInd = maxList[len(maxList)-5]
    miInd = 0
    for i in range(len(minList)-1, -1,-1):
        if (minList[i] < maInd):
            break
        miInd = minList[i]
    #(maInd,miInd)
    return (len(maxList) + len(minList)) / 2 / (eTime-sTime), xList[maInd+1 : miInd-1], xList
    

"""
def s3Eval(waveArr):
    global freq
    # waveArr is a subsection of the array containing a the max and min of the single waveform from the 25% and 75% marker.
    xList = [i for i in range(len(waveArr))]
    plt.plot(xList, waveArr, label = "L2")
    plt.show()
    dx1 = waveArr[int(len(waveArr) * 0.25) - 1] - waveArr[0]
    if dx1 == 0:
        if (waveArr[int(len(waveArr) * 0.25) - 1]-waveArr[int(len(waveArr) * 0.75) - 1] < 10):
            return "Square"
    slope = (waveArr[int(len(waveArr))-1]-waveArr[0])/len(waveArr)
    variance = 0
    for i in range(len(waveArr)):
        variance += abs(waveArr[i] - waveArr[0]+slope*i)**2
    variance /= len(waveArr)
    standardDev = variance**0.5
    print(standardDev,freq)
    dx2 = waveArr[int(len(waveArr) * 0.75) - 1] - waveArr[int(len(waveArr) * 0.25) - 1]
    print(int(12000/(freq*0.048)))
    if standardDev < int(12000/(freq*0.048)):
        return "Triangle"
    else:
        return "Sine"  # dx3 = waveArr[int(len(waveArr)-1)] - waveArr[int(len(waveArr)*0.75 - 1)]
"""
def s3EvalFULL(waveArr):
    global freq
    global rPSInt
    global ran
    avg = sum(waveArr)/len(waveArr)
    var = 0
    for i  in range(len(waveArr)):
        var +=abs(waveArr[i] - avg)**2
    stdDev = var**0.5
    print(stdDev/(8.6*ran*2.0), stdDev/(2.0*3.98*ran*2**0.5), stdDev/(ran*3.0*12**0.5),ran)
    #Standard Deviation for all three are notably different, find the dividing points in between and classify by observing which is closest to the normalized number 1 in respect to range of voltage
    varArr = [abs(1-stdDev/(8.6*ran*2.0)), abs(1-stdDev/(2.0*3.98*ran*2**0.5)), abs(1-stdDev/(ran*3.0*12**0.5))]
    # Locate the minimum difference between the normalized number (That's denoted standard deviation is associated with the wave). This will deteremine the waveform type
    minValue = min(varArr)
    # It's organized with Square first, Sine second, and Triangle third
    waveFormAns = ["Square","Sine", "Triangle"]
    for i in range(3):
        if varArr[i] == minValue:
            return waveFormAns[i]
    return 0

def main():
    # The scope of accuracy applies from 1 hz to 1750 hz assumed.
    global freq
    curWave = ""
    globalWave = "NULL"
    while True:
        freqInt, waveArr, fullWave= s1DataGens2DataClean()
        freq = freqInt
        print("Frequency : ", freqInt)
        curWave = s3EvalFULL(fullWave)
        if globalWave != curWave:
            globalWave = curWave
            # Might implement a double check before outputting new Waveform official. Why? Because the waveform and frequency may be changed mid read.
            #print("New Waveform detected : ", globalWave)
        print("Waveform Current : ", globalWave)
        time.sleep(iInt)


if __name__ == "__main__":
    main()
