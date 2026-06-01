#!/bin/bash
echo "Compiling demo.mc to assembly..."
python3 src/main.py -S examples/demo.mc -o demo.s
echo "Assembling..."
as demo.s -o demo.o
echo "Linking..."
gcc demo.o -o demo -lc
echo "Running demo..."
./demo
echo "Exit code: $?"