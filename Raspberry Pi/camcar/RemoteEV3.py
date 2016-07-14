import _thread as thread
import sys
import socket
import time

class EV3:
    # Sensor + Motor encoder ports + Motor ports
    inPorts = ('in1', 'in2', 'in3', 'in4', 'outA', 'outB', 'outC', 'outD')
    outPorts = ('outA', 'outB', 'outC', 'outD')

    def __init__(self, ip):
        # Create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # reuse the address and connect to the ev3
        ev3_address = (ip, 10000)
        self.sock.connect(ev3_address)
        print('Connected to EV3')

        # Create the input data
        self.sensorData = ['0', '0', '0', '0', '0', '0', '0', '0']

        # Wait for the ev3 to start up
        time.sleep(.3)

        # Create the input thread
        thread.start_new_thread(self.handleInput, (self.sock,))

    def handleInput(self, sock):
        try:
            while 1:
                # Wait for a message
                data = sock.recv(256).decode()
                commands = data.split('\n')
                for command in commands:
                    self.handleInputCommand(command)
        finally:
            sock.close()

    def handleInputCommand(self, command):
        # Return if there's no command
        if not command: return

        # Read the command
        args = command.split(' ')

        # Get the type of command
        if args[0] == 'sns':
            self.sensorCommand(args)

    def sensorCommand(self, args):
        # Read the port and data arguments
        port = args[1]
        sensData = args[2]

        # The first argument must be a sensor port
        if port not in self.inPorts:
            print('{} is not a sensor port.'.format(port))
            return
        # Store the second argument in the sensor data
        portNum = self.inPorts.index(port);
        self.sensorData[portNum] = sensData

    def readSensor(self, port):
        # Return if the port has an ivalid format
        if port not in self.inPorts:
            print('{} is not a sensor port.'.format(port))
            return

        portNum = self.inPorts.index(port)
        dataString = self.sensorData[portNum]
        return int(dataString)

    def changeSensorMode(self, port, mode):
        data = 'mod ' + port + ' ' + mode + '\n'
        self.sock.send(data.encode())

    def changeMotorStopMode(self, port, mode):
        data = 'stm ' + port + ' ' + mode + '\n'
        self.sock.send(data.encode())

    def runMotor(self, port, speed):
        # Return if the port has an invalid format
        if port not in self.outPorts:
            print('{} is not a motor port.'.format(port))
            return

        # Send the command to run the motor
        if self.sock:
            data = 'mot ' + port + ' ' + str(int(speed)) + '\n'
            self.sock.send(data.encode())

    def runMotorTimed(self, port, speed, run_time):
        # Run the motor
        self.runMotor(port, speed)

        # Sleep
        time.sleep(run_time / 1000)

        # Stop the motor
        self.stopMotor(port)

    def runMotorRelative(self, port, pos, speed):
         # Send the command to run the motor
        if self.sock:
            data = 'mrl ' + port + ' ' + str(pos) + ' ' + str(int(speed)) + '\n'
            self.sock.send(data.encode())

    def runMotorAbsolute(self, port, pos, speed):
         # Send the command to run the motor
        if self.sock:
            data = 'mab ' + port + ' ' + str(pos) + ' ' + str(int(speed)) + '\n'
            self.sock.send(data.encode())

    def stopMotor(self, port):
        # Simply runs the motor with a speed of 0
        self.runMotor(port, 0)


# Test the ev3
if (__name__ == '__main__'):
    ev3 = EV3('ev3dev')

    ev3.changeMotorStopMode('outA', 'brake')
    ev3.changeMotorStopMode('outB', 'hold')
    ev3.changeMotorStopMode('outC', 'brake')
    ev3.changeMotorStopMode('outD', 'brake')

    ev3.runMotorRelative('outC', -90, 50)
    ev3.runMotorRelative('outD', -60, 50)

    ev3.changeSensorMode('in3', 'COL-AMBIENT')
    ev3.changeSensorMode('in4', 'COL-AMBIENT')

    ev3.runMotorTimed('outA', -50, 300)

    time.sleep(2)
    
    ev3.changeSensorMode('in3', 'COL-REFLECT')
    ev3.changeSensorMode('in4', 'COL-REFLECT')

    ev3.runMotorTimed('outA', 60, 350)

    time.sleep(1)
    
    ev3.changeSensorMode('in3', 'COL-COLOR')
    ev3.changeSensorMode('in4', 'COL-COLOR')

    ev3.runMotorTimed('outA', -30, 250)
    
    ev3.changeMotorStopMode('outC', 'hold')

    ev3.runMotorAbsolute('outC', 0, 40)
    ev3.runMotorAbsolute('outD', 0, 40)

    while 1:
        print(ev3.readSensor('in3'))
        time.sleep(0.1)
