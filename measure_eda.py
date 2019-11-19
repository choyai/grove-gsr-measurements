import serial
import numpy as np
import time

BAUDRATE = int(input("input baud rate: "))
PORT = 'COM' + str(input("input COM Port: COM"))
max_data = 2000


def count2angle(count):
    """
    :param count:  pulsecount from encoder
    :return: motor armature angle
    """
    angle = count * np.pi * 2 / 768
    return angle


ser = serial.Serial()
ser.baudrate = BAUDRATE
ser.port = PORT
ser.timeout = 1
ser.dtr = 0
ser.rts = 0
while True:
    try:
        ser.open()
        print("connected to: " + ser.portstr)
        start = time.time()
        break
    except:
        print("No permission to access " + PORT)


counter = 1
data = ""
while True:
    try:
        line = ser.readline().decode('utf-8')
        print(line)
    # parse data and do conversions
        if len(line) > 0:
            adc_data = int(line)

            # create new string entry with all the values separated by commas
            new = "{0:.5f}".format(time.time() - start) + \
                ",{0:.5f},".format(adc_data)
            # Save to CSV file and exit after 20s or 2000 entries
            if counter >= max_data:
                f = open("log_file_super_hot_2.csv", "a")
                f.write(data)
                f.close()
                data = ''
                print("File saved")
                counter = 0
            data += (str(new) + "\n")
            counter += 1
        else:
            pass
    except KeyboardInterrupt:
        f = open("log_file_super_hot_2.csv", "a")
        f.write(data)
        f.close()
        data = ''
        print("File saved")
        end = time.time()
        print(end - start)
        ser.close()
    except:
        print("whoops, parsing error")

ser.close()
