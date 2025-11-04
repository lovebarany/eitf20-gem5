from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import AbstractClassicCacheHierarchy
from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache
from gem5.isas import ISA

from m5.objects import *

class L1Cache(AbstractClassicCacheHierarchy):
    """
    A cache hierarchy only consisting of a unified L1 cache
    """

    def _get_default_membus(self) -> SystemXBar:
        """
        A method used to obtain the default memory bus of 32 bytes in width for
        the unified cache.

        :returns: The default memory bus for the L1Cache
        """
        membus = SystemXBar(width=self._block_size)
        return membus

    def __init__(
            self,
            l1_sets: int,
            l1_assoc: int,
            block_size: int,
            ):
        AbstractClassicCacheHierarchy.__init__(self=self)
        self._block_size = block_size
        self._l1_assoc = l1_assoc
        # Compute the size based on block size, associativity, and number of sets
        size = self._l1_assoc*l1_sets*self._block_size
        self._l1_size = size

        self.membus = self._get_default_membus()

    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports
    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports
    def connect_mem_system(self, board: AbstractBoard) -> None:
        board.connect_system_port(self.membus.cpu_side_ports)

        for _, port in board.get_mem_ports():
            self.membus.mem_side_ports = port
    def connect_interrupts(self, cpu) -> None:
        int_req_port = self.membus.mem_side_ports
        int_resp_port = self.membus.cpu_side_ports
        cpu.connect_interrupt(int_req_port, int_resp_port)

class UnifiedL1(L1Cache):

    def __init__(
            self,
            l1_sets: int,
            l1_assoc: int,
            block_size: int,
            ):
        super().__init__(l1_sets=l1_sets,l1_assoc=l1_assoc,block_size=block_size)

    def incorporate_cache(self, board: AbstractBoard) -> None:
        self.connect_mem_system(board)

        self.l1caches = [
                # Specify the size as the computed size (in Bytes) divided by 1000
                L1ICache(size=f"{self._l1_size//1024}kB",assoc=self._l1_assoc)
                for _ in range(board.get_processor().get_num_cores())
                ]
        self.xbars = [
                # We need crossbars to connect icache and dcache lines to same port
                L2XBar() for _ in range(board.get_processor().get_num_cores())
                ]

        for i, cpu in enumerate(board.get_processor().get_cores()):
            cpu.connect_icache(self.xbars[i].cpu_side_ports)
            cpu.connect_dcache(self.xbars[i].cpu_side_ports)
            self.xbars[i].mem_side_ports = self.l1caches[i].cpu_side
            self.membus.cpu_side_ports = self.l1caches[i].mem_side

            self.connect_interrupts(cpu)

class L1DOnly(L1Cache):
    def __init__(
            self,
            l1_sets: int,
            l1_assoc: int,
            block_size: int,
            ):
        super().__init__(l1_sets=l1_sets,l1_assoc=l1_assoc,block_size=block_size)

    def incorporate_cache(self, board: AbstractBoard) -> None:
        self.connect_mem_system(board)

        self.l1dcaches = [
                L1DCache(size=f"{self._l1d_size//1024}kB",assoc=self._l1d_assoc)
                for _ in range(board.get_processor().get_num_cores())
                ]

        for i, cpu in enumerate(board.get_processor().get_cores()):
            # Connect I-cache directly to memory
            cpu.connect_icache(self.get_cpu_side_port())
            # Connect D-cache to cache
            cpu.connect_dcache(self.l1dcaches[i].cpu_side)
            self.l1dcaches[i].mem_side = self.get_cpu_side_port()

            self.connect_interrupts(cpu)

class L1IOnly(L1Cache):
    def __init__(
            self,
            l1_sets: int,
            l1_assoc: int,
            block_size: int,
            ):
        super().__init__(l1_sets=l1_sets,l1_assoc=l1_assoc,block_size=block_size)

    def incorporate_cache(self, board: AbstractBoard) -> None:
        self.connect_mem_system(board)

        self.l1dcaches = [
                L1DCache(size=f"{self._l1d_size//1024}kB",assoc=self._l1d_assoc)
                for _ in range(board.get_processor().get_num_cores())
                ]

        for i, cpu in enumerate(board.get_processor().get_cores()):
            # Connect D-cache directly to memory
            cpu.connect_dcache(self.get_cpu_side_port())
            # Connect I-cache to cache
            cpu.connect_icache(self.l1dcaches[i].cpu_side)
            self.l1dcaches[i].mem_side = self.get_cpu_side_port()

            self.connect_interrupts(cpu)

class UnifiedL1L2(AbstractClassicCacheHierarchy):
    def _get_default_membus(self) -> SystemXBar:
        """
        A method used to obtain the default memory bus of 64 bit in width for
        the unified cache.

        :returns: The default memory bus for the UnifiedL1L2 cache
        """
        membus = SystemXBar(width=self._l2_block_size)
        return membus

    def __init__(
            self,
            l1_sets: int,
            l1_block_size: int,
            l2_sets: int,
            l2_assoc: int,
            l2_block_size: int,
            ):
        AbstractClassicCacheHierarchy.__init__(self=self)

        self._l1_block_size = l1_block_size
        # Fixed L1 associativity
        self._l1_assoc = 2
        self._l2_block_size = l2_block_size
        self._l2_assoc = l2_assoc
        # Compute the size based on block size, associativity, and number of sets
        l1_size = self._l1_assoc*l1_sets*self._l1_block_size
        l2_size = self._l2_assoc*l2_sets*self._l2_block_size

        # Ensure values are correct
        assert l1_block_size in [16,32,64,128,256], f"L1 Cache block size should be either 16, 32, 64, 128, or 256 Bytes, is {self._l1_block_size}"
        assert l1_size==(32*1024), f"L1 Cache size should be 32kB, is {l1_size//1024}kB"
        assert l2_size==(512*1024), f"L2 Cache size should be 512kB, is {l2_size//1024}kB"
        assert self._l2_block_size>=256, f"L2 Cache block size should be at least 256, is {self._l2_block_size}"

        self._l1_size = l1_size
        self._l2_size = l2_size

        self.membus = self._get_default_membus()
    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports
    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports
    def connect_mem_system(self, board: AbstractBoard) -> None:
        board.connect_system_port(self.membus.cpu_side_ports)

        for _, port in board.get_mem_ports():
            self.membus.mem_side_ports = port
    def connect_interrupts(self, cpu) -> None:
        int_req_port = self.membus.mem_side_ports
        int_resp_port = self.membus.cpu_side_ports
        cpu.connect_interrupt(int_req_port, int_resp_port)

    def incorporate_cache(self, board: AbstractBoard) -> None:
        self.connect_mem_system(board)

        self.l1caches = [
                L1DCache(size=f"{self._l1_size//1024}kB",assoc=self._l1_assoc)
                for _ in range(board.get_processor().get_num_cores())
                ]
        self.l2caches = [
                L2Cache(size=f"{self._l2_size//1024}kB",assoc=self._l2_assoc)
                for _ in range(board.get_processor().get_num_cores())
                ]
        self.xbars = [
                # We need crossbars to connect icache and dcache lines to same port
                L2XBar() for _ in range(board.get_processor().get_num_cores())
                ]

        for i, cpu in enumerate(board.get_processor().get_cores()):
            cpu.connect_icache(self.xbars[i].cpu_side_ports)
            cpu.connect_dcache(self.xbars[i].cpu_side_ports)
            self.xbars[i].mem_side_ports = self.l1caches[i].cpu_side
            self.l2caches[i].cpu_side = self.l1caches[i].mem_side
            self.membus.cpu_side_ports = self.l2caches[i].mem_side

            self.connect_interrupts(cpu)
