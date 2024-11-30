#Mostrar las partes rojas de la imagen
import cv2 as cv

img = cv.imread('pez.jpg', 1)

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
ubb = (0,100,150) #En hsv el color rojo va de 0 a 10, y de 170 a 180
uba = (10,255,255)
ubb2 = (170,100,150)
uba2 = (180,255,255)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)

mask = mask1+mask2
res = cv.bitwise_and(img, img, mask=mask)



cv.imshow('img', img)
cv.imshow('mask', mask)
cv.imshow('hsv', hsv)
cv.imshow('res', res)

cv.waitKey(0)
cv.destroyAllWindows()