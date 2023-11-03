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
            self.serial.write(message.encode())

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


def syncMotors():
    global frontMotor, backMotor, leftMotor, rightMotor
    global arduino

    arduino.sendMessage(f"{frontMotor}{backMotor}{leftMotor}{rightMotor}")


def translateInputs():
    global leftStick, rightStick, leftTrigger, rightTrigger
    global frontMotor, backMotor, leftMotor, rightMotor

    # reset motor speeds
    frontMotor = backMotor = leftMotor = rightMotor = 0


# inputs -> outputs
"""
left stick positive X:  -right +left
left stick negative X:  +right -left

left stick positive Y:  +right +left
left stick negative Y:  -right -left

right stick positive X: none (roll in the future)
right stick negative X: none (roll in the future)

right stick positive Y: +front -back
right stick negative Y: -front +back

left trigger:   +front +back

right trigger:  -front -back
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
            debug()
            printClock = time.time()

except KeyboardInterrupt:
    pass

arduino.close()
ps4Controller.close()
pygame.quit()
