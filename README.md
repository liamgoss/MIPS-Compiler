# MIPS-Compiler
This project is a quick compiler for MIPS program written in Python. It takes in an input .txt file of mips instructions, converts them to machine code (represented in hex), and writes them to a file.

## Supported MIPS Instructions
- Arithmetic/Logic
    - AND, OR, NOR, ADD, SUB, SLT, ADDI, DIV, MULT
- Data Movement
    - LW, SW, MFHI, MFLO
- Flow Control
    - BEQ, J


## Usage
python3 compile.py textFileWithMIPSInstruction.txt textFileForMachineCode.txt

The program write the machine code for the instructions in hex. The reason for this is for use in my "MIPS 32 Bit Processor" project written in Verilog that was designed to take in hex instructions. This functionality can be changed to binary by editing the code.

## Future Work
I plan on setting mode options such as an option setting the output machine code to be hex or binary. I also want to support labels better but I am unsure of how to do that currently.
