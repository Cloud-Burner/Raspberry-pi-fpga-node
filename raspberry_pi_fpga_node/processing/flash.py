from loguru import logger

from raspberry_pi_fpga_node.core.settings import settings


class Flash:
    def __init__(self):
        logger.info("initssss")
        self.fpga_address = settings.fpga_address
        # create flash congig
        # todo checks form settings?
        pass

    def flash_fpga(self, flash_file: bytes):
        logger.info("Fpga flashed")
        pass

    def flash_arduino_nano(self):
        pass
