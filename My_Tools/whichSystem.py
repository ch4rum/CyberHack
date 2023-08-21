#!/usr/bin/python3

import re, sys, subprocess, argparse, signal;
import string, time, platform;
from pwn import *;
# python3 wichSystem.py 10.10.10.188 

def handler(sig,fram):
    print(f"\n{colours.red}[!]{colours.reset} {colours.light_red}Saliendo ...{colours.reset}\n")
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT,handler)

class Colours:
    # Definición de códigos de colores
    color_codes = {
        'green':"\033[38;5;40m",          # Verde
        'dark_green':"\033[38;5;82m",     # Verde Oscuro
        'light_green':"\033[38;5;118m",   # Verde claro
        'reset':"\033[38;0;0m",           # Restablecer a los valores por defecto
        'yellow':"\033[38;5;226m",        # Amarillo
        'light_yellow':"\033[38;5;87m",   # Amarillo claro
        #light_yellow = "\033[38;5;229m"  # Amarillo claro
        'blue':"\033[38;5;27m",           # Azul
        'light_blue':"\033[38;5;39m",     # Azul claro
        'red':"\033[38;5;196m",           # Rojo
        'light_red':"\033[38;5;203m",     # Rojo claro
        'purple':"\033[38;5;165m",        # Púrpura
        'orange':"\033[38;5;208m",        # Naranja
        'pink':"\033[38;5;211m",          # Rosa
        'cyan':"\033[38;5;51m",           # Cian
        'gray':"\033[38;5;240m",          # Gris
        'reset': "\033[0m",               # reset colours
    }

    def __getattr__(self, name):
        if name in self.color_codes:
            return self.color_codes[name]
        else:
            raise AttributeError(f"Color '{name}' not found.")
    
def get_os_youSystem(colours):
    """
    Obtiene el nombre del sistema operativo a partir del archivo /etc/os-release.
    
    Retorna:
    - Nombre del sistema operativo o mensaje de error si no se puede determinar.
    """
    try:
        os_info = dict()
        with open("/etc/os-release","r") as os_system:
            for _ in os_system:
                key, values = _.strip().split("=")
                os_info[key] = values.strip('"')
            return os_info.get("NAME","Desconocido")
    except FileNotFoundError:
        return f"{colours.red}[!] {colours.reset}{colours.gray}Distribucion linux sin poder determinar{colours.reset}"

def get_argument(colours):
    """
    Obtiene los argumentos pasados al script mediante la línea de comandos.

    Retorna:
    - Argumentos obtenidos del parser.
    """
    parser = argparse.ArgumentParser(prog='WhichSystem.py',
                                     description='Identify the system using an IP address')
    parser.add_argument('ip_address', 
                        nargs='?',
                        metavar='<IP_ADDRESS>',
                        default=None,
                        type=str, 
                        help='IP address to identify the system')
    parser.add_argument('-r', '--requeriment',
                        dest='requeriment',
                        action='store_true',
                        help='List of requirements')
    parser.add_argument('-v','--version', 
                        action='version', 
                        version='%(prog)s 1.0')
    return parser.parse_args()

def get_ttl(ip_address,colours):
    """
    Obtiene el valor TTL de un ping a la dirección IP especificada.

    Parámetros:
    - ip_address: Dirección IP a la cual hacer ping.
    - colours: Objecto para colorear texto.

    Retorna:
    - Valor TTL obtenido del resultado del ping.
    """
    try:
        proc = subprocess.Popen([f"/usr/bin/ping -c 1 {ip_address}"], 
                                stdout=subprocess.PIPE, 
                                shell=True)
        (out,err) = proc.communicate()

        out = out.split()
        out = out[12].decode('utf-8')

        ttl_value = re.findall(r"\d{1,3}", out)[0]

        return int(ttl_value)
    except IndexError:
        print(f"{colours.red}[-]{colours.reset}{colours.gray} La IP {colours.yellow}{ip_address}{colours.reset} {colours.gray}no está activa o no responde al ping.{colours.reset}")
        return None
    
def get_os(ttl):
    """
    Obtiene el sistema operativo basado en el valor TTL.

    Parámetros:
    - ttl: Valor TTL.

    Retorna:
    - Nombre del sistema operativo.
    """
    if ttl >= 0 and ttl <= 64: return "Linux"
    elif ttl >= 65 and ttl <= 128: return "Windows"
    else: return None

def ask_show(os_name,characters,colours):
    """
    Mensaje a mostrar utilizando pwn con su sistema operativo.

    Parámetros:
    - os_name: nombre del os.
    - characters: string de caracteres.
    - colours: objecto de para colorear.

    """
    p1 = log.progress(f"{colours.blue}OS{colours.reset}")

    for _ in characters:
        p1.status(f"{colours.gray}Iniciando busqueda {colours.reset}{colours.red}{_}{colours.reset}")
        time.sleep(0.03)
    p1.status(f"{colours.gray}Sistema detectado => {colours.reset}{colours.yellow}{os_name}{colours.reset}")
    
if __name__ == '__main__':
    colours = Colours()
    args = get_argument(colours)
    characters = string.hexdigits + string.punctuation

    if platform.system() == "Windows":
        os_name = "Windows"
        ask_show(os_name,characters,colours)
    elif args.requeriment:
        listRequerimnet = ["pwntools"]
        [print(f"{colours.green}[+]{colours.reset} {colours.gray}{_}{colours.reset}") for _ in listRequerimnet]

    elif not args.ip_address or not hasattr(args,'ip_address') or args.ip_address is None:
        os_name = get_os_youSystem(colours)
        print(f"{colours.red}[-]{colours.reset} {colours.gray}Nose proporciono IP{colours.reset}")
        ask_show(os_name,characters,colours)

    else: 
        ip_address = args.ip_address

        ttl = get_ttl(ip_address,colours)
        if ttl is not None or ttl != None or ttl:
            p1 = log.progress(f"{colours.blue}OS{colours.reset}")

            for date1, date2 in zip(characters, reversed(characters)):
                p1.status(f"{colours.gray}Iniciando búsqueda {colours.reset}{colours.red}{date2}{date1}{colours.reset}")
                time.sleep(0.03)

            os_name = get_os(ttl)
            p1.status(f"{colours.yellow}{ip_address}{colours.reset}{colours.gray} (ttl -> {ttl}) => {colours.reset}{colours.yellow}{os_name}{colours.reset}")
