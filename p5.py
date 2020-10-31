import time
import threading
import busio
import digitalio
import board
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# button pin
button = 25

# some global variables that need to change as we run the program
chan = None
tick = time.time()		# for runtime calculatons
sampling_rate = 1.0		# default sampling rate
thread = None			# thread changed if the sampling rate is changed


# setup pins
def setup():
	global button
	global chan

	# setup for the button
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(button, GPIO.RISING, callback=toggle_sampling_rate, bouncetime=300)

	# create the spi bus
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

	# create the cs (chip select)
	cs = digitalio.DigitalInOut(board.D5)

	# create the mcp object
	mcp = MCP.MCP3008(spi, cs)

	# create an analog input channel on pin 1
	chan = AnalogIn(mcp, MCP.P1)


def toggle_sampling_rate(channel):
	global sampling_rate
	global thread
	global tick

	# change sampling rate
	if sampling_rate == 1.0:
		sampling_rate = 5.0
	elif sampling_rate == 5.0:
		sampling_rate = 10.0
	else:
		sampling_rate = 1.0

	# reset timer
	tick = time.time()

	# stop: cancel, join
	thread.cancel()
	thread.join()

	# start thread again
	my_thread()


def calculate_temperature():
	global chan

	# get the voltage
	voltage = chan.voltage

	# convert to temperature
	temperature = (voltage - 0.5) / 0.01

	# return temperature
	return temperature


def get_runtime():
	global tick

	# calculate runtime
	tock = int(time.time() - tick)

	# return runtime
	return str(tock)


def my_thread():
	global thread
	global tick
	global chan

	# set timer and start the thread
	thread = threading.Timer(sampling_rate, my_thread)
	thread.daemon = True
	thread.start()

	# get runtime and temperature
	runtime = get_runtime()
	temperature = calculate_temperature()
	value = chan.value

	# display
	print("%ss\t\t%d \t\t\t%.2f C" %(runtime, value, temperature))
	#print( + "s		" + str(chan.value) + "			" + calculateTemp()  + " C"+" Sampling rate: "+str(sampling_rate)+" tick: "+str(tick)+" voltage: "+str(chan.voltage))


if __name__ == "__main__":
	try:
		print("Runtime		Temp Reading		Temp")
		setup()
		my_thread() # call it once to start the thread
		# tell our program to run indefinitely
		while True:
			pass
	except KeyboardInterrupt as k:
		print("Goodbye")
	except RuntimeError as r:
		pass
	except Exception as e:
		print(e)
	finally:
		GPIO.cleanup()
