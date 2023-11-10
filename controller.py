import pygame  # pip install pygame
import time
import serial  # pip install pyserial
import os

updateInterval = 0.05  # in seconds - how fast the arduino motors get synced
deadzone = 0.15  # the min joystick value for it to be percieved
minMotorPercent = 0.25  # the minimum speed percent for the motors to spin

# arduino ports
ports = [
    "/dev/ttyACM0",
    "COM4",
]


def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")


def findArduinoPort(baud):
    global ports
    for port in ports:
        try:
            testedPort = serial.Serial(port, baud)
            return testedPort
        except:
            pass
    return "none"


class motorController:
    def __init__(self, baud=9600):
        self.bottomLeftMotor = 0  # facing up: 1
        self.bottomRightMotor = 0  # facing up: 2
        self.topLeftMotor = 0  # facing forward: 3
        self.topRightMotor = 0  # facing forward: 4

        print("\nConnecting to arduino...")
        self.serial = findArduinoPort(baud)
        if self.serial != "none":
            print(f"Connected to arduino")
            time.sleep(1)
            self.debugMode = False
        else:
            print("!!!! Couldn't connect to arduino, running in debug mode !!!!")
            time.sleep(2)
            self.debugMode = True

    def sendMessage(self, message):
        if not self.debugMode:
            self.serial.write((message + "\n").encode())
        debug()

    def close(self):
        if not self.debugMode:
            self.serial.close()

    def syncMotors(self):
        message = floatsToSpeeds(
            self.bottomLeftMotor,
            self.topRightMotor,
            self.bottomRightMotor,
            self.topLeftMotor,
        )
        # bl, tr, br, tl
        self.sendMessage(message)


class controller:
    def __init__(self):
        self.leftStick = (0, 0)
        self.rightStick = (0, 0)
        self.leftTrigger = 0
        self.rightTrigger = 0

        print("\nConnecting to controller...")
        # initialize pygame
        pygame.init()
        pygame.joystick.init()
        controller_count = pygame.joystick.get_count()

        # if no controller active
        if controller_count == 0:
            print("!!!! No controllers found, defaulting to keyboard !!!!")
            print("\nControls:")
            print("Left joystick - WASD")
            print("Right joystick - IJKL")
            print("Left trigger - C")
            print("Right trigger - N")
            print("\nClick on the pygame window for keyboard to be registered")
            self.name = "keyboard"
            input("\npress enter when ready...")

            # create a screen so keyboard can be used
            pygame.init()
            screen = pygame.display.set_mode((400, 100))
            pygame.display.set_caption("Click here to use controls")
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
        if self.name == "keyboard":
            if event.type == pygame.KEYDOWN:
                self.setAxis(event.key, 1)
            elif event.type == pygame.KEYUP:
                self.setAxis(event.key, 0)
        else:
            if event.type == pygame.JOYAXISMOTION:
                self.setAxis(event.axis, event.value)

    def setAxis(self, axis, value):
        if self.name == "PS4 Controller":  # use official name later (and test)
            if axis == 0:  # left stick X
                self.leftStick = (value, self.leftStick[1])
            elif axis == 1:  # left stick Y
                self.leftStick = (self.leftStick[0], -value)
            elif axis == 4:  # left trigger
                self.leftTrigger = (value + 1) / 2
            elif axis == 2:  # right stick X
                self.rightStick = (value, self.rightStick[1])
            elif axis == 3:  # right stick Y
                self.rightStick = (self.rightStick[0], -value)
            elif axis == 5:  # right trigger
                self.rightTrigger = (value + 1) / 2
            return
        elif self.name == "Sony Computer Entertainment Wireless Controller":
            if axis == 0:  # left stick X
                self.leftStick = (value, self.leftStick[1])
            elif axis == 1:  # left stick Y
                self.leftStick = (self.leftStick[0], -value)
            elif axis == 2:  # left trigger
                self.leftTrigger = (value + 1) / 2
            elif axis == 3:  # right stick X
                self.rightStick = (value, self.rightStick[1])
            elif axis == 4:  # right stick Y
                self.rightStick = (self.rightStick[0], -value)
            elif axis == 5:  # right trigger
                self.rightTrigger = (value + 1) / 2
            return
        elif self.name == "Logitech Gamepad F310":
            if axis == 0:  # left stick X
                self.leftStick = (value, self.leftStick[1])
            elif axis == 1:  # left stick Y
                self.leftStick = (self.leftStick[0], -value)
            elif axis == 3:  # right stick X
                self.rightStick = (value, self.rightStick[1])
            elif axis == 4:  # right stick Y
                self.rightStick = (self.rightStick[0], -value)
            elif axis == 2:  # left trigger
                self.leftTrigger = (value + 1) / 2
            elif axis == 5:  # right trigger
                self.rightTrigger = (value + 1) / 2
            return
        elif self.name == "keyboard":
            # left stick
            if axis == pygame.K_w:
                self.leftStick = (self.leftStick[0], value)
            elif axis == pygame.K_a:
                self.leftStick = (-value, self.leftStick[1])
            elif axis == pygame.K_s:
                self.leftStick = (self.leftStick[0], -value)
            elif axis == pygame.K_d:
                self.leftStick = (value, self.leftStick[1])
            # right stick
            elif axis == pygame.K_i:
                self.rightStick = (self.rightStick[0], value)
            elif axis == pygame.K_j:
                self.rightStick = (-value, self.rightStick[1])
            elif axis == pygame.K_k:
                self.rightStick = (self.rightStick[0], -value)
            elif axis == pygame.K_l:
                self.rightStick = (value, self.rightStick[1])

            # triggers
            elif axis == pygame.K_n:
                self.rightTrigger = value
            elif axis == pygame.K_c:
                self.leftTrigger = value
            return

        print("!!!! NO CONTROLLER SCHEME MADE FOR " + self.name + " !!!!")
        time.sleep(0.5)
        return


def debug():
    global activeController
    global arduino

    # inputs
    clearTerminal()
    print("Inputs:")
    print(
        f"Left Joystick: ({activeController.leftStick[0]:.{3}f},{activeController.leftStick[1]:.{3}f})"
    )
    print(
        f"Right Joystick: ({activeController.rightStick[0]:.{3}f},{activeController.rightStick[1]:.{3}f})"
    )
    print(f"Right Trigger: {activeController.rightTrigger:.{3}f}")
    print(f"Left Trigger: {activeController.leftTrigger:.{3}f}")

    # outputs
    print("\nMotors:")
    print(f"Top Left: {floatToSpeed(arduino.topLeftMotor)}%")
    print(f"Top right: {floatToSpeed(arduino.topRightMotor)}%")
    print(f"Bottom left: {floatToSpeed(arduino.bottomLeftMotor)}%")
    print(f"Bottom right: {floatToSpeed(arduino.bottomRightMotor)}%")


def floatToSpeed(arg, percent=True):
    global deadzone, minMotorPercent

    if abs(arg) < deadzone:
        return f"0"

    # make it start at .25% since that is the min
    arg = (arg * (1 - minMotorPercent + deadzone)) + (
        minMotorPercent - deadzone
    ) * arg / abs(arg)

    # clamp between -1 and 1
    arg = max(min(arg, 1), -1)

    # make pretty
    if percent:
        return f"{int(arg*100)}"

    return arg * 255


def floatsToSpeeds(*args):
    speeds = ""

    for arg in args:
        arg = floatToSpeed(arg, False)

        # round and format to be 4 characters
        speeds += str(int(arg)).replace("-", "N").zfill(4)

    return speeds


def translateInputs(activeController, arduino):
    # reset motor speeds
    arduino.bottomLeftMotor = 0
    arduino.bottomRightMotor = 0
    arduino.topLeftMotor = 0
    arduino.topRightMotor = 0

    # left stick x - roll (none yet)

    # left stick y - none

    # right stick x - yaw
    arduino.topRightMotor -= activeController.rightStick[0]
    arduino.topLeftMotor += activeController.rightStick[0]
    arduino.bottomLeftMotor += activeController.rightStick[0]
    arduino.bottomRightMotor -= activeController.rightStick[0]

    # right stick y - pitch
    arduino.topRightMotor += activeController.rightStick[1]
    arduino.topLeftMotor += activeController.rightStick[1]
    arduino.bottomLeftMotor -= activeController.rightStick[1]
    arduino.bottomRightMotor -= activeController.rightStick[1]

    # left trigger - backwards
    arduino.topRightMotor -= activeController.leftTrigger
    arduino.topLeftMotor -= activeController.leftTrigger
    arduino.bottomLeftMotor -= activeController.leftTrigger
    arduino.bottomRightMotor -= activeController.leftTrigger

    # right trigger - forwards
    arduino.topRightMotor += activeController.rightTrigger
    arduino.topLeftMotor += activeController.rightTrigger
    arduino.bottomLeftMotor += activeController.rightTrigger
    arduino.bottomRightMotor += activeController.rightTrigger


# inputs -> outputs
"""
left stick X:  -right +left = rotate right

left stick Y:  +right +left = move forward

right stick X: none (roll in the future)

right stick Y: -front +back = rotate down

left trigger:   -front -back = go down

right trigger:  +front +back = go up
"""
# clear terminal
clearTerminal()

# initialize arduino
arduino = motorController()

# initialize controller
activeController = controller()

printClock = time.time()
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        activeController.possibleEvent(event)
    if time.time() - printClock >= updateInterval:
        translateInputs(activeController, arduino)
        arduino.syncMotors()
        printClock = time.time()

arduino.close()
activeController.close()
pygame.quit()
