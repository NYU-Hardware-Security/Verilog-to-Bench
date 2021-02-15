# Verilog-to-Bench
Quick and Dirty Synthesized Verilog to Bench (NanGate 15 nm)

## Instructions: Basic

First, feed in your Verilog netlist and make it a BENCH file

```
python3 tobench.py -i INPUT_FILE -o OUTPUT_FILE 
```

Optionally, to try to preserve register names (can be useful later on to check equivalence if you go BENCH --> Verilog with abc):

```
python3 tobench.py -i INPUT_FILE -o OUTPUT_FILE --for_formal_check_reg
```

## Instructions: Seq. --> Comb.
To "get rid" of DFFs:

```
python3 pretend_scan.py -i INPUT_FILE -o OUTPUT_FILE
```

## Extra processing
Sometimes, you might want to make the port names/orders line up. You can use:
```
python3 port_reorder.py -i INPUT_FILE -o OUTPUT_FILE
```

Good luck!

