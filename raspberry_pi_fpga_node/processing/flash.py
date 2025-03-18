from raspberry_pi_fpga_node.core.settings import settings


class Flash:
    def __init__(self):
        print("initssss")
        self.fpga_address = settings.fpga_address
        # create flash congig
        # todo checks form settings?
        pass

    def flash_fpga(self):
        print("fpga flashed")
        pass

    def flash_arduino_nano(self):
        pass
