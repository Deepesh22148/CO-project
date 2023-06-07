from Memory import checkOverflow
class Register:
    registers = {
        "000": 0,
        "001": 0,
        "010": 0,
        "011": 0,
        "100": 0,
        "101": 0,
        "110": 0,
    }
    flagRegister = "0000000000000000"

    def resetFlagRegister(self):
        self.flagRegister = "0000000000000000"

    def setOverflowFlag(self):
        self.flagRegister = "0000000000001000"

    def setLessThanFlag(self):
        self.flagRegister = "0000000000000100"

    def setGreaterThanFlag(self):
        self.flagRegister = "0000000000000010"

    def setEqualsFlag(self):
        self.flagRegister = "0000000000000001"

    def printFlag(self):
        print(self.flagRegister, end=" ")

    def setRegister(self, registerAddress, val):
        if (not checkOverflow(val)):
            self.registers[registerAddress] = val
        else:
            rawBinary = bin(int(val))[2::]
            self.registers[registerAddress] = int(rawBinary[len(rawBinary) - 16::], 2)

    def getRegister(self, registerAddress, binaryOrDecimal):
        if binaryOrDecimal:
            if registerAddress == "111":
                return int(self.flagRegister, 2)
            rawBinary = bin(self.registers[registerAddress])[2:]
            if len(rawBinary) > 16:
                return int(rawBinary[len(rawBinary) - 16:], 2)
            else:
                return self.registers[registerAddress]
        else:
            if registerAddress == "111":
                return int(self.flagRegister, 2)
            return self.registers[registerAddress]


    def dump(self):
        for key in self.registers.keys():
            t = format(self.registers[key])
            print(t, end=" ")
        print(self.flagRegister)

RF = Register()
