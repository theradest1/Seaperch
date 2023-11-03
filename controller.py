import serial


class device:
    def __init__(self, port="COM4", baud=9600):
        self.serial = serial.Serial(port, baud)

    def sendMessage(self, message):
        self.serial.write(message.encode())

    def close(self):
        self.serial.close()


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
