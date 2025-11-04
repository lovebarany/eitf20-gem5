from components.board_variable_block_size import BoardVariableBlockSize
from components.caches import UnifiedL1L2
from components.processor import Processor
from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

# We specify it here because we need to set it in several locations!
block_size = 32 # Bytes. Don't change for this experiment. 

memory = DualChannelDDR4_2400(size="2GB")

cache_hierarchy = UnifiedL1L2(
        l1_sets=512,
        l1_block_size=block_size,
        l2_sets=128,
        l2_block_size=256,
        l2_assoc=16)

board = BoardVariableBlockSize(
        clk_freq="3GHz",
        memory=memory,
        cache_hierarchy=cache_hierarchy,
        processor=Processor(block_size=block_size),
        block_size=block_size, 
)

board.set_se_binary_workload(obtain_resource("x86-matrix-multiply"))

simulator = Simulator(board=board)
simulator.run()
