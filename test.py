#librerias
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

#definiciones
file_name='scan4.jpg'
##parametros de umbralizacion
th=(100,170,210) 
## mapeo de respuestas
resp=('A','B','C','D','E')
##parametro de altura de inicio *recalculable con pasadas
Mle=120
## parametros archivo/th/numero preguntas/Margen superio de la fila
def funct(file_name,th,num,Mup):
    ret=np.zeros(num).tolist()
    (LOW,MED,HIGH)=th
    print(file_name)
    img = cv.imread(file_name)
    res = cv.resize(img,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
    gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    
    #plt.imshow(gray,'gray')
    #plt.title('gray')
    #plt.xticks([]),plt.yticks([])
    #plt.show()
    
    hsv = cv.cvtColor(res, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    print(img.shape,res.shape)
    s1=(255-s)
    _,s2= cv.threshold(s1,MED,1,cv.THRESH_BINARY)
    g1=gray*s2
    _,g2= cv.threshold(g1,HIGH,1,cv.THRESH_BINARY)
    g3=255*(g2+(1-s2))
    g4 = cv.blur(g3,(5,5))
    _,g5= cv.threshold(g4,LOW,1,cv.THRESH_BINARY)
    g6=255*(1-g5)
    dist=g6
    dist_8u = dist.astype('uint8')

    # Find total markers
    _, contours, _ = cv.findContours(dist_8u, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Create the marker image for the watershed algorithm
    markers = np.zeros(dist.shape, dtype=np.int32)
    # Draw the foreground markers
    print(len(contours))
    ##### aqui ya estan las respuestas segmentadas, ahora debo trabajarlas una por una
    #cv.imshow('img_org',g6)
    jk=0

    for i in range(len(contours)):
        cnt=contours[i]
        M = cv.moments(cnt)
        area = cv.contourArea(cnt)
        if M['m00']!=0 and area>10:
            jk=jk+1
            cv.drawContours(markers, contours, i, (255,255,255), -1)        
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            pr=int((cx-Mle)/29)
            rs=int((cy-Mup)/27.5) #primera fila altura 
            print ('coor',(cx,cy),area,jk,pr,rs)
            #if rs>0:
            ret[pr]=resp[rs]
            #else:
             #   ret[pr]='-'
    # Draw the background marker
    #cv.circle(markers, (5,5), 3, (255,0,0), 1)
    #print('wwwwwwsz')
    #cv.imshow('Markers', markers*10000)
    #cv.waitKey(0)
    #cv.destroyAllWindows()
    return ret   

respuestas=funct(file_name,th,34,435)
print(respuestas)