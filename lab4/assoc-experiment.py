from argparser import get_workload
from components.board_variable_block_size import BoardVariableBlockSize
from components.caches import UnifiedL1, L1DOnly, L1IOnly
from components.processor import Processor
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
import os

# Cache parameters
block_size = 32 # Bytes
l1_assoc = ASSOC
l1_sets = 32

memory = DualChannelDDR4_2400(size="8GB")


# Unified: UnifiedL1
# Data-only: L1DOnly
# Instruction-only: L1IOnly
cache_hierarchy = UnifiedL1(
        l1_sets=l1_sets,
        l1_assoc=l1_assoc,
        block_size=block_size
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
