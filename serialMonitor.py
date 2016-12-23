#!/usr/bin/python
__author__ = 'EricB'

import serial.tools.list_ports
import time, sys
from threading import Thread, Lock


#global variable to tell the monitor that a serial comm port is present
arduinoPresent=False
idleTimer = 20

# THREADs tutorial @  https://www.tutorialspoint.com/python/python_multithreading.htm
class ComPortDetec(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print "Started ComPort monitoring for: "+str(self.name)
        global arduinoPresent
        while(1):
            detected = False
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                #print "\t" +str(p)
                if self.name in str(p):
                    detected=True
            arduinoPresent = detected

            #time.sleep(1)

class serialMonitor(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        global arduinoPresent
        global idleTimer
        portIsOpened = False
        lastMsg = time.time()+idleTimer
        print("starting Serial Monitor for : %s",self.name)
        ser1 = ""
        while(1):
            if portIsOpened:
                if arduinoPresent:
                    if ser1.in_waiting:
                        sys.stdout.write(ser1.read(ser1.in_waiting))
                        lastMsg = time.time()+idleTimer
                    if(time.time()>lastMsg):
                        print("\r\n------------ Monitor: Connected but IDLE for %d seconds ...   --------------",idleTimer)
                        lastMsg = time.time()+idleTimer
                else:
                    print("---------------------------------------------------------------------------")
                    print("------------ Monitor : Arduino Resetted or disconnected !!!!   Closing %s port",self.name)
                    print("---------------------------------------------------------------------------")
                    portIsOpened = False
                    ser1.close()
            else:
                if arduinoPresent:

                    print("---------------------------------------------------------------------------")
                    print("------------ Monitor : Arduino detected Opening port : %s",self.name)
                    print("---------------------------------------------------------------------------")
                    try:
                        ser1 = serial.Serial(self.name)
                        portIsOpened = True
                    except:
                        print "Ser comm not available"
                        time.sleep(1)

                else:
                    if(time.time()>lastMsg):
                        print "------------ Monitor : Arduino Not detected ..."
                        portIsOpened = False
                        lastMsg = time.time()+idleTimer


def main(argv):     # argv is the COMport to monitor
    threads = []
    #Create new threads
    thread1 = ComPortDetec(argv)
    thread2 = serialMonitor(argv)

    # start new threads
    thread1.start()
    time.sleep(1)       # let first thread detect the Arduino before letting the second one outputs stuff
    thread2.start()

    threads.append(thread1)
    threads.append(thread2)

    for t in threads:
        t.join()
    print "Failure of the 2 threads !"

if __name__ == '__main__':
    print sys.argv[1:]
    # TODO  parse the ARGs so to check for USB device descriptions as well as COMport

    main("COM61")
