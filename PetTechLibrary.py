from hx711 import HX711
from machine import Pin, ADC, PWM, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep, sleep_ms
import network, time
import ujson
import ufirebase as firebase
import utime
import umail
global miRed
urlFireBase='https://pettechesp32-default-rtdb.firebaseio.com/'
import umail
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
nameNetWork = "Torre 3 Apto 1108"
password= "89042066380"


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Funciones manejo de funcionalidad>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Funcion de inicialización de componentes   
def initComponents():
    print("No coloque peso")
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
    CalculateRation()
    sleep(5)
    
#Funcion para calibrar solo se usa una vez y se obtiene el valor para la variable scaleCalibration
def calibrate(scale):
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
    sleep(2)
    return round(scale.get_units(10),2)

#Funcion que cierra la puerta
def closeDoor(weight):
    print("Compuerta Cerrada")
    print("Peso: {:.1f}".format(weight),"gr.")
    servo.duty(map_servo(closeServo))#cierra
    #showOledWeight("Peso:{:.2f}".format(weight),"Cerrada...")
#Función que abre la puerta   
def openDoor(weight):
    servo.duty(map_servo(openServo))#abre 
    print("Peso: {:.1f}".format(weight),"gr.")
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
#conexion a Wifi
def connectWifi():
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(nameNetWork, password)         #Intenta conectar con la red
          print('Conectando a la red', nameNetWork +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  print ("Imposible conectar")
                  miRed.active(False)
                  return False
      print("Conexión Exitosa!")
      print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
      return True

def GetConsumos():
     firebase.setURL(urlFireBase)
     firebase.get("/Consumos/","dato",bg=0)
     return firebase.dato
def GetPrametroPeso():
     firebase.setURL(urlFireBase)
     firebase.get("/ParametrosPeso/","dato",bg=0)
     return firebase.dato
def GetRangosPesos():
     firebase.setURL(urlFireBase)
     firebase.get("/RangosPesos/","dato",bg=0)
     return firebase.dato
def GetActualDate():
    # Obtener el tiempo Unix en segundos
    tiempo_unix = utime.time()

    # Convertir el tiempo Unix a una tupla de tiempo local
    tiempo_local = utime.localtime(tiempo_unix)

    # Obtener el día, mes y año del tiempo local
    dia_actual = tiempo_local[2]
    mes_actual = tiempo_local[1]
    anio_actual = tiempo_local[0]
    date = (f"{dia_actual:02d}/{mes_actual:02d}/{anio_actual}")
    return date
def GetActualTime():
    # Obtener el tiempo Unix en segundos
    tiempo_unix = utime.time()

    # Convertir el tiempo Unix a una tupla de tiempo local
    tiempo_local = utime.localtime(tiempo_unix)

    # Obtener la hora, minutos y segundos del tiempo local
    hora_actual = tiempo_local[3]
    minutos_actual = tiempo_local[4]
    hora = (f"{hora_actual:02d}:{minutos_actual:02d}")
    return hora

def CalculateRation():
    parametroPeso= GetPrametroPeso()#esto devuelve un diccionario
    peso_kg = parametroPeso["PesoKg"]
    #racion = parametroPeso["Racion"]
    total_consumo_diario = parametroPeso["TotalConsumoDiario"]
    cantidad_raciones = parametroPeso["CantidadRaciones"]
    intervalo_horas = parametroPeso["IntervaloHoras"]
    #print(peso_kg,total_consumo_diario,cantidad_raciones)
    parametroRango=GetRangosPesos()#esto devuelve un diccionario
    #print(parametroRango)
    #print(type(parametroRango))
    #Leo los parametros
    data_ordenado = dict(sorted(parametroRango.items()))#ordeno el diccionario
    #Iterar a través del diccionario e imprimir los valores
    for rango, detalles in data_ordenado.items():#busco en que rango esta el peso que ingresaron
        if value_in_range(parametroPeso["PesoKg"],detalles["Rango-Peso"]):#si el peso esta en alguno de los rangos
            print("El peso" , parametroPeso["PesoKg"] , "Esta dentro del rango ",detalles["Rango-Peso"])
            if value_in_range(parametroPeso["TotalConsumoDiario"],detalles["Rango-Racion"]):#valido la cantidad si esta dentro del rango encontrado
                print("La ración Total" , parametroPeso["TotalConsumoDiario"] , "Esta dentro del rango ",detalles["Rango-Racion"])
                break
    calculoRacion = round(float(total_consumo_diario)/float(cantidad_raciones),1)
    print("Calculo de Ración ", calculoRacion)
    CreatePlan(intervalo_horas,calculoRacion,cantidad_raciones)#creamos el plan
#Evalua si el valor esta dentro del rango
def value_in_range(valor, rango_str):
    # Dividir el rango en dos valores mediante el guion "-"
    inicio, fin = map(float, rango_str.split('-'))
    # Verificar si el valor está dentro del rango
    return inicio <= float(valor) <= fin
#Crea el plan
def CreatePlan(hourInterval,ration,quantityRation):
    print("Generando Plan...")
    firebase.delete("/Consumos/",bg=0)
    # Obtener el tiempo Unix en segundos
    tiempo_unix = utime.time()

    # Convertir el tiempo Unix a una tupla de tiempo local
    tiempo_local = utime.localtime(tiempo_unix)

    # Obtener la hora, minutos y segundos del tiempo local
    hora_actual = tiempo_local[3]
    minutos_actual = tiempo_local[4]
    # Obtener el día, mes y año del tiempo local
    dia_actual = tiempo_local[2]
    mes_actual = tiempo_local[1]
    anio_actual = tiempo_local[0]
    firebase.setURL(urlFireBase)
    currentHour = hora_actual#que traiga la hora 
    for i in range(quantityRation):
         message = {"Fecha": (f"{dia_actual:02d}/{mes_actual:02d}/{anio_actual}"),"Hora":(f"{currentHour:02d}:{minutos_actual:02d}"),"Racion":str(ration)}
         #print("Mensaje",message,"Dato para crear","/Consumos/Consumo"+str(i))
         firebase.put("/Consumos/Consumo"+str(i+1),message,bg=0)
         currentHour += hourInterval#sumo el intervalo
         if currentHour > 23:
            currentHour -= 24
            dia_actual +=1
    print("Plan Generado Correctamente...")
#Armo la consulta de dispensación
def Dispense():
    #horaActualActual="15:43"#para probar
    #fechaActual = "23/07/2023"#para probar
    horaActualActual=GetActualTime()
    fechaActual=GetActualDate()
    #Saco el plan
    consumos = GetConsumos()#Obtengo consumos
    data_ordenado = dict(sorted(consumos.items()))#ordeno el diccionario
    #print(data_ordenado)
    encontrado, valorDispensar = buscarEnPlan(data_ordenado,horaActualActual,fechaActual)
    #print(encontrado,valorDispensar)
    if encontrado:#Si encontre a hora dentro del plan
        print("La hora y fecha actual se encuentran en el plan")
        estaVacio= True
        while estaVacio:
              weight = getWeight()
              print("peso vs valor a dispensar",weight,valorDispensar,weight == valorDispensar)
              print("diferencia:",abs(weight-valorDispensar))
              if round(weight,1) >= round(1,1):# si la balanza esta llena
                    print("Hay comida",weight,"gr.")
                    closeDoor(weight)
                    sleep(5)
                    estaVacio=False
              else:#esta en menos de un gramo
                  print("No hay comida",weight,"gr.")
                  print("Incio Dispensación")
                  while weight <= valorDispensar:
                          weight = getWeight()
                          print("No esta lleno todavía",weight,"gr.")
                          openDoor(weight)
                          #sleep(1)
                  print("Ya se lleno")
                  senDemail(weight,fechaActual,horaActualActual)
                  closeDoor(weight)#cierro cuando ya este lleno
                  estaVacio=False
                  sleep(5)
    else:
        print("La hora y fecha Actual no se encuentran en el plan")
    print("Fin dispensación")       
    
def buscarEnPlan(datos,hora_buscada,fecha_buscada):
# Bucle para buscar el dato
    encontrado=False
    valorDispesar= 0.0
    for key, data in datos.items():
        #print("Hora Dato",data['Hora'],"Fecha Dato",data['Fecha'])
        if data['Hora'] == hora_buscada and data['Fecha'] == fecha_buscada:
            encontrado = True
            valorDispesar = data['Racion'] 
            break
    return encontrado,float(valorDispesar)
def senDemail(gramosDispensados,Fecha,Hora):
    # Email details
    sender_email = 'pettech14@gmail.com'
    sender_name = 'PetTech Notificación' #sender name
    sender_app_password = 'kqabbxwlthtbunep'#clave de aplicación
    recipient_email ='albertloz20@gmail.com' #correo a donde se envia la notificación
    email_subject ='Notificación de Dispensación'
    print("inicio envio")
    mailStruct = f'''
                Fecha: {Fecha}
                Hora: {Hora}
                Gramos Dispensados: {gramosDispensados}
                '''
    # Send the email
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write(mailStruct)
    smtp.send()
    smtp.quit()
    print("enviado")
    
    