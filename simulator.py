memory = [0]*32

def binary_representation(n):
    binary_string = bin(n)[2:]  
    padded_binary_string = binary_string.zfill(32)
    return ("0b" + padded_binary_string)

def display_values(num, dict):
    print("0b" + format(num, '032b'), end = " ")
    for i in dict:
        print("0b" + format(dict[i], '032b'), end = " ")
    print("\n")

def sign_extend_binary(binary_str, total_bits):
    value = int(binary_str, 2)
    if value & (1 << (total_bits - 1)):
        value -= 1 << total_bits
    return value

opcode_mappings = {'ra' : '00001', 'sp' : '00010', 'gp' : '00011', 'tp' : '00100', 't0' : '00101', 't1' : '00110', 't2' : '00111', 
            's0' : '01000', 'fp' : '01000', 's1' : '01001', 'a0' : '01010', 'a1' : '01011', 'a2' : '01100', 'a3' : '01101', 
            'a4' : '01110', 'a5' : '01111', 'a6' : '10000', 'a7' : '10001', 's2' : '10010', 's3' : '10011', 's4' : '10100', 
            's5' : '10101', 's6' : '10110', 's7' : '10111', 's8' : '11000', 's9' : '11001', 's10': '11010', 's11' :'11011', 
            't3' : '11100', 't4' : '11101', 't5' : '11110', 't6' : '11111'}

reverse_opcode_mappings = {v: k for k, v in opcode_mappings.items()}

registers = {'ra' : 0, 'sp' : 0, 'gp' : 256, 'tp' : 0, 't0' : 0, 't1' : 0, 't2' : 0, 's0' : 0,'fp' : 0, 's1' : 0, 'a0' : 0, 'a1' : 0,
             'a2': 0, 'a3' : 0, 'a4' : 0, 'a5' : 0, 'a6' : 0, 'a7' : 0, 's2' : 0, 's3' : 0, 's4' : 0, 's5' : 0, 's6' : 0,
             's7' : 0, 's8' : 0, 's9' : 0, 's10' : 0, 's11' : 0, 't3' : 0, 't4' : 0, 't5' : 0, 't6' : 0}

PC = 0

def custom_shift_left(value, shift):
    shift_amount = shift & 0x1F  
    return value << shift_amount

def custom_shift_right(value, shift):
    shift_amount = shift & 0x1F  
    return value >> shift_amount

def instruction_stats(PC, binary_list):
    for instruction in binary_list:
        z = True
        opcode = instruction[25:32]
        
        if (opcode == '0110011'): 
            if(instruction[17:20] == '000'):
                if(instruction[0:7] == '0000000'): 
                    for j in reverse_opcode_mappings:
                        if instruction[20:25] == j:
                            for k in reverse_opcode_mappings:
                                if instruction[12:17] == k:
                                    for l in reverse_opcode_mappings:
                                        if instruction[7:12] == l:
                                            registers[reverse_opcode_mappings[j]] = registers[reverse_opcode_mappings[k]] + registers[reverse_opcode_mappings[l]]
                    PC += 4
                    display_values(PC, registers)          

                elif(instruction[0:7] == '0100000'):
                    for j in reverse_opcode_mappings:
                        if instruction[20:25] == j:
                            for k in reverse_opcode_mappings:
                                if instruction[12:17] == k:
                                    for l in reverse_opcode_mappings:
                                        if instruction[7:12] == l:
                                            registers[reverse_opcode_mappings[j]] = registers[reverse_opcode_mappings[k]] - registers[reverse_opcode_mappings[l]]
                    PC += 4
                    display_values(PC, registers)
                else:
                    z = False
                    
            elif(instruction[17:20] == '001'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                for l in reverse_opcode_mappings:
                                    if instruction[7:12] == l:
                                        registers[reverse_opcode_mappings[j]] = custom_shift_left(registers[reverse_opcode_mappings[k]], registers[reverse_opcode_mappings[l]])
                PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '010'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                for l in reverse_opcode_mappings:
                                    if instruction[7:12] == l:
                                        registers[reverse_opcode_mappings[j]] = 1 if registers[reverse_opcode_mappings[k]] < registers[reverse_opcode_mappings[l]] else 0
                PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '011'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                for l in reverse_opcode_mappings:
                                    if instruction[7:12] == l:
                                        registers[reverse_opcode_mappings[j]] = 1 if (abs(registers[reverse_opcode_mappings[k]]) < abs(registers[reverse_opcode_mappings[l]])) else 0
                PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '100'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                for l in reverse_opcode_mappings:
                                    if instruction[7:12] == l:
                                        registers[reverse_opcode_mappings[j]] = registers[reverse_opcode_mappings[k]] ^ registers[reverse_opcode_mappings[l]]
                PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '101'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                for l in reverse_opcode_mappings:
                                    if instruction[7:12] == l:
                                        registers[reverse_opcode_mappings[j]] = custom_shift_right(registers[reverse_opcode_mappings[k]], registers[reverse_opcode_mappings[l]])
                PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '110'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                for l in reverse_opcode_mappings:
                                    if instruction[7:12] == l:
                                        registers[reverse_opcode_mappings[j]] = registers[reverse_opcode_mappings[k]] | registers[reverse_opcode_mappings[l]]
                PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '111'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                for l in reverse_opcode_mappings:
                                    if instruction[7:12] == l:
                                        registers[reverse_opcode_mappings[j]] = registers[reverse_opcode_mappings[k]] & registers[reverse_opcode_mappings[l]]
                PC += 4
                display_values(PC, registers)
            else:
                z = False

        elif (opcode == '0000011'):
            for j in reverse_opcode_mappings:
                if instruction[20:25] == j:
                    for k in reverse_opcode_mappings:
                        if instruction[12:17] == k:
                            memory[registers[reverse_opcode_mappings[k]] + sign_extend_binary(instruction[0:12], 12)] = registers[reverse_opcode_mappings[j]]
            PC += 4
            display_values(PC, registers)

        elif (opcode == '0010011'): 
            if (instruction[17:20] == '000'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                registers[reverse_opcode_mappings[j]] = registers[reverse_opcode_mappings[k]] + sign_extend_binary(instruction[0:12], 12)
                PC += 4
                display_values(PC, registers)

            elif (instruction[17:20] == '011'):
                for j in reverse_opcode_mappings:
                    if instruction[20:25] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[12:17] == k:
                                registers[reverse_opcode_mappings[j]] = 1 if abs(registers[reverse_opcode_mappings[k]]) < abs(sign_extend_binary(instruction[0:12], 12)) else 0
                PC += 4
                display_values(PC, registers)
            else:
                z = False

        elif (opcode == '1100111'):
            for j in reverse_opcode_mappings:
                if instruction[20:25] == j:
                    for k in reverse_opcode_mappings:
                        if instruction[12:17] == k:
                            temp = PC + 4
                            target = (registers[reverse_opcode_mappings[k]] + sign_extend_binary(instruction[0:12], 12)) & ~1
                            registers[reverse_opcode_mappings[j]] = temp
                            PC = target
                            display_values(PC, registers)

        elif (opcode == '0100011'):
            for j in reverse_opcode_mappings:
                if instruction[12:17] == j:
                    for k in reverse_opcode_mappings:
                        if instruction[7:12] == k:
                            imm = instruction[0:7] + instruction[20:25]
                            memory[registers[reverse_opcode_mappings[j]] + sign_extend_binary(imm, 12)] = registers[reverse_opcode_mappings[k]]
            PC += 4
            display_values(PC, registers)

        elif (opcode == '1100011'):
            imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + "0"
            offset = sign_extend_binary(imm, 13)
            
            if(instruction[17:20] == '000'):
                for j in reverse_opcode_mappings:
                    if instruction[12:17] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[7:12] == k:
                                if registers[reverse_opcode_mappings[j]] == registers[reverse_opcode_mappings[k]]:
                                    PC = PC + offset
                                else:
                                    PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '001'):
                for j in reverse_opcode_mappings:
                    if instruction[12:17] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[7:12] == k:
                                if registers[reverse_opcode_mappings[j]] != registers[reverse_opcode_mappings[k]]:
                                    PC = PC + offset
                                else:
                                    PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '100'):
                for j in reverse_opcode_mappings:
                    if instruction[12:17] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[7:12] == k:
                                if registers[reverse_opcode_mappings[j]] < registers[reverse_opcode_mappings[k]]:
                                    PC = PC + offset
                                else:
                                    PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '101'):
                for j in reverse_opcode_mappings:
                    if instruction[12:17] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[7:12] == k:
                                if registers[reverse_opcode_mappings[j]] >= registers[reverse_opcode_mappings[k]]:
                                    PC = PC + offset
                                else:
                                    PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '110'):
                for j in reverse_opcode_mappings:
                    if instruction[12:17] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[7:12] == k:
                                if abs(registers[reverse_opcode_mappings[j]]) < abs(registers[reverse_opcode_mappings[k]]):
                                    PC = PC + offset
                                else:
                                    PC += 4
                display_values(PC, registers)

            elif(instruction[17:20] == '111'):
                for j in reverse_opcode_mappings:
                    if instruction[12:17] == j:
                        for k in reverse_opcode_mappings:
                            if instruction[7:12] == k:
                                if abs(registers[reverse_opcode_mappings[j]]) >= abs(registers[reverse_opcode_mappings[k]]):
                                    PC = PC + offset
                                else:
                                    PC += 4
                display_values(PC, registers)
            else:
                z = False

        elif (opcode == '0110111'):
            for j in reverse_opcode_mappings:
                if instruction[20:25] == j:
                    imm = instruction[0:20] + "000000000000"
                    registers[reverse_opcode_mappings[j]] = sign_extend_binary(imm, 32)
            PC += 4
            display_values(PC, registers)

        elif (opcode == '0010111'):
            for j in reverse_opcode_mappings:
                if instruction[20:25] == j:
                    imm = instruction[0:20] + "000000000000"
                    registers[reverse_opcode_mappings[j]] = PC + sign_extend_binary(imm, 32)
            PC += 4
            display_values(PC, registers)

        elif (opcode == '1101111'):
            for j in reverse_opcode_mappings:
                if instruction[20:25] == j:
                    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + "0"
                    temp = PC + 4
                    PC = PC + sign_extend_binary(imm, 21)
                    registers[reverse_opcode_mappings[j]] = temp
            display_values(PC, registers)
        else:
            z = False

        if(z == False):
            print("Instruction Error")
            return

def generate_hexadecimal(start='1000', step=4, count=32):
    current_hex = int(start, 16)
    hex_list = []
    for _ in range(count):
        hex_value = hex(current_hex)[2:].zfill(4)
        hex_list.append('0x' + '000' + hex_value + ':')
        current_hex += step
    return hex_list

def main():
    try:
        file_path = "input.txt"
        with open(file_path, "r") as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]
        instruction_stats(PC, lines)
        for i in range(32):
            print(generate_hexadecimal()[i] + format(memory[i], '032b'))

        with open('output.txt', 'w') as file:
            for i in range(32):
                file.write(f"{generate_hexadecimal()[i]} {format(memory[i], '032b')}\n")
            
    except FileNotFoundError:
        print("Error: input.txt file not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
