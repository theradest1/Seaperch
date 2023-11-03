import pygame
import time
import serial

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


class device:
    def __init__(self, port="COM4", baud=9600):
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
            print("\n\n\n\n\n\n\n\n")
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
        print(f"Connected to controller: {self.controller.get_name()}")
        time.sleep(1)

    def close(self):
        self.controller.quit()


def debug():
    global leftStick, rightStick, leftTrigger, rightTrigger
    global frontMotor, backMotor, leftMotor, rightMotor
    # inputs
    print("\n\n\n\n\n\n\n\n\nInputs:")
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
arduino = device()

printClock = time.time()
updateInterval = 0.1  # in seconds
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:  # left stick X
                    leftStick = (event.value, leftStick[1])
                elif event.axis == 1:  # left stick Y
                    leftStick = (leftStick[0], -event.value)
                elif event.axis == 2:  # left trigger
                    leftTrigger = (event.value + 1) / 2
                elif event.axis == 3:  # right stick X
                    rightStick = (event.value, rightStick[1])
                elif event.axis == 4:  # right stick Y
                    rightStick = (rightStick[0], -event.value)
                elif event.axis == 5:  # right trigger
                    rightTrigger = (event.value + 1) / 2
        if time.time() - printClock >= updateInterval:
            translateInputs()
            syncMotors()
            # debug()
            printClock = time.time()

except KeyboardInterrupt:
    pass

arduino.close()
ps4Controller.close()
pygame.quit()
