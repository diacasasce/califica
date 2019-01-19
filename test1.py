#librerias
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

#definiciones
im = cv.imread('scan3.jpg')
#OR
img = cv.resize(im,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
print(img.shape[:2])
print(im.shape[:2])
im0 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
b,g,r = cv.split(img)
r1=r*0
g1=g*0
b1=b*0
r2=255-r
g2=255-g
b2=255-b
b3=b2-r2-g2
im1=cv.merge((b2,g1,r1))
im1b=cv.merge((r1,g1,b2))
im1g=cv.merge((r1,g1,b3))
im1r=cv.merge((r2,g1,b1))
im2=cv.merge((b2,b2,b3+b3))
im3=cv.cvtColor(im1g,cv.COLOR_BGR2GRAY)
"""
plt.imshow(im1)
plt.show()
"""
plt.imshow(im1b)
plt.show()
plt.imshow(im1g)
plt.show()
"""
plt.imshow(im1r)
plt.show()
plt.imshow(im2)
plt.show()
"""
"""
titles = ['im0', 'im1b', 'im1g', 'im1r','im3']
images = [im0, im1b, im1g, im1r,im3]
for i in range(5):
    plt.subplot(5,1,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
"""
ret,thresh1 = cv.threshold(im3,127,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(im3,127,255,cv.THRESH_BINARY_INV)
blur = cv.GaussianBlur(im3,(5,5),0)
ret3,thresh3 = cv.threshold(blur,0,255,cv.THRESH_TRUNC+cv.THRESH_OTSU)
ret,thresh4 = cv.threshold(im3,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(im3,127,255,cv.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [im3, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in range(6):
    plt.imshow(images[i],'gray')
    plt.show()
    """
    plt.subplot(6,1,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
"""