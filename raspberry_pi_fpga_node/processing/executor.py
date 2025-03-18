from concurrent.futures import ThreadPoolExecutor

from raspberry_pi_fpga_node.core.settings import settings

executor = ThreadPoolExecutor(max_workers=settings.max_threads)
