from components.bp_processors import VariableInOrderProcessor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

from m5.objects import StaticBP, BiModeBP
"""
StaticBP -> taken/nottaken
Parameters:
    - predictTaken: boolean. Changes predictor from taken (true) and nottaken (false)
BiModeBP -> bimode
Parameters: (leave these at default values, i.e. don't specify any)
    - globalPredictorSize: unsigned. Number of n-bit counters in global table.
    - globalCtrBits: unsigned. n, number of bits in global saturation counters.
    - choicePredictorSize: unsigned. Number of n-bit counters in choice predictor.
    - choiceCtrBits: unsigned. n, number of bits in choice predictor saturation counters.
"""

# L1D and L1I, unified L2
# L1D and L1I will have associativity 8, L2 will have associativity 4
l1_cache_size = INSERT_L1_CACHE_SIZE_HERE
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size=l1_cache_size,
        l1i_size=l1_cache_size,
        l2_size='256kB',
)

# Memory
memory = SingleChannelDDR4_2400(size='4GB')

# Processor
processor = VariableInOrderProcessor(
        predictor = INSERT_BP_HERE,
        penalty = INSERT_MISPREDICTION_PENALTY_HERE,
)

# Set up the board, connect all the components together
board = SimpleBoard(
        clk_freq=INSERT_CLOCK_FREQUENCY_HERE,
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy
)

# Sets the workload based on the --benchmark=WORKLOAD
board.set_workload(obtain_resource("x86-gapbs-bfs-run"))

simulator = Simulator(board=board)
simulator.run()
