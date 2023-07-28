#!/usr/bin/python3

import time
from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import os


# client = mqtt.Client()
#client.connect("test.mosquitto.org")

#client.connect("localhost")

client = mqtt.Client(transport='websockets')
# client.connect("test.mosquitto.org", 8080, 60)
client.connect("broker.emqx.io", 8083, 60)

# azulBajo = np.array([100, 100, 20], np.uint8) #Valor RGB(17,51,0)
# azulAlto = np.array([125, 255, 255], np.uint8) #Valor RGB(0,255,21)

# amarilloBajo = np.array([15, 100, 20], np.uint8) #Valor RGB(0,255,21)
# amarilloAlto = np.array([45, 255, 255], np.uint8)

verdeBajo = np.array([38, 100, 20], np.uint8)
verdeAlto = np.array([85, 255, 255], np.uint8)

rojoBajo1 = np.array([0, 190, 20], np.uint8)
rojoAlto1 = np.array([5, 255, 255], np.uint8)

rojoBajo2 = np.array([175, 190, 20], np.uint8)
rojoAlto2 = np.array([179, 255, 255], np.uint8)

comment = False
comment2 = False

os.environ["LIBCAMERA_LOG_LEVELS"] = "3"


def sendDatatoMQTT(client, porcVerde, porcRojo):
    print("Connected")

    # The four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('TopicTestVerde', porcVerde)
    print(f"send {porcVerde} to TopicTestVerde")
    
    client.publish('TopicTestRojo', porcRojo)
    print(f"send {porcRojo} to TopicTestRojo")
    
    
    
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)



def CalculoArea(mask):
    
    count = 0
    
    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        
        count = area + count
            
            
    return count



def detectacolor(frame, Bajo, Alto):
    
    # Pasamos de BGR a HSV
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(frameHSV, Bajo, Alto)
    
    return mask
    
    
    
while True:
    
    picam = Picamera2()
    
    config = picam.create_still_configuration()
    picam.configure(config)

    # picam.start_preview(Preview.QTGL)

    picam.start()
    time.sleep(0.05)
    picam.capture_file("test-python.jpg")

    picam.close()
    
    frame = cv2.imread('test-python.jpg')
    
    maskVerde = detectacolor(frame, verdeBajo, verdeAlto)
    
    maskRojo1 = detectacolor(frame, rojoBajo1, rojoAlto1)
    maskRojo2 = detectacolor(frame, rojoBajo2, rojoAlto2)
    
    maskRojo = cv2.add(maskRojo1, maskRojo2)
    
    Totalmask = cv2.add(maskVerde, maskRojo)
    
    Coloredmask = cv2.bitwise_and(frame, frame, mask= Totalmask)
    
    areaVerde = CalculoArea(maskVerde)
    print('Area Verde: ', areaVerde)

    areaRojo = CalculoArea(maskRojo)
    print('Area Rojo: ', areaRojo)
    
    areaTotal = areaVerde + areaRojo
    
    if areaTotal != 0:
        
        porcVerde = round((areaVerde / areaTotal) * 100)
        print('Porcentaje de Area Verde: ', porcVerde)

        porcRojo = round((areaRojo / areaTotal) * 100)
        print('Porcentaje de Area Rojo: ', porcRojo)
        
        sendDatatoMQTT(client, porcVerde, porcRojo)
    else:
         print('No hay datos sufcientes')
             
             
    if comment == True:
        # Mostramos la ventana de captura
        cv2.imshow('Verde', maskVerde)
        cv2.imshow('Rojo', maskRojo)
        cv2.imshow('Verde y Rojo', Totalmask)
        cv2.imshow('Coloreada', Coloredmask)
        
    if comment2 == True:
        # Mostramos la ventana de captura
        
        resize = ResizeWithAspectRatio(Coloredmask, width=980) # Resize by width OR
        # resize = ResizeWithAspectRatio(Coloredmask, height=480) # Resize by height 

        cv2.imshow('Coloreada', resize)
    
    time.sleep(0.15)
    
    # Detenemos la visualización con la tecla 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break