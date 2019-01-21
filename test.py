#librerias
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import codeReader as CR


#definiciones
file_name='scanqr.jpg'
##parametros de umbralizacion
th=(100,170,210) 
## mapeo de respuestas
resp=('A','B','C','D','E','F','G','H','K','L','m','n','')
##parametro de margen left,top,bottom


def get_contour(img,th):
    (LOW,MED,HIGH)=th
    res = cv.resize(img,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
    gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)        
    hsv = cv.cvtColor(res, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #print(img.shape,res.shape)
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
    #print(len(contours))
    ##### aqui ya estan las respuestas segmentadas, ahora debo trabajarlas una por una
    #resg6 = cv.resize(g6,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
    #cv.imshow('img_org',resg6) 
    return (contours,markers)

def get_response(ctr,mar,ret,resu,bs):
    (contours,markers)=ctr
    Mle=mar[0]
    Mup=mar[1]
    Mbo=mar[2]
    jk=0
    lst=[]
    
    for i in range(len(contours)):
        cnt=contours[i]
        M = cv.moments(cnt)
        area = cv.contourArea(cnt)
        if M['m00']!=0 and area>10:
            jk=jk+1
            cv.drawContours(markers, contours, i, (255,255,255), -1)        
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cal=(cx-Mle)/19.5
            pr=int(cal)
            rs=int((cy-Mup)/17.5) #primera fila altura 
#            print ('coor',(cx,cy),area,jk,pr,rs)
            if cy>=Mup and cy<=Mbo:
                lst.append([cx,cy,pr+bs,resp[rs]])
                resu[pr+bs]=resp[rsS]

            #if rs>0:
            #ret[pr]=resp[rs]
            #else:
             #   ret[pr]='-'
    # Draw the background marker
#    cv.circle(markers, (5,5), 3, (255,0,0), 1)
#    cv.imshow('Markers', markers*10000)
#    cv.waitKey(0)
#    cv.destroyAllWindows()
    #return ret   
    return lst




#definiciones
im = cv.imread(file_name)
#decodeQR
decodedObjects = CR.decode(im)
#removeQr
imr=CR.remove(im, decodedObjects)
#generar contornos
cont,mrk=get_contour(imr,th)
#contorno a respuest
ret=np.zeros(40).tolist()
red=np.zeros(40).tolist()
#260
#460
#660
#850
up=660
bt=up+(18*8)
#print(bt)
#res=get_response((cont,mrk),(90,up,bt),ret,red,103)
#print(respuestas,len(respuestas))
#print(np.asarray(res),len(res))

#califica(file_name,103)
def califica(file,preg):
    #calcula numero de filas
    rows=int((preg/34)+0.5)
    #carga image
    im = cv.imread(file_name)
    #decodeQR
    decodedObjects = CR.decode(im)
    #removeQr
    imr=CR.remove(im, decodedObjects)
    #generar contornos
    cont,mrk=get_contour(imr,th)
    #contorno a respuest

    ret=np.zeros(136).tolist()
    resu=np.zeros(136).tolist()
    first_line=260
    for i in range(0,rows):
        up=first_line
        bt=up+(18*8)
        print((90,up,bt))
        res=get_response((cont,mrk),(90,up,bt),ret,resu,(i*34)+1)
        #print(respuestas,len(respuestas))
        print(np.asarray(res),len(res))
        print(resu)
        first_line=bt+56
califica(file_name,136)    
