from hx711 import HX711
from machine import Pin, ADC, PWM, I2C
from ssd1306 import SSD1306_I2C
from time import sleep, sleep_ms
#parametros galga
scaleCalibration = 978.9762# Albert # valor referencia un celular de 220 gramos usando la función calibrate peso Albert
#scaleCalibration = 1448.194 # Kevin
dout = 4 #Definicion de pines
pd_sck = 5 #
#parametros servo
servoPin = 15
freq = 50
closeServo = 180
openServo= 90
#parametros oled
alto = 64
ancho = 128
#iniciamos componentes
#galga
scale = HX711(dout, pd_sck)
#servo
servo= PWM(Pin(servoPin), freq = freq)
#oled
#i2c=I2C(0, scl=Pin(22), sda=Pin(21))
#oled = SSD1306_I2C(ancho, alto, i2c)


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Funciones manejo de funcionalidad>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Funcion de inicialización de componentes   
def initComponents():    
    #print(i2c.scan(), "conectada")
    print("Iniciando, retire el peso...")    
    #oled.vline(0, 0, 20, 1)
    #oled.vline(120, 0, 20, 1)
    #oled.hline(0, 0, 120, 1)
    #oled.hline(0, 20, 120, 1)
    #oled.text("PetTech", 10, 10, 1)
    #oled.text("Iniciando...", 0, 30, 1)
    #oled.show()
    sleep(5)
    #oled.text("Retire peso...", 0, 40, 1)
    #oled.show()
    scale.set_scale(scaleCalibration)
    sleep(5)
    print("Generando tare...")
    scale.tare(20)
    sleep(5)
    print("Sistema Ok")
    servo.duty(map_servo(closeServo))#cierra
    sleep(5)
    
#Funcion para calibrar solo se usa una vez y se obtiene el valor para la variable scaleCalibration
def calibrate(scale):
    print("No coloque peso")
    scale.read()#inicio el comando 
    scale.set_scale(1)# seteo scala en 1
    #sleep(5) 
    print("Generando Tare...")
    scale.tare(20)
    sleep(5) 
    known_weight = float(input("Introduce el peso referencia en gramos: "))
    print("Coloque el peso")
    sleep(5) 
    print("Midiendo el peso del objeto...")
    measured_weight = scale.get_value(200)# LEO 100 LECTURAS
    print("Valor de Lectura: ", measured_weight)
    sleep(5) 
    # Calcular el factor de calibración.
    calibration_factor = float(measured_weight / known_weight)#saco la calibración peso medido/peso conocido
    #sleep(5) 
    print("El factor de calibracion es: ", calibration_factor)
    sleep(5) 
    print("Retire el peso de referencia")
    sleep(5)
    print("Sistema ok")
    #return calibration_factor
    print("Factor de Calibracion es : " , calibration_factor)

#Funcion que permite dar en grados el giro de los servomotores
def map_servo(x):        
        return int((x - 0) * (125 - 25) / (180 - 0) + 25)
#Función que lee el peso
def getWeight():
    return round(scale.get_units(10),2)#

#Funcion que cierra la puerta
def closeDoor(weight):
    print("Compuerta Cerrada")
    print("Peso: {:.2f}".format(weight),"gr.")
    servo.duty(map_servo(closeServo))#cierra
    #showOledWeight("Peso:{:.2f}".format(weight),"Cerrada...")
#Función que abre la puerta   
def openDoor(weight):
    servo.duty(map_servo(openServo))#abre 
    print("Peso: {:.2f}".format(weight),"gr.")
    print("Compuerta Abierta")
    #showOledWeight("Peso:{:.2f}".format(weight),"Abierta...")

#Muestra mensaje de peso en Oled
def showOledWeight(text,action):
    oled.fill(0)
    oled.pixel(64,60, 1)
    oled.vline(0, 0, 20, 1)
    oled.vline(120, 0, 20, 1)
    oled.hline(0, 0, 120, 1)
    oled.hline(0, 20, 120, 1)
    oled.text("PetTech", 10, 10, 1)
    oled.text(action, 0, 30, 1)#abierto o cerrado
    oled.text(text, 0, 40, 1)
    oled.show()
    
