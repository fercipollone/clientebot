import wmi
import json
import os
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

def leerConfig():
    config = json.loads(open('configProc.json', 'r').read())
    return config

def iniciarProceso(proc):
    config = leerConfig()
    print(config['PROCESO']['PathCliente'])
    SW_SHOWNORMAL = 1

    print("Iniciamos proceso!")
    process_startup = proc.Win32_ProcessStartup.new()
    process_startup.ShowWindow = SW_SHOWNORMAL
    proc.Win32_Process.Create(CommandLine=config['PROCESO']['PathCliente'], ProcessStartupInformation = process_startup)

def VerificarSupervivenciaProceso(proc, pid):
    if chequeaProceso(): #chequeamos si lleva mas de 30' sin modificar archivo de supervivencia 
        print(f"Terminamos proceso! {pid}")
        proc.Win32_Process(ProcessId=pid)[0].Terminate() #lo terminamos
        iniciarProceso(proc) #lo iniciamos

def chequeaProceso():
    config = leerConfig()
    #devuelve los minutos en que fue modificado
    ultMod = os.path.getmtime(config['SUPERVIVENCIA']['Path'])
    ultModTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ultMod))

    #obtenemos los minutos actuales
    actual = datetime.now()
    actual = actual.strftime("%Y-%m-%d %H:%M:%S")

    ultModTime = datetime.strptime(ultModTime, '%Y-%m-%d %H:%M:%S')
    actual = datetime.strptime(actual, '%Y-%m-%d %H:%M:%S')
    
    #Calcula diferencia
    diff = relativedelta(actual, ultModTime)
    
    if diff.minutes >= config['SUPERVIVENCIA']['Minutos']: #Hace mas de 30 min que se modifico
        print(f"{diff.minutes} Minutos sin procesar información.")
        return True

    return False

def bot():
    
    config = leerConfig()
    encontro = False
    pid = 0

    proc = wmi.WMI()
    for process in proc.Win32_Process(): #obtiene todos los procesos que se encuentran activos

        if process.Name == config['PROCESO']['Cliente']: #preguntamos si es uno de los activos
            print(f"{process.ProcessId:<10} {process.Name}")
            pid = process.ProcessId
            encontro = True

    if not encontro:
        iniciarProceso(proc)
    else:
        VerificarSupervivenciaProceso(proc, pid)
        

