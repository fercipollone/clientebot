import logging
import os
from datetime import date
from datetime import datetime

def configLog(name, log_file, level=logging.DEBUG):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if (logger.hasHandlers()):
        logger.handlers.clear()
    
    logger.addHandler(handler)

    return logger

def today():
    today = date.today()
    return "{}{:02d}{:02d}".format(today.year, today.month, today.day)

def logArchivo(proceso, funcion, msj):
    name = "C:\\Log\\BOT_ARCHIVO_%s.log" % (today())

    logger = configLog("ARCHIVO",name)
    log = f"PROCESO: {proceso} \n"
    log += f"FUNCION: {funcion} \n"
    log += f" {msj} \n" 
    logger.debug(log)
    print(msj)