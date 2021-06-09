# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2561
# This code is designed to work with the TSL2561_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TSL2561_I2CS#tabs-0-product_tabset-2

import smbus
import time

TSLaddr = 0x39 #Default I2C address, alternate 0x29, 0x49 
TSLcmd = 0x80 #Command
chan0 = 0x0C #Read Channel0 sensor date
chan1 = 0x0E #Read channel1 sensor data
TSLon = 0x03 #Switch sensors on
TSLoff = 0x00 #Switch sensors off
#Exposure settings
LowShort = 0x00 #x1 Gain 13.7 miliseconds
LowMed = 0x01 #x1 Gain 101 miliseconds
LowLong = 0x02 #x1 Gain 402 miliseconds
LowManual = 0x03 #x1 Gain Manual
HighShort = 0x10 #LowLight x16 Gain 13.7 miliseconds
HighMed = 0x11	#LowLight x16 Gain 101 miliseconds
HighLong = 0x12 #LowLight x16 Gain 402 miliseconds
HighManual = 0x13 #LowLight x16 Gain Manual
# Get I2C bus
bus = smbus.SMBus(1)
writebyte = bus.write_byte_data

def PowerOn():
        # Using default TSL2561 address, TSLaddr = 0x39. To power on our sensor, We
        # first select the control register, 0x00, with command register,
        # TSLcmd = 0x80, and use the power on setting, TSLon = 0x03
        bus.write_byte_data(TSLaddr, 0x00 | TSLcmd, TSLon)

def PowerOff():
        # Using default TSL2561 address, TSLaddr = 0x39. To power off our sensor, We
        # first select the control register, 0x00, with command register,
        # TSLcmd = 0x80, and use the power off setting, TSLoff = 0x00
        bus.write_byte_data(TSLaddr, 0x00 | TSLcmd, TSLoff)
         
def Gain1xShort():
        # Using default TSL2561 address, TSLaddr = 0x39. To set an analog gain of 1
        # with an integration time of 13.7 miliseconds, we first select the timing
        # register, 0x01, with command register, TSLcmd = 0x80, and use the respective
        # gain setting
        bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, LowShort)

def Gain1xMed():
        # Using default TSL2561 address, TSLaddr = 0x39. To set an analog gain of 1
        # with an integration time of 101 miliseconds, we first select the timing
        # register, 0x01, with command register, TSLcmd = 0x80, and use the respective
        # gain setting
        bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, LowMed)

def Gain1xLong():
        # Using default TSL2561 address, TSLaddr = 0x39. To set an analog gain of 1
        # with an integration time of 402 miliseconds, we first select the timing
        # register, 0x01, with command register, TSLcmd = 0x80, and use the respective
        # gain setting
        bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, LowLong)

def Gain16xShort():
        # Using default TSL2561 address, TSLaddr = 0x39. To set an analog gain of 16
        # with an integration time of 13.7 miliseconds, we first select the timing
        # register, 0x01, with command register, TSLcmd = 0x80, and use the respective
        # gain setting
        bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, HighShort)

def Gain16xMed():
        # Using default TSL2561 address, TSLaddr = 0x39. To set an analog gain of 16
        # with an integration time of 101 miliseconds, we first select the timing
        # register, 0x01, with command register, TSLcmd = 0x80, and use the respective
        # gain setting
        bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, HighMed)

def Gain16xLong():
        # Using default TSL2561 address, TSLaddr = 0x39. To set an analog gain of 16
        # with an integration time of 402 miliseconds, we first select the timing
        # register, 0x01, with command register, TSLcmd = 0x80, and use the respective
        # gain setting
        bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, HighLong)

def setGain(gain):
        # Sets the gain. Gain can be either 1 or 16
        if gain == 1:
                Gain1xLong()
        elif gain == 16:
                Gain16xLong()

def readIR():
        time.sleep(0.5)

        # Read data back from 0x0E(14) with command register, TSLcmd(128), 2 bytes
        # ch1 LSB, ch1 MSB
        data1 = bus.read_i2c_block_data(TSLaddr, 0x0E | TSLcmd, 2)

        # Convert the data
        ch1 = data1[1] * 256 + data1[0]

        # Return data
        return ch1

def readVisible():
        time.sleep(0.5)

        # Read data back from 0x0C(12) with command register, TSLcmd(128), 2 bytes
        # ch0 LSB, ch0 MSB
        data = bus.read_i2c_block_data(TSLaddr, 0x0C | TSLcmd, 2)

        # Read data back from 0x0E(14) with command register, TSLcmd(128), 2 bytes
        # ch1 LSB, ch1 MSB
        data1 = bus.read_i2c_block_data(TSLaddr, 0x0E | TSLcmd, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]

        # Return the data
        return (ch0 - ch1)

def readFull():
        time.sleep(0.5)

        # Read data back from 0x0C(12) with command register, TSLcmd(128), 2 bytes
        # ch0 LSB, ch0 MSB
        data = bus.read_i2c_block_data(TSLaddr, 0x0C | TSLcmd, 2)

        # Convert the data
        ch0 = data[1] * 256 + data[0]

        # Return the data
        return ch0

def readLux(gain):
        time.sleep(0.5)

	# Low Gain
        if (gain == 1):
                setGain(gain)
                ch0 = readFull()
                ch1 = readIR()

        # High Gain
        elif (gain == 16):
                setGain(gain)
                ch0 = readFull()
                ch1 = readIR()
                ch0 = ch0 / 16
                ch1 = ch1 / 16
        
	# Auto Gain
        elif (gain == 0):
                setGain(16)
                ch0 = readFull()
                if (ch0 < 65535):
                        ch1 = readIR()
                        ch0 = readFull()
                        ch0 = ch0 / 16
                        ch1 = ch1 / 16
                if (ch0 >= 65535 or ch1 >= 65535):
                        setGain(1)
                        ch0 = readFull()
                        ch1 = readIR()

	# Might need following code for auto gain light sensing
	# if (gain == 1):
		#ch0 *= 16
		#ch1 *= 16
				
	# Calculates lux value
        ch0x = ch0*16
        ch1x = ch1*16
	
        ratio = (float(ch1x)/float(ch0x))
		
        if ((ratio >= 0) & (ratio <= 0.50)):
                lux = (0.0304 * ch0x) - (0.062 * ch0x * (ratio**1.4))
        elif (ratio <= 0.61):
                lux = (0.0224 * ch0x) - (0.031 * ch1x)
        elif (ratio <= 0.80):
                lux = (0.0128 * ch0x) - (0.0153 * ch1x) 
        elif (ratio <= 1.3):
                lux = (0.00146 * ch0x) - (0.00112 * ch1x)
        elif (ratio > 1.3):
                lux = 0
                
        # Returns the lux, full spectrum, infrared spectrum, and visible spectrum values
        return lux, ch0, ch1, (ch0 - ch1)
