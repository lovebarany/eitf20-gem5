from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import (
        ExitEvent,
        Simulator,
)
import m5

cache_hierarchy = NoCache()

# Memory
memory = SingleChannelDDR4_2400(size='4GB')

# Processor
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1, isa=ISA.X86)

# Set up the board, connect all the components together
board = SimpleBoard(
        clk_freq='3GHz',
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy
)

# Sets the workload based on the --benchmark=WORKLOAD
board.set_se_binary_workload(obtain_resource("hello-gem5"))

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
