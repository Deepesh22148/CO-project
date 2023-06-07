from Memory import MEM
from ProgramCounter import PC
from RegisterWorking import RF
from ExecutionStage import EE

MEM.initialize()
PC.initialize()
halted = False

while not halted and PC.getValue()< len(MEM.binary_data):
    binary_line = MEM.getData(PC.getValue())
    halted,newPC = EE.execute(binary_line)
    PC.dump()
    RF.dump()
    PC.update(newPC)

MEM.dump()