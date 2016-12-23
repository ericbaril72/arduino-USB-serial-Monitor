# arduino-USB-serial-Monitor
A SerialMonitor for USB-cdc that automaticly closes/re-open the selected serial-port on CPU reset or USB disconnect

This Python application runs a Serial Monitor with automatic open-close of the serial-port.

Putty WAS my best friend for Arduino/Teensy application debugging over the USBserialport.
HOWEVER, some of my latest application did require substancial reprogramming or RESET.
Putty would leave the Serial window "opened" and on Windows discovery of the USB-connect, 
the new data stream would not automaticly resume. Windows could not associate it with the COMport as it was busy ( still opened )

I would then neeed to close the Putty windows and RESET again so that the windows USB-connect 
would be able to associate again with the freed COM-port.

I could not easily find a serial monitor that did just that and thought it would be a good learning experience on USB/serial knowledge.

Has been used with an ArduinoZero but can work with ANY USB-serial communication devices.

## How it works
it could have been done differently BUT i wanted to try out Threads.

1 thread checks for the COMport presence and reports on the global variable -->arduino detected
1 thread is the serial monitor.
 
## Installation

- Python 2.7
- PySerial

from the command line
> python serialMonitor.py

## TODO

- finalize [args] so to call a specific com port    ( ex: python serialMonitor.py -p COM61 )
- add [args] so to call the right port based on the description ( ex:   -d ArduinoZero )

## Wishlist

would be nice to also start based on USBdevice serial number when dealing with multiple identical devices connected on the same PC
