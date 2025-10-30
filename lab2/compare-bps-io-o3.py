from components.bp_processors import VariableBPInOrderProcessor, VariableBPO3Processor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

from m5.objects import TournamentBP, BiModeBP
"""
TournamentBP -> tournament
Parameters: (leave these at default values, i.e. don't specify any)
    - localPredictorSize: unsigned. Number of n-bit counters in local table.
    - localCtrBits: unsigned. n, number of bits in local saturation counters.
    - localHistoryTableSize: unsigned. Number of local historical branch decisions recorded.
    - globalPredictorSize: unsigned. Number of n-bit counters in global table.
    - globalCtrBits: unsigned. n, number of bits in global saturation counters.
    - choicePredictorSize: unsigned. Number of n-bit counters in choice predictor.
    - choiceCtrBits: unsigned. n, number of bits in choice predictor saturation counters.
BiModeBP -> bimode
Parameters: (leave these at default values, i.e. don't specify any)
    - globalPredictorSize: unsigned. Number of n-bit counters in global table.
    - globalCtrBits: unsigned. n, number of bits in global saturation counters.
    - choicePredictorSize: unsigned. Number of n-bit counters in choice predictor.
    - choiceCtrBits: unsigned. n, number of bits in choice predictor saturation counters.

"""

# L1D and L1I, unified L2
# L1D and L1I will have associativity 8, L2 will have associativity 4
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size='16kB',
        l1i_size='16kB',
        l2_size='256kB',
)

# Memory
memory = SingleChannelDDR4_2400(size='4GB')

# Processor
#
# In-order Processor: VariableBPInOrderProcessor
# Out-of-order Processor: VariableBPO3Processor
processor = VariableBPInOrderProcessor(
        bp = INSERT_BP_HERE()
)

# Set up the board, connect all the components together
board = SimpleBoard(
        clk_freq='3GHz',
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy
)

# Sets the workload based on the --benchmark=WORKLOAD
board.set_workload(obtain_resource("x86-gapbs-bfs-run"))

simulator = Simulator(board=board)
simulator.run()
