from components.bp_processors import VariableWidthO3Processor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

from m5.objects import StaticBP, LocalBP, TournamentBP, BiModeBP
from argparser import get_workload
import os
from pathlib import Path
from gem5.resources.resource import BinaryResource
# L1D and L1I, unified L2
# L1D and L1I will have associativity 8, L2 will have associativity 4
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size='16kB',
        l1i_size='16kB',
        l2_size='256kB',
)

# Memory
memory = SingleChannelDDR4_2400(size='4GB')

# Change the pipeline width!
pw = 8
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
#board.set_se_binary_workload(obtain_resource(get_workload()), env_list=[f"LD_LIBRARY_PATH={os.environ.get('LD_LIBRARY_PATH')}"])
binary_path = Path("/home/dumitra/gem5-2025/gem5/eitf20-gem5/workloads/a.out")
board.set_se_binary_workload(
    binary = BinaryResource(
        local_path=binary_path.as_posix()
    )
)

simulator = Simulator(board=board)
simulator.run()
