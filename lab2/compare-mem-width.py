from components.bp_processors import VariableWidthO3Processor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import (
        ExitEvent,
        Simulator,
)
from m5.objects import TournamentBP
from components.memories import MultiChannelDDR4_2400
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy

from m5.objects import StaticBP, LocalBP
import m5
#from gem5.components.memory import ChanneledMemory
#from gem5.components.dram_interfaces.ddr4 import DDR4_2400_8x8
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from argparser import get_workload
import os

# L1D and L1I, unified L2
# L1D and L1I will have associativity 8, L2 will have associativity 4
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size='4kB',
        l1i_size='16kB',
        l2_size='1024kB',
)
cache_hierarchy = NoCache()
# A multi channel memory system using DDR4_2400_8x8 based DIMM with an address space of 16GB
memory = MultiChannelDDR4_2400(1, size='4GiB')

pw = 1
# Processor
processor = VariableWidthO3Processor(
		num_cores = 1,
        predictor = LocalBP(), 
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

# Sets the workload based on the --workload=WORKLOAD
board.set_se_binary_workload(obtain_resource(get_workload()), env_list=[f"LD_LIBRARY_PATH={os.environ.get('LD_LIBRARY_PATH')}"])

def workbegin_handler():
    m5.stats.reset()
    yield False
def workend_handler():
    yield False

simulator = Simulator(
        board=board,
        on_exit_event={
            ExitEvent.WORKBEGIN: workbegin_handler(),
            ExitEvent.WORKEND: workend_handler(),
        }
)

simulator.run()
