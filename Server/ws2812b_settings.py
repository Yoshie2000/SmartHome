#!/usr/bin/env python
#from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO

settings = "mode=3;rDH=3;gC=100;cPU=2;cHR=32;sBPM=20;sFS=10;bBPM=100;bHO=3;bPO=10;bCPI=1;jDC=10;jDHI=64;jFS=10;hUD=10;fps=120;b=80"
 
# RPi Alternate, with SPIDEV - Note: Edit RF24/arch/BBB/spi.cpp and  set 'this->device = "/dev/spidev0.0";;' or as listed in /dev
radio = RF24(22, 0)
 
payload_size = 16
millis = lambda: int(round(time.time() * 1000))
 
radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5,15)

pipes = [0xF0E1, 0xF0D2]

print("Sending to pipe: ", pipes[0])
print("Payload size: ", payload_size)

time.sleep(1)
 
radio.openWritingPipe(pipes[0]) # Address of the Arduino
radio.openReadingPipe(1,pipes[1]) # Address of the Raspberry
 
def sendCode(code):
    # The payload will always be the same, what will change is how much of it we send.
 
    # First, stop listening so we can talk.
    radio.stopListening()
 
    # Take the time, and send it.  This will block until complete
    radio.write(code[:payload_size])
 
    # Now, continue listening
    radio.startListening()
 
    # Wait here until we get a response, or timeout
    started_waiting_at = millis()
    timeout = False
    while (not radio.available()) and (not timeout):
        if (millis() - started_waiting_at) > 500:
            timeout = True
 
    # Describe the results
    if timeout:
        return False
    else:
        # Grab the response, compare, and send to debugging spew
        len = radio.getDynamicPayloadSize()
        receive_payload = radio.read(len)
        print(receive_payload)
        return True
 
 
if __name__ == "__main__":
         
    print("Sending all settings...")
        
    for code in settings.split(";"):
            
        while sendCode(code) == False:
            print("Failed: ", code)
            time.sleep(0.1)
                
        print("Sending successful!")
        # cooldown
        time.sleep(0.3)