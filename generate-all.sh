#!/bin/bash

python3 src/main.py data/lwm2m/as-console-nosec/*.jls

python3 src/main.py data/lwm2m/as-console-comparison-uc/*.jls -l console -l "no console"

python3 src/main.py data/lwm2m/as-nosec-lte_m/*.jls

python3 src/main.py data/lwm2m/as-psk16/*.jls -l NoSec -l PSK16

python3 src/main.py data/lwm2m/as-psk32-comparison/*.jls -l PSK16 -l PSK32

python3 src/main.py data/lwm2m/as-x509-comparison/*.jls -l PSK32 -l x509

python3 src/main.py data/lwm2m/bs-nosec/*.jls -l "NB-IoT" -l "LTE-M"

python3 src/main.py data/lwm2m/fwu-flashswap/*.jls

python3 src/main.py data/lwm2m/fwu-pull-lte_m-1024-comparison/*.jls -l "Blocksize 1024" -l "Blocksize 512" -v 4000 -p -c

python3 src/main.py data/lwm2m/idle-comparison/*.jls -l "LTE-M" -l "NB-IoT" -f
