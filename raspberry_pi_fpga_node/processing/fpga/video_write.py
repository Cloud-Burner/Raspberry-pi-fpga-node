"""This module contains the processor that writes video and execute lang."""

import tempfile
import time

import cv2
from loguru import logger

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.processing.fpga.command_proccessing_base import (
    CommandProcessingBase,
)

MAX_ERROR_COUNT = 200


class VideoWriter:
    """This class writes video and switch tick in executor"""

    def __init__(self) -> None:
        self.camera = cv2.VideoCapture(settings.camera_number)
        self.fourcc = cv2.VideoWriter_fourcc(*settings.fourcc_codec)
        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2

    def get_video(
        self, command_processor: CommandProcessingBase, position: int
    ) -> bytes:
        logger.info("Video start")
        with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
            out = cv2.VideoWriter(
                tmp.name, self.fourcc, settings.fps, (self.width, self.height)
            )
            errors_count = 0
            while command_processor.execution_state and errors_count < MAX_ERROR_COUNT:
                time.sleep(0.05)
                ret, frame = self.camera.read()
                if not ret:
                    errors_count += 1
                    logger.warning(f"Didn't receive frame: {errors_count}")
                    continue

                command_processor.next()
                frame_cut = (
                    frame[: self.height, :] if not position else frame[self.height :, :]
                )
                out.write(frame_cut)
            out.release()
            tmp.seek(0)
            return tmp.read()
