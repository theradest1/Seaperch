import pygame  # pip install pygame
import time
import serial  # pip install pyserial
import os

# inputs
leftStick = (0, 0)
rightStick = (0, 0)
leftTrigger = 0
rightTrigger = 0

# outputs
frontMotor = 0  # facing up: 1
backMotor = 0  # facing up: 2
leftMotor = 0  # facing forward: 3
rightMotor = 0  # facing forward: 4

arduinoPort = "COM4"  # "/dev/ttyACM0"  #
controller = ""  # for normalizing
updateInterval = 0.1  # in seconds


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


class device:
    def __init__(self, port, baud=9600):
        try:
            self.serial = serial.Serial(port, baud)
            print(f"Connected to arduino on port {port} with baud of {baud}")
            time.sleep(1)
            self.debugMode = False
        except:
            print("!!!!Couldn't connect to device, running in debug mode!!!!")
            time.sleep(3)
            self.debugMode = True

    def sendMessage(self, message):
        if not self.debugMode:
            self.serial.write((message + "\n").encode())
        else:
            # parse speeds
            front = int(message[0:4].lstrip("0").replace("N", "-") + "0") / 10
            back = int(message[4:8].lstrip("0").replace("N", "-") + "0") / 10
            left = int(message[8:12].lstrip("0").replace("N", "-") + "0") / 10
            right = int(message[12:16].lstrip("0").replace("N", "-") + "0") / 10

            # debug
            clear_terminal()
            print(f"Message: {message}")
            print(f"Front: {front}")
            print(f"Back: {back}")
            print(f"Left: {left}")
            print(f"Right: {right}")

    def close(self):
        if not self.debugMode:
            self.serial.close()


class controller:
    def __init__(self):
        # initialize pygame
        pygame.init()
        pygame.joystick.init()
        controller_count = pygame.joystick.get_count()

        # if no controller active
        if controller_count == 0:
            print("No controllers found.")
            exit()

        # initialize controller
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.name = str(self.controller.get_name())
        print(f"Connected to controller: {self.name}")
        time.sleep(1)

    def close(self):
        self.controller.quit()

    def setAxis(self, axis, value):
        global leftStick, rightStick, leftTrigger, rightTrigger

        if self.name == "Controller (dualSense)":  # use official name later (and test)
            if axis == 0:  # left stick X
                leftStick = (value, leftStick[1])
            elif axis == 1:  # left stick Y
                leftStick = (leftStick[0], -value)
            elif axis == 2:  # left trigger
                leftTrigger = (value + 1) / 2
            elif axis == 3:  # right stick X
                rightStick = (value, rightStick[1])
            elif axis == 4:  # right stick Y
                rightStick = (rightStick[0], -value)
            elif axis == 5:  # right trigger
                rightTrigger = (value + 1) / 2
            return
        elif self.name == "Controller (Gamepad F310)":
            if axis == 0:  # left stick X
                leftStick = (value, leftStick[1])
            elif axis == 1:  # left stick Y
                leftStick = (leftStick[0], -value)
            elif axis == 2:  # right stick X
                rightStick = (value, rightStick[1])
            elif axis == 3:  # right stick Y
                rightStick = (rightStick[0], -value)
            elif axis == 4:  # left trigger
                leftTrigger = (value + 1) / 2
            elif axis == 5:  # right trigger
                rightTrigger = (value + 1) / 2
            return

        print("NO CONTROLLER SCEME MADE FOR " + self.name)
        time.sleep(0.5)
        return


def debug():
    global leftStick, rightStick, leftTrigger, rightTrigger
    global frontMotor, backMotor, leftMotor, rightMotor
    # inputs
    clear_terminal()
    print("Inputs:")
    print(f"Left Joystick: ({leftStick[0]:.{3}f},{leftStick[1]:.{3}f})")
    print(f"Right Joystick: ({rightStick[0]:.{3}f},{rightStick[1]:.{3}f})")
    print(f"Right Trigger: {rightTrigger:.{3}f}")
    print(f"Left Trigger: {leftTrigger:.{3}f}")

    # outputs
    print("\nMotors:")
    print(f"Front: {frontMotor:.{3}f}")
    print(f"Back: {backMotor:.{3}f}")
    print(f"Left: {leftMotor:.{3}f}")
    print(f"Right: {rightMotor:.{3}f}")


def floatsToSpeeds(*args):
    speeds = ""

    for arg in args:
        arg *= 255

        # clamp -255 to 255
        arg = max(min(arg, 255), -255)

        # round and format to be 4 characters
        speeds += str(int(arg)).replace("-", "N").zfill(4)

    return speeds


def syncMotors():
    global frontMotor, backMotor, leftMotor, rightMotor
    global arduino
    message = floatsToSpeeds(frontMotor, backMotor, leftMotor, rightMotor)

    # print(message)
    arduino.sendMessage(message)


def translateInputs():
    global leftStick, rightStick, leftTrigger, rightTrigger
    global frontMotor, backMotor, leftMotor, rightMotor

    # reset motor speeds
    frontMotor = backMotor = leftMotor = rightMotor = 0

    # left stick x
    rightMotor -= leftStick[0]
    leftMotor += leftStick[0]

    # left stick y
    rightMotor += leftStick[1]
    leftMotor += leftStick[1]

    # right stick x

    # right stick y
    frontMotor -= rightStick[1]
    backMotor += rightStick[1]

    # left trigger
    frontMotor -= leftTrigger
    backMotor -= leftTrigger

    # right trigger
    frontMotor += rightTrigger
    backMotor += rightTrigger


# inputs -> outputs
"""
left stick X:  -right +left = rotate right

left stick Y:  +right +left = move forward

right stick X: none (roll in the future)

right stick Y: -front +back = rotate down

left trigger:   -front -back = go down

right trigger:  +front +back = go up
"""


# initialize controller
ps4Controller = controller()

# initialize arduino
arduino = device(arduinoPort)

printClock = time.time()
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                ps4Controller.setAxis(event.axis, event.value)
        if time.time() - printClock >= updateInterval:
            translateInputs()
            # debug()
            syncMotors()
            printClock = time.time()

except KeyboardInterrupt:
    pass

arduino.close()
ps4Controller.close()
pygame.quit()
