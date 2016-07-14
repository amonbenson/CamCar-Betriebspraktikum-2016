#!./run.sh /usr/bin/python
#
# CamCar.py is a simple receiver program that decodes a protocoll
# to transmit ev3 motor and sensor data. It will translate the
# commands to the sensors / motors and directly controls them
#
#
#
# The Raspberry can send these commands:
#
# mot <port> <speed>        This will turn the motor at the specific port
#                           (outA, outB, outC or outD). The speed is an
#                           Integer value from -100 to 100 (negative speed
#                           means backwards rotation)
#
# mrl <port> <pos> <speed>
#                           This will run the motor to a relative position.
# mab <port> <pos> <speed>
#                           This will run the motor to an absolute position.
#
# mod <port> <mode>         This will change the mode of the sensor at the
#                           given port to the mode string given by <mode>.
#
# stm <port> <command>      This will set the stop mode. It can either be 
#                           'coast', 'break' and 'hold'. Coast will only
#                           remove the power, break will break down the
#                           movement and hold holds the motor at the position.
#
#
#
# The EV3 can send these commands
#
# sns <port> <data>         This will transmit the raw values from the
#                           sensors at the specific port (in1, in2, in3
#                           or in4). The data can be any value depending
#                           on the type of the connected sensor. Also there
#                           will be sent data on the motor ports, these are
#                           for the encoder position
#
#
#
# author: Amon Benson



# Do the imports
import thread
import sys, traceback
import socket
from ev3dev.core import *


# This will be called by a thread and checks for incoming messages (that the
# Raspberry Pi sends).
def handleInput(sock):
    try:
        while 1:
            # Wait for a message
            data = sock.recv(256)
            if not data: raise EOFError('No more data')
            commands = data.split('\n')
            for command in commands:
                if command:
                    handleInputCommand(command)
    except:
        print('Socket connection failed!')
        traceback.print_exc(file=sys.stdout)
        # Stop all motors and close the sock
        motorCommand(('mot', 'outA', '0'))
        motorCommand(('mot', 'outB', '0'))
        motorCommand(('mot', 'outC', '0'))
        motorCommand(('mot', 'outD', '0'))
        sock.close()


# This will check one single command (the Raspberry may send multiple commands
# at once so the handleInput() has to separate them and this method separates
# the single arguments.
def handleInputCommand(command):
    # Get the single arguments
    args = command.split(' ')
    print('[RASPBERRY PI] \033[1;32;40m' + command + '\033[1;37;40m')

    # Get the type of command (the first argument)
    if args[0] == 'mot':
        motorCommand(args)
    elif args[0] == 'mrl':
        motorRelativeCommand(args)
    elif args[0] == 'mab':
        motorAbsoluteCommand(args)
    elif args[0] == 'stm':
        motorStopModeCommand(args)
    elif args[0] == 'mod':
        sensorModeCommand(args)
    else:
        print('Unknown command: ' + args[0])


# This runs a motor by the given arguments (note that args[0] is not used
# because it already defines the type of command @see handleInputCommand).
def motorCommand(args):
    port = args[1]
    speed = args[2]

    if port == 'outA' and motA is not None:
        motA.run_forever(duty_cycle_sp=speed)
    if port == 'outB' and motB is not None:
        motB.run_forever(duty_cycle_sp=speed)
    if port == 'outC' and motC is not None:
        motC.run_forever(duty_cycle_sp=speed)
    if port == 'outD' and motD is not None:
        motD.run_forever(duty_cycle_sp=speed)


# This will turn a specific motor to a relative position
def motorRelativeCommand(args):
    port = args[1]
    pos = args[2]
    speed = args[3]

    mot = getMotor(port)
    if mot is not None:
        mot.run_to_rel_pos(position_sp=pos, duty_cycle_sp=speed)


# This will turn a specific motor to an absolute position
def motorAbsoluteCommand(args):
    port = args[1]
    pos = args[2]
    speed = args[3]

    mot = getMotor(port)
    if mot is not None:
        mot.run_to_abs_pos(position_sp=pos, duty_cycle_sp=speed)


# Sets the stop mode of a motor
def motorStopModeCommand(args):
    port = args[1]
    mode = args[2]

    mot = getMotor(port)
    if mot is not None:
        mot.stop_command = mode


# Gets the motor at the specified port
def getMotor(port):
    return eval('mot' + port[-1])


# This changes the mode of a specific sensor
def sensorModeCommand(args):
    port = args[1]
    mode = args[2]

    if port == 'in1' and sns1 is not None:
        sns1.mode = mode
    if port == 'in2' and sns2 is not None:
        sns2.mode = mode
    if port == 'in3' and sns3 is not None:
        sns3.mode = mode
    if port == 'in4' and sns4 is not None:
        sns4.mode = mode


# This sends the sensor data to all connected sockets
def sendSensorData(sock):
    # Sensors
    if sns1 is not None:
        sock.send(getSensorData('in1', sns1))
    if sns2 is not None:
        sock.send(getSensorData('in2', sns2))
    if sns3 is not None:
        sock.send(getSensorData('in3', sns3))
    if sns4 is not None:
        sock.send(getSensorData('in4', sns4))
    # Motor encoders
    #if motA is not None:
    #    sock.send(getMotorData('outA', motA))
    #if motB is not None:
    #    sock.send(getMotorData('outB', motB))
    #if motC is not None:
    #    sock.send(getMotorData('outC', motC))
    #if motD is not None:
    #    sock.send(getMotorData('outD', motD))


# Returns the sensor data value.
def getSensorData(port, sns):
    # Creat the data string and get the values depending on the type of sensor
    data = 'sns ' + port + ' '
    data += str(sns.value()) + '\n'
    # Return the data string
    return data

# Returns the motor encode data value.
def getMotorData(port, mot):
    # Create the data string
    data = 'sns ' + port + ' '
    data += str(mot.position) + '\n'
    # Return the datat string
    return data




# Start the main script
print('Initializing...')

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a local server
server_address = ('0.0.0.0', 10000)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(5)

# Create the motors and sensors
motA = LargeMotor('outA')   # Eyes
motB = MediumMotor('outB')  # Camera
motC = LargeMotor('outC')   # Left wheel
motD = LargeMotor('outD')   # Right wheel
sns1 = None
sns2 = None
sns3 = ColorSensor('in3')   # Left eye
sns4 = ColorSensor('in4')   # Right eye

# Wait for a client to connect
while 1:
    try:
        print('Waiting for a connection...')
        clientSock, address = sock.accept()
        print('Connected to Raspberry Pi (' + str(address) + ')')

        # Create the input thread
        thread.start_new_thread(handleInput, (clientSock,))

        # Constantly send the sensor data
        sendSensorData(clientSock)

    except Exception:
        print('Socket connection failed!')
        traceback.print_exc(file=sys.stdout)
