import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

while 1 :
	i = chr(int(raw_input('increment pos?: ')))
	ser.write(i)
    #print(ser.readline())