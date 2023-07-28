import time
from picamera2 import Picamera2, Preview
import cv2
import numpy as np

azulBajo = np.array([100, 100, 20], np.uint8) #Valor RGB(17,51,0)
azulAlto = np.array([125, 255, 255], np.uint8) #Valor RGB(0,255,21)

amarilloBajo = np.array([15, 100, 20], np.uint8) #Valor RGB(0,255,21)
amarilloAlto = np.array([45, 255, 255], np.uint8)

verdeBajo = np.array([38, 100, 20], np.uint8)
verdeAlto = np.array([85, 255, 255], np.uint8)

rojoBajo1 = np.array([0, 190, 20], np.uint8)
rojoAlto1 = np.array([5, 255, 255], np.uint8)

rojoBajo2 = np.array([175, 190, 20], np.uint8)
rojoAlto2 = np.array([179, 255, 255], np.uint8)

def CalculoArea(mask):
    
    count = 0
    
    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        
        count = area + count
            
            
    return count


def detectacolor(frame):
    
    # Pasamos de BGR a HSV
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    maskVerde = cv2.inRange(frameHSV, verdeBajo, verdeAlto)
    
    maskRojo1 = cv2.inRange(frameHSV, rojoBajo1, rojoAlto1)
    maskRojo2 = cv2.inRange(frameHSV, rojoBajo2, rojoAlto2)
    maskRojo = cv2.add(maskRojo1, maskRojo2)
    
    Totalmask = cv2.add(maskVerde, maskRojo)
    
    Coloredmask = cv2.bitwise_and(frame, frame, mask= Totalmask)
    
    # print(maskRojo)
    
    areaVerde = CalculoArea(maskVerde)
    print('Area Verde: ', areaVerde)

    areaRojo = CalculoArea(maskRojo)
    print('Area Rojo: ', areaRojo)
    
    areaTotal = areaVerde + areaRojo
    
    porcVerde = (areaVerde / areaTotal) * 100
    print('Porcentaje de Area Verde: ', porcVerde)
    
    porcRojo = (areaRojo / areaTotal) * 100
    print('Porcentaje de Area Rojo: ', porcRojo)
    
    # Mostramos la ventana de captura
    cv2.imshow('Verde', maskVerde)
    cv2.imshow('Rojo', maskRojo)
    cv2.imshow('Verde y Rojo', Totalmask)
    cv2.imshow('Coloreada', Coloredmask)
    

while True:
    
    picam = Picamera2()
    
    config = picam.create_preview_configuration()
    picam.configure(config)

    # picam.start_preview(Preview.QTGL)

    picam.start()
    time.sleep(0.05)
    picam.capture_file("test-python.jpg")

    picam.close()
    
    frame = cv2.imread('test-python.jpg')
    
    detectacolor(frame)
    
    time.sleep(0.25)
    
    # Detenemos la visualización con la tecla 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
