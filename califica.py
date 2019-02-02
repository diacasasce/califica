#librerias
import numpy as np
import cv2 as cv
from fs import checkFolder
import codeReader as CR
import datetime
import os


def filter(contours,area,ratio,solid,ima):
    result=[]
    for i in range(len(contours)):
        cnt=contours[i]
        Carea = cv.contourArea(cnt)
        x,y,w,h = cv.boundingRect(cnt)
        Cratio = float(w)/h
        hull = cv.convexHull(cnt)
        hull_area = cv.contourArea(hull)
        if hull_area>0:
            Csolid = float(Carea)/hull_area
        else:
            Csolid=0
        if Carea>area and Carea<20*area:
            if abs(Cratio-ratio)<(0.4*ratio):
                if(abs(Csolid-solid)<(0.5*solid)):                
                    result.append(cnt)   
    refs=(ima.copy()*0)
    cv.drawContours(refs, result, cv.FILLED, (255,255,255))
#    show('ima',refs)
    return (result,refs)

def get_contour(img,th):
    #show('ori',img)
    (LOW,MED,HIGH)=th
    res = cv.resize(img,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)    
    #show('ori r',res)
    res=img
    frame=img.copy()
    gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(res, cv.COLOR_BGR2HSV)
    black = np.array([0,0,0])
    vr=''
    prep=frame.copy()
    Ugray =np.array([255,255,200])
    mask = cv.inRange(hsv, black, Ugray)
    blur = cv.blur(mask,(5,5))
    kernel = np.ones((3,3),np.uint8)
    erosion = cv.erode(blur,kernel,iterations = 9)
    eroad= cv.add(erosion,erosion)
    eroadd = cv.erode(eroad,kernel,iterations = 2)
    eroad=cv.addWeighted(erosion,1,eroadd,0.3,0)
    dilation = cv.dilate(eroad,kernel,iterations = 3)
    erotion = cv.erode(dilation,kernel,iterations = 1)

    erotion= cv.add(erotion,erotion)
    blur = cv.bilateralFilter(erotion,25,200,200)
    blur= cv.add(blur,blur)
    blur= cv.add(blur,blur)
    blur= cv.add(blur,blur)
#    show('bmaskd',blur)
#    show('mask2',mask2)
    # Find total markers
    #_, contours, _ = cv.findContours(dist_8u, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    _, contours, _ = cv.findContours(erotion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Create the marker image for the watershed algorithm
    markers = np.zeros(erosion.shape, dtype=np.int32) 
    cntr,imf=filter(contours,50,1,1,res)
    # Draw the foreground markers
    #print(len(contours))
    ##### aqui ya estan las respuestas segmentadas, ahora debo trabajarlas una por una
    #resg6 = cv.resize(g6,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
    cv.drawContours(res, cntr, cv.FILLED, (0,0,250))
    return (cntr,markers,imf)

def get_id(ctr,mar,img):
    (contours,markers)=ctr
    U=mar[0]
    B=mar[1]
    L=mar[2]
    R=mar[3]
    
    jk=0
    lst=[]
    ret=['','','','','','','','','','','']
    for i in range(len(contours)):
        cnt=contours[i]
        M = cv.moments(cnt)
        area = cv.contourArea(cnt)
        if M['m00']!=0 :
            jk=jk+1
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if U<=cy <=B and L<=cx <=R:
                posY=round((abs(cy-U)/31)-0.5)
                posX=int(round((abs(cx-L)/34.2)-0.5))
                #print(cy,cy-U,posY,posX)
                #cv.circle(img,(cx,cy), 10, (0,0,255), -1)
                #show('ctr',img[117:427,140:530])
                if posX<len(ret):
                    ret[posX]=int(posY)
    ide=''
    for i in range(0,len(ret)):
        ide=ide+str(ret[i])
    #print(ide)
    return ide

def get_section(start,conEx,sz,spc):
    limits=[]
    st=start
    for i in range(len(conEx)):
        fn=st+(sz*conEx[i])
        limits.append((st,fn))
        st=fn+spc
    return limits

def check_Range(coor,ranges,conEx,mar,sz):
    (x,y)=coor
    for i in range(len(ranges)):
        limits=ranges[i]
        if(limits[0]<=y<=limits[1]):
            posY=round(abs(y-limits[0])/sz)
            #print(posY)
            return (i+1)
#    resu=get_resp(pre,secs,(cont,mrk),mar,resu,imr.copy())
def get_resp(pre,secs,sz,ctr,mar,resu,img):
    letras=['A','B','C','D','E','F','G','H','I']
    (contours,markers)=ctr
    L=mar[0]
    R=mar[1]
    D=mar[2]
    jk=0
    lst=[]
    result=np.zeros(50).tolist()
    for i in range(len(contours)):
        cnt=contours[i]
        M = cv.moments(cnt)
        area = cv.contourArea(cnt)
        if M['m00']!=0 and area>10:
            jk=jk+1
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            for i in range(len(secs)):
                limits=secs[i]
                if(limits[0]<=cy<=limits[1]):
                    posY=round((abs(cy-limits[0])/sz)-0.5)
                    posX=round((abs(cx-L)/D)-0.5)
                    if posX+(35*i)<len(resu) and int(posY)<len(letras) :
                        if resu[posX+(35*i)]=='0':
                            resu[posX+(35*i)]=letras[int(posY)]
                        else:
                            resu[posX+(35*i)]='X'

    #                cv.circle(img,(cx,cy), 10, (0,0,255), -1)
    #show('ctr',img)
    return resu

# show 
def show(title,image,last=True):
    img=cv.resize(image,None,fx=0.4, fy=0.4, interpolation = cv.INTER_CUBIC)
    cv.imshow(title,img) 
    if last:
        cv.waitKey(0)
        cv.destroyAllWindows()
# string de numeros a respuestas por fila
def Dsplit(str): 
    res=[]
    for i in range(0,len(str)):
        res.append(int(str[i]))
    return np.asarray(res)

#califica(file_name,103)
def Califica(file,th,baseDir):
    #carga image
    #print(file)
    im = cv.imread(file)
    save=cv.imread(file)
    #print(im.shape)
    #show('original',im)
    QR= im[0:800,0:1700]
#    show('QR',QR)
    #print(QR.shape)
    #decodeQR
    decodedObjects = CR.decode(QR)
    Idprueba,data,Max=str(decodedObjects[0].data).split('\'')[1].split(',')
    pre=Dsplit(data)
    #print(Idprueba)
    #print(pre)
    #print(Max)
    #CR.display(QR,decodedObjects)
    #removeQr
    imrQ=CR.remove(im, decodedObjects)
    ##remove logo
    imr= imrQ[300:4200,0:1700]
    
#    blur = cv.bilateralFilter(imr,(5,5))
#    blur = cv.blur(blur,(5,5))
#    blur = cv.blur(blur,(5,5))
 #   img12=cv.resize(imr,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
#    cv.imshow('noblur',img12) 
#    img22=cv.resize(blur,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
#    cv.imshow('blur',img22) 
#    cv.waitKey(0)
#    cv.destroyAllWindows()
    #print(imr.shape)
    #show('removed',imr)
    
    #generar contornos
    cont,mrk,imFilter=get_contour(imr,th)
    # obtiene documento de identidad  --- Id 
    #imfr= imr[117:427,140:530]
    #show('first',imfr)
    Id=get_id((cont,mrk),(117,427,140,530),imr.copy())
    #print(Id)
    #contorno a respuest
    resu=['0']*(int(Max))
    first_line=530
    mar=(140,1490,38.57)
    
    secs=get_section(first_line,pre,36,56)
    #resu=get_response((cont,mrk),(160,up,bt),resu,(35*i),imr.copy())
    resu=get_resp(pre,secs,36,(cont,mrk),mar,resu,imr.copy())
    resp=[]
    for i in range(0,len(resu)):
        resp.append(str(resu[i]))
    response=''.join(resp)
    folder=checkFolder(baseDir+Idprueba)
    nm=Id
    newName=folder+"/"+nm+".jpg"
#    ctName=folder+"/ct-"+nm+".jpg"
#    show('filtro',imFilter)
    cv.imwrite(newName,save)
    #cv.imwrite(ctName,imFilter)
    if os.path.isfile(newName):
        #print(file)
        os.remove(file)
    #print((Idprueba,Id,response))
    return (Idprueba,Id,response)

#ls=get_section(0,[4,4,8,4],30,20)

#print(ls)
#print(check_Range(130,ls,))```
