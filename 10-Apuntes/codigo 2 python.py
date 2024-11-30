####################
###################
#Importar Video

import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret,img = cap.read()
    if ret:
        cv.imshow('img', img)
        k=cv.waitKey(1) & 0xFF
        if k == 27:
            break

    
cap.release()
cv.destroyAllWindows()