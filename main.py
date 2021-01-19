from procesos import *
from inicio import *

if __name__ == "__main__":
    if validaInicioBot():
        bot()
    else:
        print('No paso la validacion incial')
