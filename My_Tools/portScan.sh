#!/bin/bash

# ./portScan.sh <ip-address>

#Colours
lightMagentaColour="\e[0;95m\033[1m"
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"

ctrl_c(){
    echo -e "\n\n${redColour}[!] Saliendo ...${endColour}\n"
    tput cnorm; exit 1
}

# Ctrl +C
trap ctrl_c SIGINT

declare -i counter=0
declare -a ports=($(seq 1 65535))

checkPort(){
  (exec 3<> /dev/tcp/$1/$2) 2>/dev/null

  if [ $? -eq 0 ]; then
    echo -e "${yellowColour}[+]${endColour} ${grayColour}Host ${endColour}${blueColour}$1 ${endColour}${grayColour}- Port ${endColour}${blueColour}$2 ${endColour}${grayColour}(OPEN)${endColour}"
  fi

  exec 3<&-
  exec 3>&-
}

while getopts "i:h" argument; do
  case "$argument" in
    i) ip_address=$OPTARG; let counter+=1;;
    h);;
  esac
done

# Ocultar cursor
tput civis
if [ $counter -eq 1 ];then 
  echo -e "\n${yellowColour}[+]${endColour} ${grayColour}Scaneando ip ${endColour} ${blueColour}$ip_address${endColour}${grayColour}:${endColour}\n"
  for port in ${ports[@]}; do
    checkPort $ip_address $port &
  done
else
  echo -e "\n${yellowColour}[+] Uso:${endColour}${turquoiseColour} $0 ${endColour}${yellowColour}[-i <ip?>] [-h] ${endColour}\n"
  echo -e "\t${purpleColour}-i${endColour} ${lightMagentaColour}<ip?>${endColour} ${grayColour}Ip a escanear.${endColour}"
  echo -e "\t${purpleColour}-h${endColour} \t ${grayColour}Mostrar panel de ayuda.${endColour}\n"
fi;wait

# Mostrar cursor
tput cnorm
