#!/usr/bin/python3

import signal, sys, requests, string, subprocess;
import os, argparse;
from pwn import *; 
from urllib.parse import urlparse
from time import sleep; 

def handler(sig, frame):
    print(f"\n\n{colours.red}[!] {colours.reset}{colours.light_red}Saliendo ...{colours.reset}\n")
    sys.exit(1)

# ctrl + c    
signal.signal(signal.SIGINT, handler)

class Colours:
    # Definición de códigos de colores
    color_codes = {
        'green':"\033[38;5;40m",          # Verde
        'dark_green':"\033[38;5;82m",     # Verde Oscuro
        'light_green':"\033[38;5;118m",   # Verde claro
        'reset':"\033[38;0;0m",           # Restablecer a los valores por defecto
        'yellow':"\033[38;5;226m",        # Amarillo
        #'light_yellow':"\033[38;5;87m",   # Amarillo claro
        'light_yellow':"\033[38;5;229m",  # Amarillo claro
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

def banner():
    # Imprime el banner del programa con colores y diseño especial.
    print('''
    \u001b[31m                                                          
    @@@  @@@  @@@  @@@  @@@   @@@@@@   @@@@@@@             @@@  @@@@@@@    @@@@@@   
    @@@  @@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@             @@@  @@@@@@@@  @@@@@@@@  
    @@!  @@!  @@!  @@!  @@@  @@!  @@@    @@!               @@!  @@!  @@@  @@!  @@@  
    !@!  !@!  !@!  !@!  @!@  !@!  @!@    !@!               !@!  !@!  @!@      @!@   
    @!!  !!@  @!@  @!@!@!@!  @!@!@!@!    @!!    @!@!@!@!@  !!@  @!@@!@!      !!@    
    !@!  !!!  !@!  !!!@!!!!  !!!@!!!!    !!!    !!!@!@!!!  !!!  !!@!!!      !!@     
    !!:  !!:  !!:  !!:  !!!  !!:  !!!    !!:               !!:  !!:                 
    :!:  :!:  :!:  :!:  !:!  :!:  !:!    :!:               :!:  :!:         !:!     
    :::: :: :::   ::   :::  ::   :::     ::                ::   ::          ::     
    :: :  : :     :   : :   :   : :     :                :     :          :::                                                                                                      
                                                                               \033[38;5;81mv1.0''')
    print("\u001b[37m--------------------------------------------------------------------------------")
    print("\t\t\t\t\033[38;5;226mA resource for the cybersecurity community")
    print("\u001b[37m--------------------------------------------------------------------------------")

def get_argument():
    """
    Parsea los argumentos de línea de comandos usando argparse.

    Retorna:
    - argparse.Namespace: Objeto que contiene los argumentos parseados.
    """
    parser = argparse.ArgumentParser(prog="Ip_publy.py",
                                     description="Get the IP address of a URL or display the public IP of the system.")
    parser.add_argument('host',
                        nargs='?',
                        metavar='<HOST>',
                        default=None,
                        type=str,
                        help="URL or address for which to get the IP address.")
    parser.add_argument('-r', '--requeriment',
                        dest='requeriment',
                        action='store_true',
                        help='Install the required dependencies for the program.')
    parser.add_argument('-v','--version',
                        action='version',
                        version='%(prog)s 1.0')
    return parser.parse_args()

def install_requeriments(colours):
    """
    Instala los requerimientos necesarios para el programa.

    Parámetros:
    - colours (Colours): Objeto para colorear texto.
    """
    requeriments = ['pwntools', 'requests']
    pathExist = os.path.exists('/etc/os-release')
    try:
        for package in requeriments:
            if pathExist:
                os_info = {}
                with open('/etc/os-release', 'r') as os_system:
                    for _ in os_system:
                        key, value = _.strip().split('=')
                        os_info[key] = value.strip('"')
                    os_name = os_info.get('NAME', 'Desconocido')
                    if os_name.lower() == 'arch' or os_name.lower() == "arch linux":
                        subprocess.check_call(['sudo', 'pacman', '-S', f'python-{package}', '--noconfirm'])
                        print(f"\n{colours.dark_green}[+]{colours.reset}{colours.green} Requerimientos instalados exitosamente.{colours.reset}\n")
                    elif os_name.lower() == 'debian' or os_name.lower() == 'ubuntu':
                        subprocess.check_call(['sudo', 'apt', 'install', f'python3-{package}', '-y'])
                        print(f"\n{colours.dark_green}[+]{colours.reset}{colours.green} Requerimientos instalados exitosamente.{colours.reset}\n")
                    else:
                        print(f"{colours.red}[-] {colours.reset}{colours.gray}La distribución {colours.reset}{colours.light_blue}'{os_name}'{colours.reset}{colours.gray} no está soportada. Instala el paquete {colours.reset}{colours.light_blue}'{package}'{colours.reset}{colours.gray} manualmente.{colours.reset}")
            else:
                subprocess.check_call(['pip', 'install', package])
                print(f"\n{colours.dark_green}[+]{colours.reset}{colours.green} Requerimientos instalados exitosamente.{colours.reset}\n")
    except subprocess.CalledProcessError as error:
        print(f"\n{colours.red}[!] {colours.reset}{colours.gray}Error al instalar requerimientos: {colours.reset}{colours.light_red}{error}{colours.reset}")

def ipaddress(host_url,character,colours):
    """
    Obtiene la dirección IP de una URL o dirección y la muestra.

    Parámetros:
    - host_url (str): URL o dirección a analizar.
    - character (str): Conjunto de caracteres para mostrar progreso.
    - colours (Colours): Objeto para colorear texto.

    Retorna:
    - str: Dirección IP obtenida.
    """
    parsed_url = urlparse(host_url)
    if parsed_url.netloc:
        host = parsed_url.netloc
    else:
        host = parsed_url.path
    try:
        ip_address = socket.gethostbyname(host)
        p1 = log.progress(f"{colours.blue}IP{colours.reset}")
        for _ in character:
            p1.status(f"{colours.gray}Iniciando búsqueda {colours.reset}{colours.red}{_}{colours.reset}")
            sleep(0.05)
        if ip_address:
            p1.success(f"{colours.gray}La dirección IP de {colours.reset}{colours.light_yellow}{host}{colours.reset}{colours.gray} es: {colours.reset}{colours.yellow}{ip_address}{colours.reset}")
            return ip_address
        else:
            print(f"{colours.red}[-]{colours.reset}{colours.gray}No se encontró una dirección IP para {colours.reset}{colours.light_yellow}{host}{colours.reset}")
    except Exception as error:
        print(f"{colours.red}[!] {colours.reset}{colours.gray}ERROR al obtener la dirección IP: {colours.reset}{colours.light_red}{str(error)}{colours.reset}")

def publicip(colours,character):
    """
    Obtiene y muestra la dirección IP pública del sistema.

    Parámetros:
    - colours (Colours): Objeto para colorear texto.
    - character (str): Conjunto de caracteres para mostrar progreso.

    Retorna:
    - str: Dirección IP pública obtenida.
    """
    p1 = log.progress(f"{colours.blue}IP Pública{colours.reset}")
    for _ in character:
        p1.status(f"{colours.gray}Iniciando búsqueda {colours.reset}{colours.red}{_}{colours.reset}")
        sleep(0.05)
    public_ip = requests.get("https://ipinfo.io/ip").text.strip()
    p1.success(f"{colours.gray}La IP pública es {colours.reset}{colours.yellow}{public_ip}{colours.reset}")
    return public_ip

if __name__ == "__main__":
    colours = Colours()
    args = get_argument()
    character = string.hexdigits + string.punctuation
    
    if args.requeriment:
        install_requeriments(colours)
    elif args.host:
        banner()          
        host_url = args.host
        if not host_url.isdigit():
            ipaddress(host_url,character,colours)
    else:
        banner()
        publicip(colours,character)
