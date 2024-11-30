#Mostrar solo un color especifico de un video
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while True:
  ret, img = cap.read()
  if ret:
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    ubb = (25,50,100)
    uba = (35, 255, 255)
    
    mask = cv.inRange(hsv, ubb, uba)
    res = cv.bitwise_and(img, img, mask=mask)
    
    cv.imshow('img', img)
    cv.imshow('res', res)
    
    k = cv.waitKey(1) & 0xFF
    if k == 27:
      break
    
cap.release()
cv.destroyAllWindows()