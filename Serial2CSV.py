#! /usr/bin/env python


import serial
import sys
import csv
import time
import os
global iterations
def writeToCsv(datalist):
  
  global CSVData_success

  header = ["ID","Year","Month","Day","Hour","Minute","Seconds","Temperature","Pressure","Humidity","GPS"]

  fileName = "/home/pi/Desktop/logs/data_"+str(time.strftime("%m_%d_%y_")+ "log.csv")
  
  if os.path.exists(fileName):
    f = open(fileName, "a")

  else:
    f = open(fileName, "a+")
    for element in header:
      p = (element + ",")
      #p = p.strip().rstrip(',')
      #p = (','.join (header))
    #s = p.replace(',', '')
      f.write(p)
    
    f.write("\n")
    
  for element in datalist:
    if type(element)==str:
      #q = (','.join (datalist))
      #f.write(q)
      f.write(element + ",")
    if type(element) == list:
      for i in element:
         #r = (','.join (element))
         #f.write(r)
        f.write(i + ",")
  f.write("\n")
  f.close()
  CSVData_success = True

#data = []

ser = serial.Serial("/dev/ttyUSB0",115200,bytesize=8, parity=serial.PARITY_NONE, stopbits=1,timeout=1,xonxoff = False,dsrdtr = False,rtscts = False,writeTimeout = 2)
""" Exception Handling """
try: 
    ser.open()
except Exception, e:
    print "Seial Port Already Open" + str(e)
  #  exit()

if ser.isOpen():
    with open('fileName', 'w+') as f:
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output 
                 #and discard all that is in buffer

            time.sleep(0.5)  #give the serial port sometime to receive the data

            totalLines = 0
    #
    #with open('fileName', 'w+') as f:
            while True:
                response = ser.readline()
                print("Reading RUMS Sensor Data: " + response)
                line = response.rstrip().split(',')
                line = filter(None,line) # Filter out empty strings
                writeToCsv(line)
            totalLines = totalLines + 1

            if (totalLines >= 2):
            #break
                sys.exit()
  
            ser.close()
        except Exception, e1:
            print "Error communicating...: " + str(e1)

else:
    print "Can not open serial port "


ser.close()



