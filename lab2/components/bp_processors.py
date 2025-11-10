from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from m5.objects import X86O3CPU 

"""
'In-order' dual-core processor

This processor will not be a TRUE in-order processor. There is a detailed in-order CPU model: MinorCPU,
but it has some severe limitations:
    - cannot run multi-threaded applications
    - branch predictor statistics are NOT recorded

There are two ways we can solve this:
    - Implement statistics recording for MinorCPU
    - Use another model, which we do and describe below

We use the more detailed out-of-order O3Core, but constrain it so much that it essentially
acts as an in-order processor. This will not emulate a true in-order processor, but for our experiments
with comparing branch predictors it is good enough!
"""
class VariableBPInOrderCore(BaseCPUCore):
    def __init__(self,bp):
        super().__init__(X86O3CPU(), ISA.X86)
        # Specify branch predictor, passed from instantiation of this class
        self.core.branchPred = bp

        # Constrain pipeline width, if width is 1 it doesn't really matter how
        # much we do in-order
        self.core.fetchWidth=1
        self.core.decodeWidth=1
        self.core.issueWidth=1
        self.core.commitWidth=1

        # Same as pipeline width, if the ROB is very small, it's hard to re-order at all
        self.core.numROBEntries=8
        self.core.numIQEntries=4

        # We can't limit these further, as there is a lower limit to how many we need.
        self.core.numPhysIntRegs=64
        self.core.numPhysFloatRegs=64

class VariableBPInOrderProcessor(BaseCPUProcessor):
    def __init__(self,bp):
        # Dual-core system, otherwise we might have problems running multithreaded benchmarks
        cores = [VariableBPInOrderCore(bp) for _ in range(2)]
        super().__init__(cores)


"""
Out-of-order single-core processor
"""
class VariableBPO3Core(BaseCPUCore):
    def __init__(self,bp):
        super().__init__(X86O3CPU(), ISA.X86)

        # Specify branch predictor, passed from instantiation of this class
        self.core.branchPred = bp

        # Leave rest of O3 settings to be default

class VariableBPO3Processor(BaseCPUProcessor):
    def __init__(self,bp):
        # Single-core system, but BaseCPUProcessor expects list of cores
        cores = [VariableBPO3Core(bp)]
        super().__init__(cores)


"""
In-order dual-core processor with varying branch penalty and branch predictor
"""
class VariableO3Core(BaseCPUCore):
    def __init__(self, predictor, penalty):
        super().__init__(X86O3CPU(), ISA.X86)

        # Specify branch predictor, passed from instantiation of this class
        self.core.branchPred = predictor

        """
        Specify the branch misprediction penalty.
        
        Implementation note:
        There is no parameter to directly set the branch penalty, so we use inter-stage delays to model the penalty instead.
        A misprediction is noticed in the Issue/Execute/Writeback (IEW) stage, which is communicated to the Commit stage.
        IEW communicates with Commit for more than just mispredictions, so we cannot use this.
        Commit will message the Fetch stage that a misprediction has happened, and new instructions need to be fetched.
        The only cases where this communication takes place is if an instruction needs to be squashed, that is if:
            - a misprediction has happened.
            - a memory order misspeculation has happened.
        Since we have an 'in-order' processor, the second case will almost 'never' happen, so we use the delay between commit and fetch to model branch misprediction penalty
        If you want to verify for yourself that this 'never' happens, check the following statistic in stats.txt:
        board.processor.cores0.core.iew.memOrderViolationEvents
        """
        self.core.commitToFetchDelay = penalty

class VariableO3Processor(BaseCPUProcessor):
    def __init__(self, predictor, penalty):
        cores = [VariableO3Core(predictor, penalty) for _ in range(2)]
        super().__init__(cores)

