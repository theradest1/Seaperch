import serial


class device:
    def __init__(self, port="COM4", baud=9600):
        self.serial = serial.Serial(port, baud)

    def sendMessage(self, message):
        self.serial.write(message.encode())

    def close(self):
        self.serial.close()


# motors 1 and 2 - yaw, forward/backward
# motors 3 and 4 - pitch, up/down
# motors 4 and 5 - roll (not currently here)

# left joystick - (yaw, forward/backward)
# right joystick - (roll, pitch)
# left triggers - up
# right triggers - down


# open new device
arduino = device()

try:
    while True:
        data_to_send = input("Enter speed (0-255): ")
        data_to_send += str(int(input("Enter motor (1-4): ")) - 1)
        arduino.sendMessage(data_to_send)
        # send data
except KeyboardInterrupt:
    print("Closed")
    arduino.close()
