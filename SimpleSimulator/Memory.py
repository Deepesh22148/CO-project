from sys import stdin


class Memory:
    binary_data = []

    def initialize(self):
        for i in stdin:
            line = i[:16]
            self.binary_data.append(line)
        c = 128 - len(self.binary_data)
        if c >= 0:
            for i in range(c):
                self.binary_data.append("0" * 16)

    def getData(self, currentPC):
        return self.binary_data[currentPC]

    def dump(self):
        for i in self.binary_data:
            print(i)

    def setValueOfAddress(self, Address, val):
        self.binary_data[int(Address, 2)] = format(int(val),"016b")

    def getValueFromAddress(self, address):
        return self.binary_data[int(address, 2)]


def checkOverflow(val):
    if (int(val) > (2 ** 16 - 1)):
        return True
    else:
        return False


MEM = Memory()
