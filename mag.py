#!/usr/bin/env python

import pexpect
import sys
import time

def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t



def calcMagn(rawX,rawY,rawZ):
    vX= (rawX*1.0)/(65535/2000)
    vY= (rawY*1.0)/(65535/2000)
    vZ= (rawZ*1.0)/(65535/2000)
    print "Magn:X:%.2f uT;" %vX+"Y:%.2f uT;" %vX+"Z:%.2f uT;" %vX

bluetooth_adr = sys.argv[1]
tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
tool.expect('\[LE\]>')
print "Preparing to connect. You might need to press the side button..."
tool.sendline('connect')
# test for success of connect
tool.expect('\[CON\].*>')
tool.sendline('char-write-cmd 0x4A 01')
tool.expect('\[LE\]>')
while True:
    time.sleep(1)
    tool.sendline('char-read-hnd 0x46')
    tool.expect('descriptor: .*') 
    rval = tool.after.split()
    rawX = floatfromhex(rval[2] + rval[1])
    rawY = floatfromhex(rval[4] + rval[3])
    rawZ = floatfromhex(rval[6] + rval[5])
    #print rval
    calcMagn(rawX,rawY,rawZ)



