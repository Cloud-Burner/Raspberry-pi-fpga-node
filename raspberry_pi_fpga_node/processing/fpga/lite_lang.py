"""This module contains Lang executor for fpga."""

import lgpio  # type: ignore[import-not-found]
from loguru import logger

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.processing.fpga.command_proccessing_base import (
    CommandProcessingBase,
    chip,
)


class LiteLangExecutor(CommandProcessingBase):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        logger.info("starting LiteLangExecutor")
        super().__init__(*args, **kwargs)
        logger.info("super initied")
        self.map_commands = {
            "pin": self._set_pin_state,
            "write_frame": self._add_frame_amount,
        }
        logger.info("map ready")
        self.allowed_pins = settings.connected_pins
        logger.info("allowed pins: " + str(self.allowed_pins))

    def _set_pin_state(self) -> None:
        logger.info("Setting pin")
        _, pin_str, state = self._instruction[self.command_counter]
        pin = int(pin_str)

        if not pin or not state:
            raise ValueError(f"Invalid script, pin is {pin}, state is {state}")

        if pin not in self.allowed_pins:
            logger.error(f"Not allowed to set pin {pin}")
            raise ValueError(f"Incorrect script, pin is {pin}")
        logical_state = 1 if state == "high" else 0
        lgpio.gpio_write(chip, pin, logical_state)

    def _add_frame_amount(self) -> None:
        _, amount = self._instruction[self.command_counter]
        self.frame_counter += int(amount)

    def next(self) -> None:
        logger.info(f"Next called with {self.frame_counter} frames")
        self.frame_counter -= 1
        if self.frame_counter == 1 and self.command_counter < len(self._instruction):
            self.frame_counter += 1

            self.map_commands[self._instruction[self.command_counter][0]]()
            self.command_counter += 1
        elif self.frame_counter == 0:
            self.execution_state = False

        if self.frame_counter == 0:
            self.execution_state = False
