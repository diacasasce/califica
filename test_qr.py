import numpy as np
import cv2 as cv
import fs 
import codeReader as CR
import datetime
import os
import califica as cl
#test_qur
def prt(val):
    if val:
        print(scale(val[0].polygon,3))
        print(val[0].polygon)
        input()
    else:
        print('---------------')
def scale(data,fact=1):
    resp=[]
    for point in data:
        x,y=(point.x,point.y)
        x=int(x/fact)
        y=int(y/fact)
        resp.append((x,y))
    return(resp)
def qr_det(qr,fact=1):
    hsv = cv.cvtColor(qr, cv.COLOR_BGR2HSV)
    black = np.array([-1,0,0])
    vr=''
    Ugray =np.array([255,255,200])
    res = cv.resize(hsv,None,fx=fact , fy=fact, interpolation = cv.INTER_CUBIC)
    mask = cv.inRange(res, black, Ugray)
    kernel = np.ones((6,6),np.uint8)
    openn = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    openn = cv.morphologyEx(openn, cv.MORPH_OPEN, kernel)
    openn = 255-cv.morphologyEx(openn, cv.MORPH_OPEN, kernel)
    #cl.show('mask',openn)
    decode=CR.decode(openn)
    if decode:
        return decode    #cl.show('mask',openn)
    else:
        return False

def test(file):
    print(file)
    im = cv.imread(file)
    save=cv.imread(file)
    #cl.show('test',im)
    QR= im[0:800,0:1700]
    #cl.show('testQ',QR)
    fact=3
    detected=qr_det(QR,fact)
    if detected:
        CR.display(im,detected,fact)
        cl.show('test',CR.remove(im,detected,fact))
    


folder='./origen/procesados/sinQR/'
files=fs.listFolder('./origen/procesados/sinQR/','.jpg')
for file in files:
    test(folder+file)