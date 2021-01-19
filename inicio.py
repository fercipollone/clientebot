from log import *
from util import *

def validaInicioBot():
    
    #PREGUNTAMOS SI TENEMOS EL ARCHIVO DE CONFIGURACION
    fileconfigpath = leerConfigPath() 
    if not fileconfigpath[0]:
        logArchivo("inicio", "validaInicioBot", "No se pudo leer la variable de entorno clientepath")
        return False 

    if os.path.isfile(fileconfigpath[1] + 'configProc.json'):
        return True
    else:
        msj = f"NO SE ENCUENTRA EL ARCHIVO DE CONFIGURACION: {fileconfigpath[1]}configProc.json"
        logArchivo("inicio", "validaInicioBot", msj)
        return False

    