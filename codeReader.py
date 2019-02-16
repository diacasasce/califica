from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  #for obj in decodedObjects:
    #print('Type : ', obj.type)
    #print('Data : ', obj.data,'\n')
     
  return decodedObjects

def scale(data,fact=1):
  resp=[]
  for point in data:
    x,y=(point.x,point.y)
    x=int(x/fact)
    y=int(y/fact)
    resp.append((x,y))
  return(resp)
 
# Display barcode and QR code location  
def display(im, decodedObjects,fact=1):
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = scale(decodedObject.polygon,fact)
    
    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
     
    # Number of points in the convex hull
    n = len(hull)
 
    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
# Display results 
  res = cv2.resize(im,None,fx=0.5 , fy=0.5, interpolation = cv2.INTER_CUBIC)  
  cv2.imshow("Results", res);
  cv2.waitKey(0);
  cv2.destroyAllWindows() 

# remove barcode and QR code location  
def remove(im, decodedObjects,fact=1):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = scale(decodedObject.polygon,fact)
    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
     
    # Number of points in the convex hull
    n = len(hull)
    #print('convex hull',n,(hull[0],hull[3]))
#    cv2.polylines(im,hull,True,(0,255,255),3)
  try:
    cv2.rectangle(im,hull[0],hull[2],(255,255,255),cv2.FILLED)
    cv2.rectangle(im,hull[0],hull[2],(255,255,255),5)
    return im
  except:
    return im

