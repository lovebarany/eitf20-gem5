from typing import (
        Optional,
        Union,
)

from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
from gem5.components.memory.dram_interfaces.ddr4 import DDR4_2400_8x8
from gem5.components.memory.memory import ChanneledMemory

def DualChannelDDR4_2400(
        interleaving_size: int,
        size: Optional[str] = None,
) -> AbstractMemorySystem:
    """ 
    Dual channel memory system with non-fixed interleaving size
    """
    # Set minimum interleaving size to 64, otherwise we crash
    # 64 is the default value, hence we use that
    inter_size = max(interleaving_size, 64)
    return ChanneledMemory(DDR4_2400_8x8, 2, inter_size, size)
