"""This module contains the definition of the Command ProccessingBase class."""

import lgpio

from raspberry_pi_fpga_node.core.settings import settings

chip = lgpio.gpiochip_open(0)
for pin in settings.arduino_pins + settings.fpga_pins:
    lgpio.gpio_claim_output(chip, pin, 1)


class CommandProcessingBase:
    """Command processing base class needs for subclasses of command execution."""

    def __init__(self, instruction: bytes) -> None:
        self._instruction = [
            line.split()
            for line in instruction.decode("utf-8").splitlines()
            if line.strip() != ""
        ]
        self.execution_state = True
        self.frame_counter = 30
        self.command_counter = 0

    def next(self) -> None:
        """Method that calls every frame of the video stream."""
        raise NotImplementedError
