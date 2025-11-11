from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.isas import ISA
from m5.objects import X86O3CPU 

"""
'In-order' single-core processor

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
        # Single-core system, but BaseCPUProcessor expects list of cores
        cores = [VariableBPInOrderCore(bp) for _ in range(1)]
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

