import json
import os 

def leerConfigPath():
    status = False 
    configpath = os.environ.get('clientepatharenasports', '0') 
    if (not configpath == '0'):
        status = True
    return [status, configpath]

def inspect(value):
    print('****************************************************************************************************')
    print(value)
    print('****************************************************************************************************')

def pause():
    os.system("pause")
