import traceback, sys, re, argparse


"""
        Supported Instructions and their Opcodes
                |           |   Opcode  |   Opcode
        Type    |   Ins     |   /Funct  |   /Funct
                |           |   (Hex)   |   (Binary)
    ------------|-----------|-----------|------------
        R       |   AND     |   0/24    |   000000/100100
        R       |   OR      |   0/25    |   000000/100101
        R       |   NOR     |   0/27    |   000000/100111
        R       |   ADD     |   0/20    |   000000/100000
        R       |   SUB     |   0/22    |   000000/100010
        R       |   SLT     |   0/2A    |   000000/101010
        I       |   ADDI    |   8/-     |   001000/------
        R       |   DIV     |   0/1A    |   000000/011010
        R       |   MULT    |   0/18    |   000000/011000
        I       |   LW      |   23/-    |   100011/------
        I       |   SW      |   2B/-    |   101011/------
        R       |   MFHI    |   0/10    |   000000/001010
        R       |   MFLO    |   0/12    |   000000/001100
        R       |   BEQ     |   4/-     |   000100/------
        J       |   J       |   2/-     |   000010/------
"""

"""
// R-Type (integer arithmetic, bitwise operations, compare instructions: slt,sgt etc.)
            // 31...26 25...21 20...16 15...11 10...6 5...0
            // 6 bits  5 bits  5 bits  5 bits  5 bits 6 bits
            // Opcode  Rs      Rt      Rd      Shamt  funct
/ J-Type (Jump/Call)
            // 31...26 25...0
            // Opcode  Const
 // I-Type (Load/Store/Branch (Conditonal))
            // 31...26 25...21 20...16 15...0
            // 6 bits  5 bits  5 bits  16 bits
            // Opcode  Rs      Rt      Immediate
"""

supportedInstructions = {
    # R TYPE INSTRUCTIONS
    "AND" : {
        "Opcode" : 0x0,
        "Funct" : 0x24,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "OR" : {
        "Opcode" : 0x0,
        "Funct" : 0x25,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "NOR" : {
        "Opcode" : 0x0,
        "Funct" : 0x27,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "ADD" : {
        "Opcode" : 0x0,
        "Funct" : 0x20,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "SUB" : {
        "Opcode" : 0x0,
        "Funct" : 0x22,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "SLT" : {
        "Opcode" : 0x0,
        "Funct" : 0x2A,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "DIV" : {
        "Opcode" : 0x0,
        "Funct" : 0x1A,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "MULT" : {
        "Opcode" : 0x0,
        "Funct" : 0x18,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "MFHI" : {
        "Opcode" : 0x0,
        "Funct" : 0x10,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "MFLO" : {
        "Opcode" : 0x0,
        "Funct" : 0x12,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    "BEQ" : {
        "Opcode" : 0x4,
        "Funct" : None,
        "Type" : "R",
        "inputCount" : 3 # Takes in Rs, Rt, Rd
    },
    # I TYPE INSTRUCTIONS
    "ADDI" : {
        "Opcode" : 0x8,
        "Funct" : None,
        "Type" : "I",
        "inputCount" : 3 # Takes in Rt, Rs, Immediate
    },
    "LW" : {
        "Opcode" : 0x23,
        "Funct" : None,
        "Type" : "I",
        "hasOffset" : True,
        "inputCount" : 3 # Takes in  RegDest, Offset, RegSource,
    },
    "SW" : {
        "Opcode" : 0x2B,
        "Funct" : None,
        "Type" : "I",
        "hasOffset" : True,
        "inputCount" : 3 # Takes in  RegDest, Offset, RegSource,
    },
    # J TYPE INSTRUCTIONS
    "J" : {
        "Opcode" : 0x2,
        "Funct" : None,
        "Type" : "J",
        "inputCount" : 1 # Takes in Destination Address
    }
}

registers = {
    "$ZERO" : 0,    # The Constant Value 0
    "$0" : 0,       # The Constant Value 0
    "$AT" : 1,      # Assembler Temporary
    "$V0" : 2,      # Value for Function Results and Expression Evaluation
    "$V1" : 3,      # Value for Function Results and Expression Evaluation
    "$A0" : 4,      # Argument
    "$A1" : 5,      # Argument
    "$A2" : 6,      # Argument
    "$A3" : 7,      # Argument
    "$T0" : 8,      # Temporary
    "$T1" : 9,      # Temporary
    "$T2" : 10,     # Temporary
    "$T3" : 11,     # Temporary
    "$T4" : 12,     # Temporary
    "$T5" : 13,     # Temporary
    "$T6" : 14,     # Temporary
    "$T7" : 15,     # Temporary
    "$S0" : 16,     # Saved Temporary
    "$S1" : 17,     # Saved Temporary
    "$S2" : 18,     # Saved Temporary
    "$S3" : 19,     # Saved Temporary
    "$S4" : 20,     # Saved Temporary
    "$S5" : 21,     # Saved Temporary
    "$S6" : 22,     # Saved Temporary
    "$S7" : 23,     # Saved Temporary
    "$T8" : 24,     # Temporary
    "$T9" : 25,     # Temporary
    "$K0" : 26,     # Reservered for OS Kernel
    "$K1" : 27,     # Reservered for OS Kernel
    "$GP" : 28,     # Global Pointer
    "$SP" : 29,     # Stack Pointer
    "$FP" : 30,     # Frame Pointer
    "$RA" : 31      # Return Address
}

def mipsToMachineCode(instructionsList):
    def getInputs(string, type, hasOffset=False):
            if type.upper() == "R":
                matches = re.findall(r'\$[A-Za-z0-9]+', string)
                return matches
            elif type.upper() == "I":
                if hasOffset: # if SW or LW
                    matches = re.findall(r'\$[A-Za-z0-9]+|[0-9]+|\(\$[A-Za-z0-9]+\)', string)
                    if len(matches) == 3:
                        Rt = matches[0]
                        offset = matches[1]
                        Rs = matches[2][1:-1]  # Exclude the parentheses from the offset
                        
                        #print("Rt:", Rt)
                        #print("Rs:", Rs)
                        #print("Offset:", offset)
                        return [Rt, offset, Rs]
                    else:
                        #print("Invalid instruction format")
                        return None
                else: # If ADDI
                    matches = re.findall(r'\$[A-Za-z0-9]+|[0-9]+', string)
                    if len(matches) == 3:
                        dest_register = matches[0]
                        source_register = matches[1]
                        immediate_value = matches[2]
                        
                        #print("Destination Register:", dest_register)
                        #print("Source Register:", source_register)
                        #print("Immediate Value:", immediate_value)
                        return [dest_register, source_register, immediate_value]
                    else:
                        #print("Invalid instruction format")
                        return None
            elif type.upper() == "J":
                return [string[2:]]
            else:
                print("Invalid type!")
                return None

                    


    # sample element in instructionsList: DIV r1, r2, r3
    hexInstructions = []
    for instructionString in instructionsList:
        match = re.match(r'^\w+', instructionString)
        if match:
            cmd = match.group(0).upper()
        try:
            cmd_dict = supportedInstructions[cmd]
        except KeyError as e:
            # Unsupported instruction
            badIns = "".join(traceback.format_exception_only(e)).strip()[10:]
            print(f"ERROR: {badIns} is not a supported instruction!")
            sys.exit(-1)
        opcode = hex(cmd_dict["Opcode"])
        if cmd_dict['Funct'] is not None:
            funct = hex(cmd_dict['Funct'])
        numInputs = int(cmd_dict["inputCount"])
        type = cmd_dict["Type"]
        if cmd == "SW" or cmd == "LW":
            matches = getInputs(instructionString, type, True)
            assert len(matches) == numInputs, f"{instructionString} does not have the required {numInputs} inputs!"
            destReg = matches[0]
            offset = matches[1]
            sourceReg1 = matches[2]
            sourceReg2 = None
            immediate = None
        else:
            matches = getInputs(instructionString, type, False)
            assert len(matches) == numInputs, f"{instructionString} does not have the required {numInputs} inputs!"
            if type.upper() != "J":
                destReg = matches[0]
                sourceReg1 = matches[1]
                sourceReg2 = None
                immediate = None
                if matches[2][0] == "$":
                    # Third input is a register, not an immediate
                    sourceReg2 = matches[2]
                    immediate = None
                else:
                    sourceReg2 = None
                    immediate = matches[2]
            else:
                destReg = None
                sourceReg1 = None
                sourceReg2 = None
                immediate = matches[0]
        # Make sure the amount of inputs passed actually line of with expected amount
        
        destRegNum = registers[destReg.upper()] if destReg is not None else None
        sourceReg1Num = registers[sourceReg1.upper()] if sourceReg1 is not None else None
        sourceReg2Num = registers[sourceReg2.upper()] if sourceReg2 is not None else None
        
        #print(f"""{instructionString} has these inputs:\n
        #Destination:{destReg} [{destRegNum}]\n
        #SourceReg1: {sourceReg1} [{sourceReg1Num}]\n
        #SourceReg2: {sourceReg2} [{sourceReg2Num}]\n
        #Immediate: {immediate}\n""")

        if type.upper() == "R":
            # 31...26 25...21 20...16 15...11 10...6 5...0
            # 6 bits  5 bits  5 bits  5 bits  5 bits 6 bits
            # Opcode  Rs      Rt      Rd      Shamt  funct
            opcode_binary = format(int(opcode, 16), f'0{6}b')
            if cmd == "DIV":
                rd_binary = "00000"
            else:
                rd_binary = format(int(hex(destRegNum), 16), f'0{5}b')

            rs_binary = format(int(hex(sourceReg1Num), 16), f'0{5}b')
            rt_binary = format(int(hex(sourceReg2Num), 16), f'0{5}b')
            #shamt_binary = format(int(0x0, 16), f'0{5}b') # No functions with shamt are supported yet
            shamt_binary = '00000'
            funct_binary = format(int(funct, 16), f'0{5}b')
            #print(instructionString)
            machinecode = "" + opcode_binary + rs_binary + rt_binary + rd_binary + shamt_binary + funct_binary
            #print(machinecode)
            decimal_value = int(machinecode, 2)
            hex_value = format(decimal_value, '08x')
            hexInstructions.append(hex_value)
            #print(hex_value)
        elif type.upper() == "I":
            # 31...26 25...21 20...16 15...0
            # 6 bits  5 bits  5 bits  16 bits
            # Opcode  Rs      Rt      Immediate
            opcode_binary = format(int(opcode, 16), f'0{6}b')
            rs_binary = format(int(hex(sourceReg1Num), 16), f'0{5}b')
            if sourceReg2Num is not None:
                rt_binary = format(int(hex(sourceReg2Num), 16), f'0{5}b')
            else:
                rt_binary = "00000"
            if immediate is not None:
                immediate_binary = format(int(immediate, 10), f'0{16}b')
            else:
                immediate_binary = format(int(offset, 10), f'0{16}b')
            machinecode = "" + opcode_binary + rs_binary + rt_binary + immediate_binary
            #print(instructionString)
            #print(machinecode)
            decimal_value = int(machinecode, 2)
            hex_value = format(decimal_value, '08x')
            hexInstructions.append(hex_value)
            #print(hex_value)
        elif type.upper() == "J":
            # 31...26 25...0
            # Opcode  Const
            opcode_binary = format(int(opcode, 16), f'0{6}b')
            try:
                immediate_binary = format(int(immediate, 10), f'0{16}b')
            except ValueError as e:
                print(f"\nWARNING: Label {immediate} is not supported! Please use the hex address of the label's location!")
                print(f"\t Using FFFF as filler! Replace as necessary!\n")
                immediate_binary = immediate_binary = format(int("65535", 10), f'0{16}b')
            machinecode =  opcode_binary + immediate_binary
            #print(instructionString)
            #print(machinecode)
            decimal_value = int(machinecode, 2)
            hex_value = format(decimal_value, '08x')
            hexInstructions.append(hex_value)
            #print(hex_value)
        else:
            print("You shouldn't have made it this far without an error")
    return hexInstructions
        

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='MIPS Compiler')
    parser.add_argument('readFile', type=str, nargs='?', default='MIPSProgram.txt', help='Input file path')
    parser.add_argument('writeFile', type=str, nargs='?', default='Program.txt', help='Output file path')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the file paths
    readFile = args.readFile
    writeFile = args.writeFile
    with open(readFile, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    commands = lines

    print(f"Compiling {readFile} into machine code...")
    print(f"Compiled to {writeFile}!")
    instructions = mipsToMachineCode(commands)

    with open(writeFile, "w") as file:
        for instruction in instructions:
            file.write(instruction + "\n")
            file.write("0\n0\n0\n")

        # Fill the rest of the file with the pattern
        remaining_lines = 256 - len(instructions) * 4  # Subtracting the number of lines used by instructions
        pattern = "F0000000\n0\n0\n0\n"
        file.write(pattern * remaining_lines)