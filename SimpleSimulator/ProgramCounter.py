class Program_counter:
    currentCounter = 0

    def initialize(self):
        self.currentCounter = 0

    def getValue(self):
        return self.currentCounter

    def update(self, newCounter):
        self.currentCounter = newCounter

    def dump(self):
        t = format(self.currentCounter, '07b')
        print(t, end=" ")


PC = Program_counter()
