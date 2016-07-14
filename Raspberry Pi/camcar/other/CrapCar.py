import socket
import sys
import thread
import picamera
import ImageTools
import DataHandler


# Waits for new data and handles the input
def inputThread(connection):
	while 1:
		# Read the data
		data = connection.read()
		handleInput(data)

# Handle the input
def handleInput(data):
	args = data.split(' ')
	if args[0] == 'touch1'
		

# Handle the connection
def handleConnection(camera, connection):
	# Read the input and send the data
	detectColor = (0 ,0, 255)
	pixel = ImageTools.detectColor(camera, detectColor)
	direction = float(pixel[0]) / camera.resolution[0] * 2 - 1

	# Create left speed factor and increase when robot is turning left
	leftSpeedFactor = 1
	if direction > 0:
		leftSpeedFactor = 1 + direction

	# Create right speed factor and increase when robot is turning right
	rightSpeedFactor = 1
	if direction < 0:
		rightSpeedFactor = 1 - direction

	# Create left and right speeds
	leftSpeed = int(leftSpeedFactor * motorSpeed)
	rightSpeed = int(rightSpeedFactor * motorSpeed)
	print(str(leftSpeed) + ', ' + str(rightSpeed))

	# Send the values to the ev3 connection
	connection.send('left run ' + str(leftSpeed))
	connection.send('right run ' + str(rightSpeed))


# Create a camera
camera = picamera.PiCamera()
camera.resolution = (64, 48)
motorSpeed = 25

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# reuse the address and bind the socket to the port
server_address = ('0.0.0.0', 10000)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while 1:
	# Wait for a connection
	print >>sys.stderr, 'Waiting for a connection...'
	connection, client_address = sock.accept()

	try:
		print('Connected to EV3')

		# Start the input handler thread
		thread.start_new_thread( inputThread, (connection) )

		# Send the actions to the motors
		while 1:

			# Handle the connection (gets the camera input and sends commands to the ev3)
			handleConnection(camera, connection)

	except Exception, e:
		print('Error: ' + str(e))
		print('Trying to reconnect...')

	finally:
		# Clean up the connection
		connection.close()
