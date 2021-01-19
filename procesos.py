import wmi
import json
import os
import time 
import signal
import subprocess
from util import *
from log import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

def obtenerConfig():
    global config 
    config = leerConfig()

def leerConfig():
    configpath = leerConfigPath()[1] + 'configProc.json'
    file = open(configpath, 'r').read()
    config = json.loads(file)
    return config

def iniciarProceso(proc):
    SW_SHOWNORMAL = 1

    try:
        process_startup = proc.Win32_ProcessStartup.new()
        process_startup.ShowWindow = SW_SHOWNORMAL
        commandlinec = f"{config['PROCESO']['PathCliente']} {config['PROCESO']['PathConfig']}"
        proc.Win32_Process.Create(CommandLine=commandlinec, ProcessStartupInformation = process_startup)
    except Exception as exp:
        logArchivo("procesos.py", "iniciarProceso", exp)

def VerificarSupervivenciaProceso(proc, pid):
    if chequeaProceso(): 
        KillProcess()
        iniciarProceso(proc) #lo iniciamos

def chequeaProceso():
    #devuelve los minutos en que fue modificado
    ultMod =  datetime.fromtimestamp(os.path.getmtime(config['SUPERVIVENCIA']['Path']))
    
    #Obtener fecha actual 
    actual = datetime.now()
    
    #Calcula diferencia
    diff = relativedelta(actual, ultMod)

    if diff.days >= 1:
        return True 

    if diff.hours >= 1:
        return True

    if diff.minutes >= config['SUPERVIVENCIA']['Minutos']: 
        return True

    return False

def bot():    
    obtenerConfig()
    encontro = False
    pid = 0

    proc = wmi.WMI()
    for process in proc.Win32_Process(Name=config['PROCESO']['Cliente']): 
        # print(f"{process.ProcessId:<10} {process.Name}")
        pid = process.ProcessId
        encontro = True    

    if not encontro:  
        # print('Inicia Proceso porque no lo econtro')
        iniciarProceso(proc)
    else:
        # print('Lo encontre vamos a verificar la supervivencia')
        VerificarSupervivenciaProceso(proc, pid)
            
def KillProcess():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(["taskkill", "/IM", config['PROCESO']['Cliente'], "/T", "/F"], startupinfo=si)