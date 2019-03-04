#librerias
import numpy as np
import cv2 as cv
from fs import checkFolder
import codeReader as CR
import datetime
import os
#from matplotlib import pyplot as plt

def fillHoles(im_th):
    im_floodfill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv.floodFill(im_floodfill, mask, (0,0), 255);
    im_floodfill_inv = cv.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv
    return im_out

def filter(contours,areas,ratio,solid,ima):
    result=[]
    coor=[]
    area,Uarea=areas
    refsa=(ima.copy()*0)
    refss=(ima.copy()*0)

    for cnt in contours:
        Carea = cv.contourArea(cnt)
        M = cv.moments(cnt)
        x,y,w,h = cv.boundingRect(cnt)        
        Cratio = float(w)/h
        hull = cv.convexHull(cnt)
        hull_area = cv.contourArea(hull)
        cx=0
        cy=0
        mx=0
        my=0
        if M['m00']!=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cbx=x+(w/2)
            cby=y+(h/2)  
            mx=int((cx+cbx)/2)
            my=int((cy+cby)/2)
            cv.circle(refss,(mx,my), 20, (0,0,255), -1)
                    
        if hull_area>0:
            Csolid = float(Carea)/hull_area
        else:
            Csolid=0
        if area <= Carea <= Uarea:
            #if abs(Cratio-ratio)<(0.7*ratio):
            if(abs(Csolid-solid)<(0.7*solid)):     
                result.append(cnt)
                cv.circle(refsa,(mx,my), 20, (0,0,255), -1)
                coor.append((mx,my))
            else:
                print(Csolid,abs(Csolid-solid),(0.7*solid))
                cv.circle(refsa,(mx,my), 20, (0,255,255), -1)    
            #else:
            #    print(Cratio,abs(Cratio-ratio),(0.7*ratio))
            #    cv.circle(refsa,(mx,my), 30, (255,0,255), -1)
        elif Carea>Uarea:
            cv.circle(refsa,(mx,my), 20, (0,255,0), -1)
        elif (0.8*area)<=Carea<area:
            cv.circle(refsa,(mx,my), 20, (255,255,0), -1)
            print(Carea)
        elif Carea<(0.8*area):
            cv.circle(refsa,(mx,my), 20, (255,0,255), -1)
                    
    #cv.drawContours(refs, result, cv.FILLED, (255,255,255))
    #show('rf',refsa[1000:2000,400:4500],0.15)
    #show('ima1',ima,last=False)
    #show('ima2',refsa)
    return (result,refsa,coor)
def shakeLR(im,sh,times=1):
    mask=im
    for i in range(times):
        shape=mask.shape
        otherL=mask.copy()
        otherR=mask.copy()
        otherL[0:shape[0]-sh,0:shape[1]-sh]=mask[sh:shape[0],sh:shape[1]]
        otherR[sh:shape[0],sh:shape[1]]=mask[0:shape[0]-sh,0:shape[1]-sh]
        mask=cv.add(otherL,otherR)
    return mask
def shakeRL(im,sh,times=1):
    mask=im
    for i in range(times):
        shape=mask.shape
        otherL=mask.copy()
        otherR=mask.copy()
        otherL[sh:shape[0],0:shape[1]-sh]=mask[0:shape[0]-sh,sh:shape[1]]
        otherR[0:shape[0]-sh,sh:shape[1]]=mask[sh:shape[0],0:shape[1]-sh]
        mask=cv.add(otherL,otherR)
    return mask
def get_contour(img,th):
    res=img
    #show('ori',img)
    # quita numeros y parte manuscrita
    (LOW,MED,HIGH)=th
    #show('ori r',res)
    #res=img
    gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(res, cv.COLOR_BGR2HSV)
    #show('hsv',hsv,last=False)
    
    h,s,v=cv.split(hsv)
    black = np.array([0,0,0])
    vr=''
    kernel = np.ones((3,3),np.uint8)
    kernel3 = np.ones((7,7),np.uint8)
    kernel5 = np.ones((11,11),np.uint8)
    Ugray =np.array([255,255,220])
    mask = cv.inRange(hsv, black, Ugray)
    qwe=np.asarray((s>50),np.uint8)        
    quee=255*qwe
    mask=mask-quee
    #show('init',mask,0.15,last=False)
    other=shakeLR(mask,5,1)
    #show('other',other,0.15,last=False)
    added=cv.add(mask,other)
    #show('addd',added,0.15)    
    openn = cv.morphologyEx(added, cv.MORPH_OPEN, kernel)
    del added
    del mask
    #show('st1',openn,0.15,last=False)
    closing = cv.morphologyEx(openn, cv.MORPH_CLOSE, kernel3)
    del openn
    #show('st2',closing,0.15,last=False)


    erosion = cv.erode(closing,kernel,iterations = 3)
    erosion = cv.morphologyEx(erosion, cv.MORPH_CLOSE, kernel5)    
    erosion=fillHoles(erosion)
    #show('st3',erosion,0.15,last=False)
    erosion = cv.erode(erosion,cv.getStructuringElement(cv.MORPH_RECT,(5,1)),iterations = 3)
    #show('st3y',erosion,0.15,last=False)

    dilation = cv.dilate(erosion,kernel3,iterations = 1)
#    dilation = cv.dilate(dilation,kernel,iterations = 1)
    #show('st4',dilation,0.15)

#    closing = cv.morphologyEx(dilation, cv.MORPH_CLOSE, kernel5)
    closing=fillHoles(dilation)
    #show('st5s',closing,last=False)
    
    del dilation
    closing = cv.morphologyEx(closing, cv.MORPH_CLOSE, kernel5)
    closing = cv.morphologyEx(closing, cv.MORPH_CLOSE, kernel5)
    
    blackhat = cv.morphologyEx(closing, cv.MORPH_BLACKHAT, np.ones((21,21),np.uint8))
    closing=cv.add(blackhat,closing)
    clos=fillHoles(closing)
    #show('bh',blackhat,last=False)
    
    #show('st5',closing,last=False)
    del blackhat
    
    
    
    #erosion = cv.erode(closing,cv.getStructuringElement(cv.MORPH_CROSS,(3,3)),iterations = 6)
    #show('st6',erosion,0.15,last=False)
    #erosiony = cv.erode(erosion,cv.getStructuringElement(cv.MORPH_RECT,(5,1)),iterations = 6)
    #show('st6y',erosiony,0.15,last=False)
    erosion = cv.erode(closing,np.ones((21,21),np.uint8),iterations = 1)
    #show('st6y',erosion,0.15,last=False)
    erosion = cv.dilate(erosion,np.ones((7,7),np.uint8),iterations = 1)
    erosion = cv.dilate(erosion,np.ones((3,3),np.uint8),iterations = 6)
    #show('st6z',erosion,0.15,last=False)
    closing = cv.morphologyEx(erosion, cv.MORPH_CLOSE,np.ones((9,9),np.uint8))
    del erosion
    #show('st7',closing,0.15,last=False)
    prep=closing.copy()
    del closing
    #show('test',prep)
    
    
    #plt.figure(1)
    #plt.imshow(prep)
    #plt.show()
    
    # fin
    #_, contours, _ = cv.findContours(dist_8u, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    _, contours, _ = cv.findContours(prep, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Create the marker image for the watershed algorithm
    cntr,imf,coor=filter(contours,(800,10000),1,1,res)
    #show('st12',imf,0.15)
    # Draw the foreground markers
    #print(len(contours))
    ##### aqui ya estan las respuestas segmentadas, ahora debo trabajarlas una por una
    #resg6 = cv.resize(g6,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
    return (cntr,imf*0,imf,coor)

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

def floodFill(src,connectivity,tolerancia,point):
    flags = connectivity
    flags |= cv.FLOODFILL_FIXED_RANGE
    cv.floodFill(src, None, point, (0, 255, 255), (tolerancia) * 3, (tolerancia) * 3, flags)
    return src
#califica(file_name,103)
def Califica(file,th,baseDir):
    print('->',datetime.datetime.now())
    OldName=file
    newName=file
    Idprueba,Id,response=(False,False,False)
    #carga image
    print(file)
    im = cv.imread(file)
    #implus= cv.add(~im,~im)
    #implus= cv.add(implus,implus)
    #implus= cv.add(implus,implus)
    
    save=cv.imread(file)
    h,w,_=im.shape
    #print(h,w)
    #plt.figure(1)
    #plt.imshow(~im)
    #plt.show()
    #show('original',im,0.5)
    #plt.figure(1)
    #plt.imshow(implus)
    #plt.show()
    #plt.figure(1)
    #plt.imshow(~implus)
    #plt.show()
    
    #input('???')
    #show('original',im,0.5)
    
    QR= im[500:800,1000:w].copy()
    id_part = im[0:800,0:800].copy()
    res_part = im[800:h,0:w].copy()
    #preprocesamiento de imagen - identficacion
    median = cv.medianBlur((~id_part),11)
    gray = cv.cvtColor(median,cv.COLOR_BGR2GRAY)
    _, otsu = cv.threshold(gray,25,255,cv.THRESH_BINARY)
    merge=cv.merge((~otsu,~otsu,~otsu))
    ipm=cv.bitwise_and(id_part,merge)
    #preprocesamiento de imagen - respuestas
    median = cv.medianBlur((res_part),11)
    _,_,vv=cv.split(cv.cvtColor(~res_part,cv.COLOR_BGR2HSV))
    median = cv.medianBlur((vv),11)
    median = cv.medianBlur((~median),11)
    _, otsu = cv.threshold(median,200,255,cv.THRESH_BINARY)
    #dilatar mascara
    otsu = cv.dilate(otsu,cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5)),iterations = 2)
    merge=cv.merge((otsu,otsu,otsu))
    rpm=cv.bitwise_and(res_part,merge)
    #Reasignacion de matrices
    im[800:h,0:w]=rpm
    im[0:800,0:800]=ipm    
    im[500:800,1000:1700]=QR
    #show('sc',save,0.5,False)
    #show('sharpen2',im,0.5)   
    QR= im[0:800,0:1700]
    
    #show('QR',QR,0.5)
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
        
        im[0:720,600:1700]=255
        im[0:420,0:1700]=255
        #plt.figure(1)
        #plt.imshow(im)
        #plt.show()
        imrQ=CR.remove(im, decodedObjects,fact)
        # pinta ancla
        #print(decodedObjects[0].rect)
        imres = cv.resize(imrQ,None,fx=3, fy=3, interpolation = cv.INTER_CUBIC)
        h,w,_=imres.shape
        fr=700
        imres=imres[fr:h, 0:w]
        anX=decodedObjects[0].rect.left
        anY=decodedObjects[0].rect.top-fr
        Ui=anY-520
        Li=anX-3302
        Ur=anY+676
        Lr=anX-3302
        U=Ui
        B=Ui+900
        #print(B)
        L=Li
        R=Li+1100
        
        #show('after qr',imrQ,0.5)
        ##remove logo
        
        #show('sc',imres,last=False)
        #show('c',imres[fr:h, 0:w])
        
        imcnt=imres.copy()
        
        #plt.figure(1)
        #plt.imshow(imres)
        #plt.show()
        
        #518
        #474    
        #
        #generar contornos
        #show('before',imres)
        U=Ui
        B=Ui+900
        #print(B)
        L=Li
        R=Li+1100
        #print(R)
        #inserta las lineas
        Ry=88
        Rx=30

        for i in range(0,11):
            sp=Ry*i
            cv.line(imcnt,(L,U+sp),(R,U+sp),(255,255,255),15)
            sp=(Ry+13)*i
            cv.line(imcnt,(L+(sp),U),(L+(sp),B),(255,255,255),15)
            #cv.line(imres,(0,U+sp),(2000,U+sp),(255,0,0),5)
        cv.rectangle(imres,(L,U),(R,B),(255,0,255),3)
        first_line=Ur
        mar=(Lr,Lr+4000,112)        
        he=106
        secs=get_section(first_line,pre,he,161)
        qwe=0
        #print(secs)
        for i in range(0, len(secs)):
            lim=secs[i]
            pr=pre[i]
            U,B=lim
            L,R,Q=mar
            for i in range(0,int(pr)+1):
                sp=he*i
                cv.line(imcnt,(L,U+sp),(R,U+sp),(255,255,255),5)
            for i in range(0,36):
                sp=Q*i
                cv.line(imcnt,(L+sp,U),(L+sp,B),(255,255,255),5)
                
            #show('fili'+str(qwe),imFilter[U:B,L:R],0.3,False)
            qwe+=1
        #show('imcnt',imcnt,0.5)
        cont,mrk,imFilter,coor =get_contour(imcnt,th)
        cv.circle(imres,(anX,anY), 20, (255,0,255), -1)
        cv.circle(imres,(Li,Ui), 20, (255,0,0), -1)
        cv.circle(imres,(Lr,Ur), 20, (0,255,0), -1)
        imra=imFilter.copy()
        
        cv.circle(imra,(anX,anY), 100, (0,0,255), -1)

        #print(anX,anY)
        #show('test',imra)
        U=Ui
        B=Ui+900
        #print(B)
        L=Li
        R=Li+1100
        #print(R)
        #inserta las lineas
        Ry=88
        Rx=30

        for i in range(0,11):
            sp=Ry*i
            cv.line(imFilter,(0,U+sp),(2000,U+sp),(255,0,0),5)
            cv.line(imFilter,(L+(40*i),U),(L+(40*i),B),(255,0,0),5)
            #cv.line(imres,(0,U+sp),(2000,U+sp),(255,0,0),5)
        cv.rectangle(imres,(L,U),(R,B),(255,0,255),3)
        #show('fili1',imFilter[U:B,L:R],0.5)
        # obtiene documento de identidad  --- Id 
        #(120,427,140,530)
        #Rx=input('rx?' )
        Id=get_id_c((U,B,L,R),coor,int(Rx),int(Ry))
        #input(Id)
        #contorno a respuest
        resu=['0']*(int(Max))
        first_line=Ur
        mar=(Lr,Lr+4000,112)        
        he=106
        secs=get_section(first_line,pre,he,161)
        qwe=0
        #print(secs)
        for i in range(0, len(secs)):
            lim=secs[i]
            pr=pre[i]
            U,B=lim
            L,R,Q=mar
            for i in range(0,int(pr)+1):
                sp=he*i
                cv.line(imFilter,(L,U+sp),(R,U+sp),(0,255,255),5)
                cv.line(imres,(L,U+sp),(R,U+sp),(0,255,0),5)
            for i in range(0,36):
                sp=Q*i
                cv.line(imFilter,(L+sp,U),(L+sp,B),(0,255,255),5)
                cv.line(imres,(L+sp,U),(L+sp,B),(0,255,0),5)
                
            #show('fili'+str(qwe),imFilter[U:B,L:R],0.3,False)
            qwe+=1
        #print(secs)
        #show('filiFul',imFilter,0.15)
        resu=get_resp_c(mar,coor,pre,secs,he,resu)
        #resu=get_resp(pre,secs,36,(cont,mrk),mar,resu,imr.copy())
        resp=[]
        for i in range(0,len(resu)):
            resp.append(str(resu[i]))
        response=''.join(resp)




        folder=checkFolder(baseDir+Idprueba)
        folder='./'+folder
        print()
        nm=OldName
        nm=str(Id)
        #print(datetime.datetime.now())
        #input('ALMOST')
        #nm=str(datetime.datetime.now()).replace(' ','--').replace('.','&').replace(':','&')
        
        newName=folder+"/"+nm+".jpg"
        
        k=1
        while os.path.isfile(newName)==True:
            newName=folder+"/"+nm+'-'+str(k)+".jpg"
            k+=1
        #show('fili',imFilter,0.15)
        #input('ready??')
#        input(newName)
        print(Idprueba,Id,response)
        #show('filtro',imres)
        #input('ready')
        print(cv.imwrite(newName,save))
        #folder=checkFolder(baseDir+Idprueba+'/grid')
        #ctName=folder+"/grid-"+nm+".jpg"
        #print(cv.imwrite(ctName,imres))

        #print(OldName)
        #print(newName)
    else:
        head,tail=os.path.split(OldName)
        folder=checkFolder(baseDir+'sinQR')
        newName=folder+"/"+tail
        cv.imwrite(newName,save)
        #cv.imwrite(ctName,imFilter)
    if os.path.isfile(newName):
        #print(file)
        os.remove(file)
    else:
        print('error al Eliminar')
    print('->',datetime.datetime.now())
    
    return (Idprueba,Id,response)

#ls=get_section(0,[4,4,8,4],30,20)

#print(ls)
#print(check_Range(130,ls,))```
