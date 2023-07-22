from PetTechLibrary import *


if connectWifi():
   
  
    initComponents()#inicialicamos componentes
    while True:
            weight = getWeight() # leo 10 veces para ser más precisos      
            if round(weight,1) >= round(1,1):#el valor es mayor a 1 gramo cierra por que hay comida
                closeDoor(weight)
            else:#Si el valor es 0 abre la compuerta
                openDoor(weight)



