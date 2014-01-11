import serial
import re
import urllib2
import time

ser = serial.Serial('COM9', 9600)
command = ''
timestamp = ''
ts = ''
tsRaw = 0
battery = ''
pressure = ''
humidity = ''
dewpoint = ''
tempH = ''
tempP = ''
tempR = ''
wind = ''
winddir = ''
rain = ''
wxid = ''
putRecord = 'http://www..../PutRecord.php'          # URL of scrit to add a record to the database
getTimestamp = 'http://www..../ts.php'   # URL of script to get Unix epoch
debug = ''
line = ''

def convertStamp(stamp):
    # convert dd-mon-yy hh:nn:ss to yyyy-mm-dd hh:nn:ss
    
    myStamp = stamp
    
    try:
        # convert month to number
        myStamp = re.sub('Jan', '01', myStamp)
        myStamp = re.sub('Feb', '02', myStamp)
        myStamp = re.sub('Mar', '03', myStamp)
        myStamp = re.sub('Apr', '04', myStamp)
        myStamp = re.sub('May', '05', myStamp)
        myStamp = re.sub('Jun', '06', myStamp)
        myStamp = re.sub('Jul', '07', myStamp)
        myStamp = re.sub('Aug', '08', myStamp)
        myStamp = re.sub('Sep', '09', myStamp)
        myStamp = re.sub('Oct', '00', myStamp)
        myStamp = re.sub('Nov', '11', myStamp)
        myStamp = re.sub('Dec', '12', myStamp)
            
        # parse
        dates = myStamp.split('-')
        dd = dates[0]
        mon = dates[1]
        yy = dates[2]
        yy = yy.split(' ')
        yy = yy[0]
        now = myStamp.split(' ')
        
        # return correctly formatted
        reply = yy + '-' + mon + '-' + dd + '\%20' + now[1]
    except:
        reply = ''
    finally:
        return reply

# main code loop

# announce self
print "wxXRF.py"
line = ''

while True:
    try:
        # read a line from serial port
        try:
            #line = ''
            #for char in ser.read():
            #    print char,
            #    if char == '\n':
            #        break
            #    line.append(char)
            #print char,
            #line = line + char
            line = ser.readline()
            line = re.sub("\n", "", line)
            # echo the line
            print str(round(time.time() + (442344937-1389029745), 1)) + '>' + line
        except:
            line = ''
        
        # see if this line has wxid:
        i = line.lower().find('wxid:')
        if i >= 0:
            # it does
            i = line.find(':')
            wxid = line[i+2:]
            i = wxid.find('\r');
            if i>0:
                wxid = wxid[:i]
            wxid = '?wxid=' + wxid

        # see if this line has start time:
        i = line.lower().find('start time:')
        if i >= 0:
            # it does
            i = line.find('01-Jan-2000')
            if i >= 0:
                # bad timestamp, so get new from server
                reply = urllib2.urlopen(getTimestamp).read()
                ser.write('h ' + str(reply) + '\n')

        # see if this line has ts:
        i = line.lower().find('ts:')
        if i >= 0:
            # it does
            i = line.find(':')
            ts = line[i+2:]
            i = ts.find('\r');
            if i > 0:
                ts = ts[:i]
            try:
                tsRaw = int(ts)
            except:
                tsRaw = 0
            ts = '&ts=' + ts

        # see if this line has timestamp:
        i = line.lower().find('timestamp:')
        if i >= 0:
            # it does
            i = line.find(':')
            timestamp = line[i+2:]
            i = timestamp.find(' \r');
            if i > 0:
                timestamp = timestamp[:i]
            timestamp = convertStamp(timestamp)
            timestamp = '&timestamp=' + timestamp

        # see if this line has battery:
        i = line.lower().find('battery:')
        if i >= 0:
            # it does
            i = line.find(':')
            battery = line[i+2:]
            i = battery.find(' ');
            if i > 0:
                battery = battery[:i]
            battery = '&battery=' + re.sub("\.", "", battery)

        # see if this line has wind speed:
        i = line.lower().find('wind speed:')
        if i >= 0:
            # it does
            i = line.find(':')
            wind = line[i+2:]
            i = wind.find(' ');
            if i > 0:
                wind = wind[:i]
            wind = '&wind=' + re.sub("\.", "", wind)

        # see if this line has wind dir:
        i = line.lower().find('wind dir:')
        if i >= 0:
            # it does
            i = line.find(':')
            winddir = line[i+2:]
            i = winddir.find(' ');
            if i > 0:
                winddir = winddir[:i]
            winddir = '&winddir=' + re.sub("\.", "", winddir)

        # see if this line has rain rate:
        i = line.lower().find('rain rate:')
        if i >= 0:
            # it does
            i = line.find(':')
            rain = line[i+2:]
            i = rain.find(' ');
            if i > 0:
                rain = rain[:i]
            rain = '&rain=' + re.sub("\.", "", rain)

        # see if this line has tempP:
        i = line.lower().find('tempp:')
        if i >= 0:
            # it does
            i = line.find(':')
            tempP = line[i+2:]
            i = tempP.find(' ');
            if i > 0:
                tempP = tempP[:i]
            tempP = '&tempP=' + re.sub("\.", "", tempP)

        # see if this line has tempH:
        i = line.lower().find('temph:')
        if i >= 0:
            # it does
            i = line.find(':')
            tempH = line[i+2:]
            i = tempH.find(' ');
            if i > 0:
                tempH = tempH[:i]
            tempH = '&tempH=' + re.sub("\.", "", tempH)

        # see if this line has RTC temp:
        i = line.lower().find('rtc temp:')
        if i >= 0:
            # it does
            i = line.find(':')
            tempR = line[i+2:]
            i = tempR.find(' ');
            if i > 0:
                tempR = tempR[:i]
            tempR = '&tempR=' + re.sub("\.", "", tempR)

        # see if this line has humidity:
        i = line.lower().find('humidity:')
        if i >= 0:
            # it does
            i = line.find(':')
            humidity = line[i+2:]
            i = humidity.find(' ');
            if i > 0:
                humidity = humidity[:i]
            humidity = '&humidity=' + re.sub("\.", "", humidity)

        # see if this line has dew point:
        i = line.lower().find('dew point:')
        if i >= 0:
            # it does
            i = line.find(':')
            dewpoint = line[i+2:]
            i = dewpoint.find(' ');
            if i > 0:
                dewpoint = dewpoint[:i]
            dewpoint = '&dewpoint=' + re.sub("\.", "", dewpoint)

        # see if this line has pressure:
        i = line.lower().find('pressure:')
        if i >= 0:
            # it does
            i = line.find(':')
            pressure = '&pressure=' + line[i+2:]
            i = pressure.find(' ');
            if i > 0:
                pressure = pressure[:i]

        # check for end of data group
        i = line.lower().find('next time')
        if i >= 0:
            command = putRecord + wxid + timestamp + ts + battery + pressure + tempP + tempH + \
            tempR + humidity + wind + winddir + rain + dewpoint + debug
            # print command
            
            if tsRaw >= 50000:
                try:
                    # send command to server and get reply
                    reply = urllib2.urlopen(command).read()
                    
                    # only print reply if not ok
                    i = reply.lower().find('ok')
                    if i < 0:
                        print reply
                except:
                    print "database update failed"
            else:
                print 'bad timestamp'
    except:
        continue