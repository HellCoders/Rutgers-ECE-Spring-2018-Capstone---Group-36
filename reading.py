import os, time, sys
import TSL2561_Driver
pipe_name = 'Sensors'

def write_data( ):
    # Opens a named pipe that you can only write to
    pipeout = os.open(pipe_name, os.O_WRONLY)

    # Reads in data from the sensors
    Lux, Full, Infrared, Visible = TSL2561_Driver.readLux(0)
    # To allow for enough time for Raspberry Pi 3 to
    # properly gain sensor information from sensors
    time.sleep(1)
    # Sends sensor information to the pipe
    os.write(pipeout, 'Lux: %d\n' %Lux)
    # To allow for enough time for Raspberry Pi 3 to
    # send information before needing to gain the
    # sensor information to send to the pipe again
    time.sleep(0.5)
        
def read_data( ):
    # Opens a named pipe to read information from
    pipein = open(pipe_name, 'r+')

    # This reads in the line from the pipe whilst removing the last character
    line = pipein.readline()
    pipein.close()
    print 'Java got %s' %line

# If the pipe doesn't exist, the pipe will be created
if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

# Reading data from pipe!
while True:
	read_data()
        write_data()
