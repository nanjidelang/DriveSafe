import serial
import urllib
import urllib2


ser = serial.Serial('/dev/ttyACM0', 115200)

n = 0
while n<3: #filter the first 3 data
    ser.readline()
    n+=1

while 1:

    values = {'Heartrate':ser.readline().split()[1], 'SpO2':ser.readline().split()[3]}
    data = urllib.urlencode(values)
    reg = urllib2.Request(url= 'http://127.0.0.1:5000/add', data = data)
    resp = urllib2.urlopen(reg)
    print resp.read()
