# LwM2M Joulescope-Evaluation Script

Quickly hacked together script to plot a proper graph a power consumption measured using a Joulescope.

## Usage

```bash
# python3 ./src/main.py -h

usage: main.py [-h] [-o OUTPUT] [-s] [-a ADD_FILE] [-l LABEL] jls_file

plot jls files as fancy diagrams

positional arguments:
  jls_file              path to jls file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        name of resulting png file
  -s, --show            whether the created plot should be shown
  -a ADD_FILE, --add-file ADD_FILE
                        addition file
  -l LABEL, --label LABEL
                        labels for plot
```
