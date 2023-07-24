from PetTechLibrary import Dispense,connectWifi,initComponents

if connectWifi():
    initComponents()#inicialicamos componentes
    while True:
        Dispense()