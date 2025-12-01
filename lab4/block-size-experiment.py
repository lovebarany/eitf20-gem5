from argparser import get_workload
from components.board_variable_block_size import BoardVariableBlockSize
from components.caches import UnifiedL1L2
from components.processor import Processor
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
import os

# Cache parameters
l1_block_size = BLOCK_SIZE # Bytes
l1_assoc = 2
l1_sets = SETS # The cache size should be 32KB, so modify block_size and sets so that that is the case
l2_block_size = 256 # Bytes
l2_sets = 512
l2_assoc = 4

memory = DualChannelDDR4_2400(size="8GB")

# Unified L1, Unified L2
cache_hierarchy = UnifiedL1L2(
        l1_sets=l1_sets,
        l1_block_size=l1_block_size,
        l1_assoc=l1_assoc,
        l2_sets=l2_sets,
        l2_block_size=l2_block_size,
        l2_assoc=l2_assoc
)

board = BoardVariableBlockSize(
        clk_freq="1GHz",
        memory=memory,
        cache_hierarchy=cache_hierarchy,
        processor=Processor(block_size=l1_block_size),
        block_size=l1_block_size, 
)

board.set_se_binary_workload(obtain_resource(get_workload()), env_list=[f"LD_LIBRARY_PATH={os.environ.get('LD_LIBRARY_PATH')}"])

simulator = Simulator(board=board)
simulator.run()
