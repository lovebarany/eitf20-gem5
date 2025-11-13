from gem5.components.memory.memory import ChanneledMemory
from gem5.components.memory.dram_interfaces.ddr4 import DDR4_2400_8x8
from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
from typing import Optional

def MultiChannelDDR4_2400(
    channels =4,
    size: Optional[str] = None
) -> AbstractMemorySystem:
    
 #   A multi channel memory system using DDR4_2400_8x8 based DIMM.
   
    return ChanneledMemory(DDR4_2400_8x8, channels, 64, size=size)
