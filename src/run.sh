#!/bin/bash
python3 conv.py $1 > l.json
python3 cfg1.py l.json
