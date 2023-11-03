import pygame
import time

leftStick = (0, 0)
rightStick = (0, 0)
leftTrigger = 0
rightTrigger = 0

pygame.init()

# get controller
pygame.joystick.init()
controller_count = pygame.joystick.get_count()

if controller_count == 0:
    print("No controllers found.")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()

print(f"Connected to controller: {controller.get_name()}")

printClock = time.time()
printInterval = 0.1

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
        if time.time() - printClock >= printInterval:
            printClock = time.time()
            print(
                f"\n\n\n\n\n\n\n\n\nLeft Joystick: ({leftStick[0]:.{3}f},{leftStick[1]:.{3}f})\nRight Joystick: ({rightStick[0]:.{3}f},{rightStick[1]:.{3}f})\nRight Trigger: {rightTrigger:.{3}f}\nLeft Trigger: {leftTrigger:.{3}f}"
            )
except KeyboardInterrupt:
    pass

controller.quit()
pygame.quit()
