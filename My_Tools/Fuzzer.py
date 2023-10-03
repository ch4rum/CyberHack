#!/bin/python3

import signal, sys, argparse, requests
from tqdm import tqdm

__version__ = "Fuzzer 1.0"

def ctrl_c(sig, frame):
    print(f"\n\n[!] Saliendo...\n")
    sys.exit(1)
    
# Ctrl + C
signal.signal(signal.SIGINT,ctrl_c)

def argument_Parse():
    try:
        parse = argparse.ArgumentParser(prog="Fuzzer.py",
                                        description="Programa para realizar fuzzer web")
        parse.add_argument('-u',
                           metavar="< URL >",
                           default=None,
                           type=str,
                           help="Url del sitio a hacer fuzzer.")
        parse.add_argument('-d',
                           metavar="< Diccionario >",
                           default=None,
                           type=str,
                           help="Pasar diccionario")
        parse.add_argument('-v','--version',
                           action='version',
                           version=f'Fuzzer.py {__version__.split()[1]}')
        if len(sys.argv) == 1:
            parse.print_help()
            sys.exit(1)
        
        return parse.parse_args()
    except argparse.ArgumentError:
        print("Error de argumentos")
    
def open_archives(archive):
    try:
        with open(archive, "r") as file:
            dicc = file.read().splitlines()
        if not dicc:
            print("El diccionario esta vacio.")
        return dicc
    except FileNotFoundError:
        print("El diccionario no fue encontrado.")
        
def fuzzer(url, dicc):
    if not dicc:
        return 
    p1= tqdm(total=len(dicc), desc="Progreso", unit="urls", dynamic_ncols=True)
    for word in dicc:
        new_url = url + word
        response = requests.get(new_url)
        if response.status_code == 200:
            tqdm.write(f"[+] {new_url} Ok")
        p1.update(1)
    p1.close()

if __name__ == "__main__":
    arg = argument_Parse()
    archive =open_archives(arg.d)
    if archive:
        fuzzer(arg.u, archive)
