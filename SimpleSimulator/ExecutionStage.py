from RegisterWorking import RF
from Memory import MEM, checkOverflow
from ProgramCounter import PC


class ExecutionStage:
    def execute(self, binarycode):
        opcode = binarycode[:5]
        halt, newPC = False, PC.getValue() + 1
        # add typeA binarycode
        if opcode == '00000':
            reg1 = binarycode[7:10]
            reg2 = binarycode[10:13]
            reg3 = binarycode[13:16]
            res = RF.getRegister(reg2, False) + RF.getRegister(reg3, False)
            if checkOverflow(res):
                RF.setOverflowFlag()
            else:
                RF.resetFlagRegister()
            RF.setRegister(reg1, res)
            halt, newPC = False, PC.getValue() + 1

        # sub typeA binarycode
        elif opcode == '00001':
            reg1 = binarycode[7:10]
            reg2 = binarycode[10:13]
            reg3 = binarycode[13:16]
            res = RF.getRegister(reg2, False) - RF.getRegister(reg3, False)
            if res < 0:
                RF.setOverflowFlag()
                RF.setRegister(reg1, 0)
            else:
                RF.setRegister(reg1, res)
                RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        # movi typeb binarycode
        elif opcode == "00010":
            reg1 = binarycode[6:9]  # reading address of reg1
            value = binarycode[9:]  # reading the value of $Imm
            value = int(value, 2)
            RF.setRegister(reg1, value)
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        # mov typec binarycode
        elif opcode == "00011":
            reg1 = binarycode[10:13]
            reg2 = binarycode[13:]
            RF.setRegister(reg1, RF.getRegister(reg2, False))
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        # ld typed binarycode
        elif opcode == '00100':
            reg1 = binarycode[6:9]
            memoryAddress = binarycode[9:]
            valueAtMemory = MEM.getValueFromAddress(memoryAddress)
            RF.setRegister(reg1, valueAtMemory)
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        # st typed binarycode
        elif opcode == '00101':
            reg1 = binarycode[6:9]
            memoryAddress = binarycode[9:]
            MEM.setValueOfAddress(memoryAddress, RF.getRegister(reg1, False))
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        # mul typea binarycode
        elif opcode == '00110':
            reg1 = binarycode[7:10:]
            reg2 = binarycode[10:13:]
            reg3 = binarycode[13:16:]
            res = RF.getRegister(reg2, False) * RF.getRegister(reg3, False)
            if (checkOverflow(res)):
                RF.setOverflowFlag()
            else:
                RF.resetFlagRegister()
            RF.setRegister(reg1, res)
            halt, newPC = False, PC.getValue() + 1

        elif (opcode == "00111"):
            reg3 = binarycode[10:13:]
            reg4 = binarycode[13::]
            if int(reg3, 2) == 0:
                RF.setOverflowFlag()
                RF.setRegister('000', 0)
                RF.setRegister("001", 0)
            else:
                remainder = int(RF.getRegister(reg3, False) )% 1
                quotient = int(RF.getRegister(reg3, False)) // 1
                RF.setRegister("000", quotient)
                RF.setRegister("001", remainder)
                RF.resetFlagRegister()
                halt, newPC = False, PC.getValue() + 1

        elif opcode == "01000":
            reg1 = binarycode[6:9]
            immediateValue = int(binarycode[9:], 2)
            try:
                shiftedString = '0' * immediateValue + RF.getRegister(reg1, True)[
                                                    :16 - immediateValue:]
                RF.setRegister(reg1, int(shiftedString, 2))
                RF.resetFlagRegister()
                halt, newPC = False, PC.getValue() + 1
            except TypeError:
                pass

        elif opcode == "01001":
            reg1 = binarycode[6:9]
            immediateValue = int(binarycode[9:], 2)
            shiftedString = RF.getRegister(reg1, True)[immediateValue::] + '0' * immediateValue
            RF.setRegister(reg1, int(shiftedString, 2))
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        elif opcode == "01010":
            reg1 = binarycode[7:10:]
            reg2 = binarycode[10:13:]
            reg3 = binarycode[13:16:]
            res = RF.getRegister(reg2, False) ^ RF.getRegister(reg3, False)
            RF.setRegister(reg1, res)
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        elif opcode == "01011":
            reg1 = binarycode[7:10:]
            reg2 = binarycode[10:13:]
            reg3 = binarycode[13:16:]
            res = RF.getRegister(reg2, False) | RF.getRegister(reg3, False)
            RF.setRegister(reg1, res)
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        elif opcode == "01100":
            reg1 = binarycode[7:10:]
            reg2 = binarycode[10:13:]
            reg3 = binarycode[13:16:]
            res = RF.getRegister(reg2, False) & RF.getRegister(reg3, False)
            RF.setRegister(reg1, res)
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        elif opcode == "01101":
            reg1 = binarycode[10:13:]
            reg2 = binarycode[13::]
            inverted = ""
            for bit in reg2:
                if bit == '1':
                    inverted += '0'
                else:
                    inverted += '1'
            RF.setRegister(reg1, int(inverted, 2))
            RF.resetFlagRegister()
            halt, newPC = False, PC.getValue() + 1

        elif opcode == "01110":
            reg1 = binarycode[10:13:]
            reg2 = binarycode[13::]
            if int(RF.getRegister(reg1, False)) < int(RF.getRegister(reg2, False)):
                RF.setLessThanFlag()
            elif int(RF.getRegister(reg1, False)) > int(RF.getRegister(reg2, False)):
                RF.setGreaterThanFlag()
            else:
                RF.setEqualsFlag()
            halt, newPC = False, PC.getValue() + 1

        elif opcode == "01111":
            memoryAddress = binarycode[9:]
            (halt, newPC) = (False, int(memoryAddress, 2))
            RF.resetFlagRegister()

        elif opcode == "11100":
            if RF.flagRegister == "0000000000000100":
                memoryAddress = binarycode[9:]
                halt, newPC = False, int(memoryAddress, 2)
            else:
                halt, newPC = False, PC.getValue() + 1
            RF.resetFlagRegister()

        elif opcode == "11101":
            if RF.flagRegister == "0000000000000010":
                memoryAddress = binarycode[9:]
                halt, newPC = False, int(memoryAddress, 2)
            else:
                halt, newPC = False, PC.getValue() + 1
            RF.resetFlagRegister()

        elif opcode == "11111":
            if RF.flagRegister == "0000000000000001":
                memoryAddress = binarycode[9:]
                halt, newPC = False, int(memoryAddress, 2)
            else:
                halt, newPC = False, PC.getValue() + 1
            RF.resetFlagRegister()

        # halt binarycode
        elif opcode == "10011":
            RF.resetFlagRegister()
            halt, newPC = True, PC.getValue() + 1

        return halt,newPC


EE = ExecutionStage()
