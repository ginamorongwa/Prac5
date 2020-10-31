import time
import threading
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.CE0)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P1)

my_time = 0
tick = time.time()



def my_thread():
	global tick
	global chan
	thread = threading.Timer(10.0, my_thread)
	thread.daemon = True
	thread.start()
	#print('Raw ADC Value: ', chan.value)
	#print('ADC Voltage: ' + str(chan.voltage) + 'V')
	tock = int(time.time() - tick)
	print(str(tock) + "s		" + str(chan.value) + "			" + "0" + " C")

if __name__ == "__main__":
	try:
		print("Runtime		Temp Reading		Temp")
		my_thread() # call it once to start the thread
		# tell our program to run indefinitely
		while True:
			pass
	except KeyboardInterrupt as k:
		print("Goodbye")
	except Exception as e:
		print(e)
	finally:
		pass
