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
 
 
# Display barcode and QR code location  
def display(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon
 
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
  cv2.imshow("Results", im);
  cv2.waitKey(0); 

# remove barcode and QR code location  
def remove(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon
 
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

