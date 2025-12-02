from argparser import get_workload
from components.board_variable_block_size import BoardVariableBlockSize
from components.caches import UnifiedL1L2
from components.processor import Processor
from components.memories import DualChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
import os

# Cache parameters
block_size = BLOCK_SIZE # Bytes
l1_sets = NUM_SETS # The L1 cache size should be 32KB, so modify block_size and sets so that that is the case

memory = DualChannelDDR4_2400(size="8GB", interleaving_size=block_size)

# Unified L1, Unified L2
cache_hierarchy = UnifiedL1L2(
        l1_sets=l1_sets,
        l1_block_size=block_size,
)

board = BoardVariableBlockSize(
        clk_freq="1GHz",
        memory=memory,
        cache_hierarchy=cache_hierarchy,
        processor=Processor(block_size=block_size),
        block_size=block_size, 
)

board.set_se_binary_workload(obtain_resource(get_workload()), env_list=[f"LD_LIBRARY_PATH={os.environ.get('LD_LIBRARY_PATH')}"])

simulator = Simulator(board=board)
simulator.run()
