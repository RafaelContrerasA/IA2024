import cv2 as cv
import numpy as np
img = cv.imread('Pez.jpg', 0)
x,y = img.shape
print(img.shape)
img2 = np.zeros((x*2,y*2), dtype='uint8')

for i in range(x):
    for j in range(y):
        if(img[i,j]>150):   
            img[i, j]=255
        else:
            img[i, j]=0

        #img2[i*2, j*2] = 255 - img[i,j] Invertir 
        #img2[i*2, j*2] = img[i,j] Agrandar 

print(img2.shape)
cv.imshow('img', img)
#cv.imshow('img2', img2)
cv.waitKey(0)
cv.destroyAllWindows()

# rgb cymk hcv

