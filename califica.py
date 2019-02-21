#librerias
import numpy as np
import cv2 as cv
from fs import checkFolder
import codeReader as CR
import datetime
import os
from matplotlib import pyplot as plt

def fillHoles(im_th):
    im_floodfill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv
    return im_out

def filter(contours,areas,ratio,solid,ima):
    result=[]
    coor=[]
    area,Uarea=areas
    refsa=(ima.copy()*0)
#    refss=(ima.copy()*0)

    for cnt in contours:
        Carea = cv.contourArea(cnt)
        M = cv.moments(cnt)
        x,y,w,h = cv.boundingRect(cnt)        
        Cratio = float(w)/h
        hull = cv.convexHull(cnt)
        hull_area = cv.contourArea(hull)
        cx=0
        cy=0
        if M['m00']!=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cbx=x+(w/2)
            cby=y+(h/2)  
            mx=int((cx+cbx)/2)
            my=int((cy+cby)/2)
#        cv.circle(refss,(mx,my), 20, (0,0,255), -1)
                    
        if hull_area>0:
            Csolid = float(Carea)/hull_area
        else:
            Csolid=0
        if Carea>area and Carea<Uarea:
            if abs(Cratio-ratio)<(0.7*ratio):
                if(abs(Csolid-solid)<(0.7*solid)):     
                    result.append(cnt)
                    cv.circle(refsa,(mx,my), 20, (0,0,255), -1)
                    coor.append((mx,my))

    #cv.drawContours(refs, result, cv.FILLED, (255,255,255))
    #show('rf',refsa[1000:2000,400:4500],0.15)
    #show('ima1',refss,last=False)
    return (result,refsa,coor)
def get_contour(img,th):
    #show('ori',img)
    # quita numeros y parte manuscrita
    img[0:500,550:1700]=255+(img[0:500,550:1700]*0)
    img[0:130,0:550]=255+(img[0:130,0:550]*0)
    #show('init2',img)
    (LOW,MED,HIGH)=th
    res = cv.resize(img,None,fx=3, fy=3, interpolation = cv.INTER_CUBIC)
    #show('ori r',res)
    #res=img
    frame=img.copy()
    gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(res, cv.COLOR_BGR2HSV)
    h,s,v=cv.split(hsv)
    black = np.array([0,0,0])
    vr=''
    prep=frame.copy()
    kernel = np.ones((3,3),np.uint8)
    kernel3 = np.ones((7,7),np.uint8)
    kernel5 = np.ones((11,11),np.uint8)
    Ugray =np.array([255,255,220])
    mask = cv.inRange(hsv, black, Ugray)
    qwe=np.asarray((s>50),np.uint8)        
    quee=255*qwe
    mask=mask-quee
    #show('init',mask,0.15,last=False)
    
    openn = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    #show('st013',openn,0.15,last=False)
    closing = cv.morphologyEx(openn, cv.MORPH_CLOSE, kernel3)
    #show('st023',closing,0.15,last=False)
    erosion = cv.erode(closing,kernel,iterations = 3)
    #show('st13',erosion,0.15,last=False)
    dilation = cv.dilate(erosion,kernel3,iterations = 2)
    dilation = cv.dilate(dilation,kernel,iterations = 1)
    #show('st23',dilation,0.15,last=False)
    closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, kernel5)
    closing = cv.morphologyEx(closing, cv.MORPH_CLOSE, kernel5)
    #show('st33',closing,last=False)

    erosion = cv.erode(closing,cv.getStructuringElement(cv.MORPH_CROSS,(3,3)),iterations = 6)
    #show('st44',erosion,0.15,last=False)
    closing = cv.morphologyEx(erosion, cv.MORPH_CLOSE,np.ones((25,25),np.uint8))
    #show('st33',closing,0.15,last=False)
    prep=closing
    #show('test',prep)
    #plt.figure(1)
    #plt.imshow(prep)
    #plt.show()
    
    # fin
    #_, contours, _ = cv.findContours(dist_8u, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    _, contours, _ = cv.findContours(prep, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Create the marker image for the watershed algorithm
    markers = np.zeros(prep.shape, dtype=np.int32) 
    cntr,imf,coor=filter(contours,(1500,9000),1,1,res)
    #show('st12',imf,0.15)
    # Draw the foreground markers
    #print(len(contours))
    ##### aqui ya estan las respuestas segmentadas, ahora debo trabajarlas una por una
    #resg6 = cv.resize(g6,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
    return (cntr,markers,imf,coor)

def get_id_c(mar,coor,Rx,Ry):
    U=mar[0]
    B=mar[1]
    L=mar[2]
    R=mar[3]
    jk=0
    lst=[]
    ret=['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
    Carr=np.asarray(coor)
    for co in coor:
        cx,cy=co
        if U<=cy <=B and L<=cx <=R:
            #print((cx,cy))
            posY=round(((cy-U)/Ry)-0.5)
            posX=int(round(((cx-L)/Rx)-0.5))
            if(posY<0):
                posY=0
            if(posX<0):
                posX=0
                
            #print((posX,posY))
            if posX<=len(ret):
                ret[posX]=int(posY)
    ide=''
    for i in range(0,len(ret)):
        ide=ide+str(ret[i])
    
    #print(ide)
    #print(ret)
    return ide
    
def get_id(ctr,mar,img):
    (contours,markers)=ctr
    U,B,L,R=mar
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
                posY=round((abs(cy-U)/3)-0.5)
                posX=int(round((abs(cx-L)/34.2)-0.5))
                #print(cy,cy-U,posY,posX)
                #cv.circle(img,(cx,cy), 10, (0,0,255), -1)
                #show('ctr',img[117:427,140:530])
                if posX<=len(ret):
                    ret[posX-1]=int(posY)
                else:
                    print(posX)
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


def get_resp_c(mar,coor,pre,secs,sz,resu):
    letras=['A','B','C','D','E','F','G','H','I']
    L,R,D=mar
    jk=0
    lst=[]
    result=np.zeros(50).tolist()
    for co in coor:
        cx,cy=co
        for i in range(len(secs)):
            limits=secs[i]
            up,lo=limits
            if(up<=cy<=lo):
                posY=round((abs(cy-up)/sz)-0.5)
                posX=round((abs(cx-L)/D)-0.5)
                if posX+(35*i)<len(resu) and int(posY)<len(letras) :
                    if resu[posX+(35*i)]=='0':
                        resu[posX+(35*i)]=letras[int(posY)]
                    else:
                        resu[posX+(35*i)]='X'
    #print(resu)                        
    return resu

def get_resp(pre,secs,sz,ctr,mar,resu,img):
    letras=['A','B','C','D','E','F','G','H','I']
    (contours,markers)=ctr
    L=mar[0]#left
    R=mar[1]#right
    D=mar[2]#Distance
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

# detector
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

# show 
def show(title,image,fac=0.2,last=True):
    img=cv.resize(image,None,fx=fac, fy=fac, interpolation = cv.INTER_CUBIC)
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
    #print(datetime.datetime.now())
    OldName=file
    newName=file
    Idprueba,Id,response=(False,False,False)

    #carga image
    #print(file)
    im = cv.imread(file)
    save=cv.imread(file)
    #print(im.shape)
    #show('original',im)
    QR= im[0:800,0:1700]
    #show('QR',QR)
    #print(QR.shape)
    #decodeQR
    fact=3
    decodedObjects=qr_det(QR,fact)
    ##posibilidad para agregar el punto de referencia
    if decodedObjects:
        Idprueba,data,Max=str(decodedObjects[0].data).split('\'')[1].split(',')
        pre=Dsplit(data)
        #print(Idprueba)
        #print(pre)
        #print(Max)
        #CR.display(QR,decodedObjects)
        #removeQr
        imrQ=CR.remove(im, decodedObjects,fact)
        ##remove logo
        imr= imrQ[300:4200,0:1700]
        #518
        #474    
        #print(decodedObjects[0].rect)
        anX=decodedObjects[0].rect.left
        anY=decodedObjects[0].rect.top-900
        #generar contornos
        cont,mrk,imFilter,coor =get_contour(imr,th)
        imra=imFilter.copy()
        cv.circle(imra,(anX,anY), 100, (0,0,255), -1)
        
        #print(anX,anY)
        #show('test',imra)
        U=anY-530
        B=1500
        #print(B)
        L=anX-3300
        R=anX-2000
        #print(R)
        #inserta las lineas
        #for i in range(0,11):
            #sp=90*i
            #cv.line(imFilter,(0,U+sp),(2000,U+sp),(255,0,0),5)
            #cv.line(imFilter,(L+(40*i),U),(L+(40*i),B),(255,0,0),5)
        #show('fili1',imFilter[U:B,L:R],0.5)
        # obtiene documento de identidad  --- Id 
        #(120,427,140,530)
        #Rx=input('rx?' )
        Ry=90
        Rx=40
        Id=get_id_c((U,B,L,R),coor,int(Rx),int(Ry))
        #input(Id)
        #contorno a respuest
        resu=['0']*(int(Max))
        first_line=anY+670
        mar=(L-10,L+4000,112)        
        he=100
        secs=get_section(first_line,pre,he,180)
        qwe=0
        #print(secs)
        for lim in secs:
            #print(lim)
            U,B=lim
            L,R,Q=mar
            #for i in range(0,5):
            #    sp=100*i
            #    cv.line(imFilter,(L,U+sp),(R,U+sp),(0,255,255),5)
            #for i in range(0,35):
            #    sp=Q*i
            #    cv.line(imFilter,(L+sp,U),(L+sp,B),(0,255,255),5)
            #show('fili'+str(qwe),imFilter[U:B,L:R],0.3,False)
            #qwe+=1
        #print(secs)
        
        resu=get_resp_c(mar,coor,pre,secs,he,resu)
        #resu=get_resp(pre,secs,36,(cont,mrk),mar,resu,imr.copy())
        resp=[]
        for i in range(0,len(resu)):
            resp.append(str(resu[i]))
        response=''.join(resp)
        folder=checkFolder(baseDir+Idprueba)
        nm=str(Id)
        #print(datetime.datetime.now())
        #input('ALMOST')
        newName=folder+"/"+nm+".jpg"
        k=1
        while os.path.isfile(newName)==True:
            newName=folder+"/"+nm+'-'+str(k)+".jpg"
            k+=1
#        print((Idprueba,Id,response))
#        show('fili',imFilter,0.15)
#        input('ready??')
        cv.imwrite(newName,save)
    #    ctName=folder+"/ct-"+nm+".jpg"
    #    show('filtro',imFilter)
    #    print(OldName)
    #    print(newName)
    else:
        head,tail=os.path.split(OldName)
        folder=checkFolder(baseDir+'sinQR')
        newName=folder+"/"+tail
        cv.imwrite(newName,save)
        #cv.imwrite(ctName,imFilter)
    
    if os.path.isfile(newName):
        #print(file)
        os.remove(file)
    
    return (Idprueba,Id,response)

#ls=get_section(0,[4,4,8,4],30,20)

#print(ls)
#print(check_Range(130,ls,))```
