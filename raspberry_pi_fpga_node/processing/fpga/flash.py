"""This module contains the flash processor."""

import os
import subprocess
from pathlib import Path

from jinja2 import Template
from loguru import logger

from raspberry_pi_fpga_node.core.settings import settings


class Flash:
    """This class contains the flash processor for fpga and arduino."""

    def __init__(self) -> None:
        self.clear_flash = str(Path(settings.dynamic_dir + "/clear_flash.svf"))
        self.bench_flash = str(Path(settings.dynamic_dir + "/output.svf"))
        self.target_fpga = str(Path(settings.static_dir + "/target.cfg"))
        self.blaster_conf = str(Path(settings.static_dir + "/usb_blaster.cfg"))
        if os.path.exists(f"{settings.static_dir}/target.cfg"):
            os.remove(f"{settings.static_dir}/target.cfg")
            logger.info("Old target.cfg removed")
        with open(f"{settings.static_dir}/target_template.cfg", "r") as f:
            template_content = f.read()
        template = Template(template_content)
        rendered = template.render(expected_id=settings.fpga_address)
        with open(f"{settings.static_dir}/target.cfg", "w") as f:
            f.write(rendered)
        logger.info("New target.cfg created")

        logger.info("Fpga confs inited")

    def flash_fpga(self, flash_file_path: str) -> None:
        """Function calls openocd flash tool to load user flash file
        :param flash_file_path:"""
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
            logger.error(f"Error flashing boart {exc}")
            raise ConnectionRefusedError("No connection to fpga") from exc

    def flash_arduino_nano(self, flash_file_path: str) -> None:
        """Function calls openocd flash tool to load user flash file
        :param flash_file_path:"""
        rate = "-b57600" if settings.bootloader_old else "-b115200"
        # avrdude -v -patmega328p -carduino -P /dev/ttyUSB0 -b57600 -D -Uflash:w:sketch_may4a.ino.with_bootloader.hex:i
        command = [
            "avrdude",
            "-v",
            "-patmega328p",
            "-carduino",
            "-P",
            settings.arduino_nano_port,
            rate,
            "-D",
            f"-Uflash:w:{flash_file_path}:i",
        ]
        logger.debug(command)
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logger.info(f"Arduino nano flashed for {flash_file_path.split('/')[-1]}")
        except subprocess.CalledProcessError as exc:
            logger.error(f"Error flashing board {exc}")
            raise ConnectionRefusedError("No connection to arduino") from exc
