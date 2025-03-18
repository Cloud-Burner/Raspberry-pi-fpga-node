from raspberry_pi_fpga_node.processing.flash import Flash

# todo plan

# in
#  files
# flash + excecute + writre video

# запускаем ексекутор и ливаем?
# тест усппех
flasher = Flash()


def fpga_handle(flash_file_path: str, instruction: bytes) -> None:
    flasher.flash_fpga()
    # start write video
    # universal ?

    pass


def arduino_nano_handle():
    pass
