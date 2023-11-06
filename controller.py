import pygame  # pip install pygame
import time
import serial  # pip install pyserial
import os

pygame.init()
screen = pygame.display.set_mode((400, 100))
pygame.display.set_caption("Click here for keyboard controls")

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
            debug()

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
            print("No controllers found - defaulting to keyboard")
            self.name = "keyboard"
            time.sleep(1)
            return

        # initialize controller
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.name = str(self.controller.get_name())
        print(f"Connected to controller: {self.name}")
        time.sleep(1)

    def close(self):
        self.controller.quit()

    def possibleEvent(self, event):
        if event.type == pygame.JOYAXISMOTION:
            self.setAxis(event.axis, event.value)
        elif event.type == pygame.KEYDOWN and self.name == "keyboard":
            self.setAxis(event.key, 1)
        elif event.type == pygame.KEYUP and self.name == "keyboard":
            self.setAxis(event.key, 0)

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
        elif self.name == "keyboard":
            # left stick
            if axis == pygame.K_w:
                leftStick = (leftStick[0], value)
            elif axis == pygame.K_a:
                leftStick = (-value, leftStick[1])
            elif axis == pygame.K_s:
                leftStick = (leftStick[0], -value)
            elif axis == pygame.K_d:
                leftStick = (value, leftStick[1])
            # right stick
            elif axis == pygame.K_i:
                rightStick = (rightStick[0], value)
            elif axis == pygame.K_j:
                rightStick = (-value, rightStick[1])
            elif axis == pygame.K_k:
                rightStick = (rightStick[0], -value)
            elif axis == pygame.K_l:
                rightStick = (value, rightStick[1])

            # triggers
            elif axis == pygame.K_n:
                rightTrigger = value
            elif axis == pygame.K_c:
                leftTrigger = value
            return

        print("NO CONTROLLER SCHEME MADE FOR " + self.name)
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
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        ps4Controller.possibleEvent(event)
    if time.time() - printClock >= updateInterval:
        translateInputs()
        syncMotors()
        printClock = time.time()

arduino.close()
ps4Controller.close()
pygame.quit()
