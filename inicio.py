from log import *

def validaInicioBot():
    
    #PREGUNTAMOS SI TENEMOS EL ARCHIVO DE CONFIGURACION
    if os.path.isfile('configProc.json'):
        return True
    else:
        logArchivo("inicio", "validaInicioBot", "NO SE ENCUENTRA EL ARCHIVO DE CONFIGURACION: configProc.json")
        return False