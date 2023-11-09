import pygame  # pip install pygame
import time
import serial  # pip install pyserial
import os

updateInterval = 0.05  # in seconds - how fast the arduino motors get synced

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
        self.topMotor = 0  # facing up: 1
        self.bottomMotor = 0  # facing up: 2
        self.leftMotor = 0  # facing forward: 3
        self.rightMotor = 0  # facing forward: 4

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
            self.topMotor, self.bottomMotor, self.leftMotor, self.rightMotor
        )
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
        if self.name == "Controller (dualSense)":  # use official name later (and test)
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
    print(f"Front: {floatToSpeed(arduino.topMotor)}")
    print(f"Back: {floatToSpeed(arduino.bottomMotor)}")
    print(f"Left: {floatToSpeed(arduino.leftMotor)}")
    print(f"Right: {floatToSpeed(arduino.rightMotor)}")


def floatToSpeed(arg):
    return f"{max(min(arg, 1), -1):.{3}f}"


def floatsToSpeeds(*args):
    speeds = ""

    for arg in args:
        arg *= 255

        # clamp -255 to 255
        arg = max(min(arg, 255), -255)

        # round and format to be 4 characters
        speeds += str(int(arg)).replace("-", "N").zfill(4)

    return speeds


def translateInputs(activeController, arduino):
    # reset motor speeds
    arduino.topMotor = arduino.bottomMotor = arduino.leftMotor = arduino.rightMotor = 0

    # left stick x
    arduino.rightMotor -= activeController.leftStick[0]
    arduino.leftMotor += activeController.leftStick[0]

    # left stick y
    arduino.rightMotor += activeController.leftStick[1]
    arduino.leftMotor += activeController.leftStick[1]
    arduino.topMotor += activeController.leftStick[1]
    arduino.bottomMotor += activeController.leftStick[1]

    # right stick x

    # right stick y
    arduino.topMotor += activeController.rightStick[1]
    arduino.bottomMotor -= activeController.rightStick[1]

    # left trigger
    arduino.topMotor -= activeController.leftTrigger
    arduino.bottomMotor -= activeController.leftTrigger

    # right trigger
    arduino.topMotor += activeController.rightTrigger
    arduino.bottomMotor += activeController.rightTrigger


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
