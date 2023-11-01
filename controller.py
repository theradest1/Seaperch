import serial

# Define the serial port and baud rate
arduino = serial.Serial('COM4', 9600)  # Change 'COM4' to your Arduino's serial port

try:
    while True:
        data_to_send = input("Enter data to send to Arduino: ")
        arduino.write(data_to_send.encode())  # send data
except KeyboardInterrupt:
    arduino.write("0".encode())  # turn off motors
    print("Program terminated.")
    arduino.close()