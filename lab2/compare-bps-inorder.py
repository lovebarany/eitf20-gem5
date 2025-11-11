from argparser import get_workload
from components.bp_processors import VariableBPInOrderProcessor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

from m5.objects import StaticBP, LocalBP
"""
StaticBP -> taken/nottaken
StaticBP(predictTaken=True/False)
Parameters:
    - predictTaken: boolean. Changes predictor from taken (true) and nottaken (false)

LocalBP -> 2-bit local history
LocalBP()
Parameters: (leave these at default values, i.e. don't specify any) 
    - localPredictorSize: unsigned. Changes the number of entries in the n-bit counter table. Default: 2048
    - localCtrBits: unsigned. n, number of bits in the saturation counters. Keep this at 2 for this experiment!
"""
import os


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

# Sets the workload based on the --workload=WORKLOAD
board.set_se_binary_workload(obtain_resource(get_workload()), env_list=[f"LD_LIBRARY_PATH={os.environ.get('LD_LIBRARY_PATH')}"])

simulator = Simulator(board=board)
simulator.run()
