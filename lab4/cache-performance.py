from components.board_variable_block_size import BoardVariableBlockSize
from components.caches import UnifiedL1, L1DOnly, L1IOnly
from components.processor import Processor
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
import os

# We specify it here because we need to set it in several locations!
block_size = 32 # Bytes. Don't change for this experiment. 

memory = DualChannelDDR4_2400(size="2GB")

cache_hierarchy = UnifiedL1(l1_sets=64,l1_assoc=4,block_size=block_size)

board = BoardVariableBlockSize(
        clk_freq="3GHz",
        memory=memory,
        cache_hierarchy=cache_hierarchy,
        processor=Processor(block_size=block_size),
        block_size=block_size, 
)

board.set_se_binary_workload(obtain_resource("WORKLOAD"), env_list=[f"LD_LIBRARY_PATH={os.environ.get('LD_LIBRARY_PATH')}"])

simulator = Simulator(board=board)
simulator.run()
