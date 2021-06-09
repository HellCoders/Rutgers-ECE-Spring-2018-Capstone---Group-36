import threading
import numpy

import random

# globals referenced
lightList = []
lightAvg = 0
tempList = []
tempAvg = 0
humidList = []
humidAvg = 0
motionList = []
motionSum = 0

# for the purpose of testing only.
def mockData():
	return random.randint(1,100)

def second():
	# replace mockData() with functions that return values of a sensor
	lightList.append(mockData())
	tempList.append(mockData())
	humidList.append(mockData())
	motionList.append(mockData()) # motion sensor return 1 or 0 (yes / no)
	threading.Timer(1.0, second).start()
def minute():
	# reference all globals
	global lightList, tempList, humidList, motionList
	global lightAvg, tempAvg, humidAvg, motionSum
	sendFlag = False
	lightNew = int(numpy.average(lightList))
	lightList = []
	tempNew = int(numpy.average(tempList))
	tempList = []
	motionNew = int(numpy.sum(motionList))
	motionList = []
	if (lightAvg != lightNew):
		lightAvg = lightNew
		sendFlag = True
	if (tempAvg != tempNew):
		tempAvg = tempNew
		sendFlag = True
	if (motionNew != 0):
		motionSum = motionNew
		sendFlag = True
	if (sendFlag):
		# now we pipe / send via MQTT
		print("light: " + str(lightAvg) + "\ntemp: " + str(tempAvg) + "\nhumid: " + str(tempAvg) + "\nmotion: " + str(motionSum))

		##INSERT CODE TO SEND DATA TO PIPE "pipe" BELOW

	# for testing, change from 60.0 to 5.0
	threading.Timer(60.0, minute).start()

second()
minute()
