from components.bp_processors import VariableWidthO3Processor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from m5.objects import TournamentBP
from components.memories import MultiChannelDDR4_2400

from m5.objects import StaticBP, LocalBP
#from gem5.components.memory import ChanneledMemory
#from gem5.components.dram_interfaces.ddr4 import DDR4_2400_8x8


# L1D and L1I, unified L2
# L1D and L1I will have associativity 8, L2 will have associativity 4
#cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
#        l1d_size='16kB',
##        l1i_size='16kB',
#        l2_size='256kB',
#)
cache_hierarchy = NoCache()
# A possibly multi channel memory system using DDR4_2400_8x8 based DIMM with an address space of 4GB
memory = MultiChannelDDR4_2400(4, size='16GiB')

pw = 4
# Processor
processor = VariableWidthO3Processor(
        predictor = LocalBP(), 
        penalty = 1,
        fetchWidth= pw,
        decodeWidth= pw,
        renameWidth = pw,
        issueWidth = pw,
        commitWidth = pw
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
