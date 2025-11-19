from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from m5.objects import X86O3CPU 
from m5.objects.FuncUnit import *
from components.FuncUnitConfig import *
from m5.objects.FUPool import *
 
"""
Single-issue single-core processor
"""
class VariableBPSingleIssueCore(BaseCPUCore):
    def __init__(self,bp):
        super().__init__(X86O3CPU(), ISA.X86)
        # Specify branch predictor, passed from instantiation of this class
        self.core.branchPred = bp

        # Constrain pipeline width
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

class VariableBPSingleIssueProcessor(BaseCPUProcessor):
    def __init__(self,bp):
        # Single-core system, but BaseCPUProcessor expects list of cores
        cores = [VariableBPSingleIssueCore(bp) for _ in range(1)]
        super().__init__(cores)


"""
Multiple-issue Out-of-order single-core processor
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
Smaller out-of-order processor with varying branch predictor and branch misprediction penalty
"""
class VariableO3Core(BaseCPUCore):
    def __init__(self, predictor, penalty):
        super().__init__(X86O3CPU(), ISA.X86)

        # We have a somewhat less wide pipeline than default
        self.core.fetchWidth=4
        self.core.decodeWidth=4
        self.core.issueWidth=4
        self.core.commitWidth=4

        # Specify branch predictor, passed from instantiation of this class
        self.core.branchPred = predictor

        """
        Implementation note, branch misprediction penalty:

        There is no one parameter to set a misprediction penalty latency, so we have to get a bit creative.
        When a misprediction is noticed, several pipeline stages are messaged, and many things happen.
        One of these is that the Commit stage squashes all instructions in the re-order buffer (ROB).
        The ROB squashes several instructions at a time, controlled by the `squashWidth` parameter passed.
        As such, we scale squashWidth by our misprediction penalty, so that a higher penalty means that
        less instructions can be squashed at once, and squashing thus takes longer.

        NOTE: Squashes do not only occur due to mispredictions, but it is one source of them! Since we only
        have one squashing unit, we have to live with this. This is a consideration you might have to consider 
        when designing a real CPU as well. While this way of handling misprediction penalties is not perfect,
        it is the best that we have found. Other ways could be to work with the various delay parameters, however
        these are slightly finicky, and can lead to the simulator hanging due to (as of now) unknown reasons.
        """
        self.core.squashWidth = 8//penalty

class VariableO3Processor(BaseCPUProcessor):
    def __init__(self, predictor, penalty):
        cores = [VariableO3Core(predictor, penalty) for _ in range(1)]
        super().__init__(cores)

# Helper class to configure the functional units
class Lab2FUPool(FUPool):
    FUList = [
        IntALU(),
        IntMultDiv(),
        FP_ALU(),
        FP_MultDiv(),
        ReadPort(),
        SIMD_Unit(),
    #    Matrix_Unit(),
        PredALU(),
        WritePort(),
        RdWrPort(),
        IprPort(),
        ]


"""Variable pipeline width O3 processor
"""

class VariableWidthO3Core(BaseCPUCore):
    
    def __init__(self, predictor, fetchWidth, decodeWidth, renameWidth, issueWidth, commitWidth):
        super().__init__(X86O3CPU(), ISA.X86)
        # Choose pipeline width for each stage
        self.core.fetchWidth=fetchWidth
        self.core.decodeWidth=decodeWidth
        self.core.renameWidth=renameWidth
        self.core.dispatchWidth = issueWidth
        self.core.issueWidth=issueWidth
        self.core.wbWidth = issueWidth
        self.core.commitWidth=commitWidth
        self.core.squashWidth = commitWidth
	# Limit the size of ROB and instruction queue depth 
        if commitWidth == 1:
            self.core.numROBEntries=8
            self.core.numIQEntries=4
            self.core.numPhysIntRegs=64
            self.core.numPhysFloatRegs=64
        # Specify branch predictor, passed from instantiation of this class
        self.core.branchPred = predictor
        self.core.fuPool = Lab2FUPool()


class VariableWidthO3Processor(BaseCPUProcessor):
    def __init__(self,num_cores, predictor, fetchWidth, decodeWidth, renameWidth, issueWidth, commitWidth):
        # Single-core system, but BaseCPUProcessor expects list of cores
        cores = [VariableWidthO3Core(predictor, fetchWidth, decodeWidth, renameWidth, issueWidth, commitWidth)for _ in range(num_cores)]
        super().__init__(cores)

