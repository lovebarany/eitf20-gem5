from abc import ABCMeta

from gem5.utils.override import overrides
from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.abstract_cache_hierarchy import AbstractCacheHierarchy
from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
from gem5.components.processors.abstract_processor import AbstractProcessor
from gem5.components.boards.se_binary_workload import SEBinaryWorkload

from m5.objects import (
    AddrRange,
    IOXBar,
    SimObject,
    System,
    Port,
)

from typing import List



class AbstractSystemBoardVariableBlockSize(System, AbstractBoard):
    """
    An abstract board for cases where boards should inherit from System.
    """

    __metaclass__ = ABCMeta

    def __init__(
        self,
        clk_freq: str,
        processor: "AbstractProcessor",
        memory: "AbstractMemorySystem",
        cache_hierarchy: "AbstractCacheHierarchy",
        block_size: int
    ):
        System.__init__(
            self,
            cache_line_size=block_size,
        )
        AbstractBoard.__init__(
            self,
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
        )

    @overrides(SimObject)
    def createCCObject(self):
        """We override this function as it is called in ``m5.instantiate``. This
        means we can insert a check to ensure the ``_connect_things`` function
        has been run.
        """
        super()._connect_things_check()
        super().createCCObject()


class BoardVariableBlockSize(AbstractSystemBoardVariableBlockSize, SEBinaryWorkload):
    def __init__(
        self,
        clk_freq: str,
        processor: AbstractProcessor,
        memory: AbstractMemorySystem,
        cache_hierarchy: AbstractCacheHierarchy,
        block_size: int
    ) -> None:
        super().__init__(
            clk_freq=clk_freq,
            processor=processor,
            memory=memory,
            cache_hierarchy=cache_hierarchy,
            block_size=block_size
        )

    @overrides(AbstractSystemBoardVariableBlockSize)
    def _setup_board(self) -> None:
        pass

    @overrides(AbstractSystemBoardVariableBlockSize)
    def has_io_bus(self) -> bool:
        return False

    @overrides(AbstractSystemBoardVariableBlockSize)
    def get_io_bus(self) -> IOXBar:
        raise NotImplementedError(
            "SimpleBoard does not have an IO Bus. "
            "Use `has_io_bus()` to check this."
        )

    @overrides(AbstractSystemBoardVariableBlockSize)
    def has_dma_ports(self) -> bool:
        return False

    @overrides(AbstractSystemBoardVariableBlockSize)
    def get_dma_ports(self) -> List[Port]:
        raise NotImplementedError(
            "SimpleBoard does not have DMA Ports. "
            "Use `has_dma_ports()` to check this."
        )

    @overrides(AbstractSystemBoardVariableBlockSize)
    def has_coherent_io(self) -> bool:
        return False

    @overrides(AbstractSystemBoardVariableBlockSize)
    def get_mem_side_coherent_io_port(self) -> Port:
        raise NotImplementedError(
            "SimpleBoard does not have any I/O ports. Use `has_coherent_io` to "
            "check this."
        )

    @overrides(AbstractSystemBoardVariableBlockSize)
    def _setup_memory_ranges(self) -> None:
        memory = self.get_memory()

        # The simple board just has one memory range that is the size of the
        # memory.
        self.mem_ranges = [AddrRange(memory.get_size())]
        memory.set_memory_range(self.mem_ranges)
