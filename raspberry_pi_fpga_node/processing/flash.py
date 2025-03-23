import subprocess
from pathlib import Path

from loguru import logger

from raspberry_pi_fpga_node.core.settings import settings


class Flash:
    def __init__(self):
        # create flash congig
        # todo checks form settings?
        self.clear_flash = str(Path(settings.dynamic_dir + "/clear_flash.svf"))
        self.bench_flash = str(Path(settings.dynamic_dir + "/output.svf"))
        self.target_fpga = str(Path(settings.static_dir + "/target_fpga.cfg "))
        self.blaster_conf = str(Path(settings.static_dir + "/usb_blaster.cfg "))
        logger.info("Fpga confs inited")

    def flash_fpga(self, flash_file_path: str):
        command = [
            "openocd",
            "-f",
            self.blaster_conf,
            "-f",
            self.target_fpga,
            "-c",
            f"init; svf {flash_file_path}; shutdown",
        ]
        logger.debug(command)
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logger.info(f"Fpga flashed for {flash_file_path.split('/')[-1]}")
        except subprocess.CalledProcessError as exc:
            logger.error(f"Ошибка при выполнении команды {exc}")
            # todo raise something

    def flash_arduino_nano(self):
        pass
