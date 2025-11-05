from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from m5.objects import X86O3CPU 


"""
Out-of-order single-core processor
"""
class Core(BaseCPUCore):
    def __init__(self, block_size):
        super().__init__(X86O3CPU(), ISA.X86)
        self.core.fetchWidth=2
        self.core.fetchBufferSize = block_size
        self.core.decodeWidth=2
        self.core.issueWidth=2
        self.core.commitWidth=2

        self.core.numPhysIntRegs=128
        self.core.numPhysFloatRegs=128

class Processor(BaseCPUProcessor):
    def __init__(self, block_size):
        cores = [Core(block_size=block_size)]
        super().__init__(cores)

