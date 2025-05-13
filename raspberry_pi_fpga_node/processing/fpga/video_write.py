"""This module contains the processor that writes video and execute lang."""

import tempfile

import cv2

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.processing.fpga.command_proccessing_base import (
    CommandProcessingBase,
)
from loguru import logger

class VideoWriter:
    """This class writes video and switch tick in executor"""

    def __init__(self) -> None:
        self.camera = cv2.VideoCapture(settings.camera_number)
        self.fourcc = cv2.VideoWriter_fourcc(*settings.fourcc_codec)
        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_video(
        self, command_processor: CommandProcessingBase, position = 0
    ) -> bytes:
        logger.info("Video start")
        with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
            out = cv2.VideoWriter(
                tmp.name, self.fourcc, settings.fps, (self.width, self.height)
            )
            while command_processor.execution_state:
                ret, frame = self.camera.read()
                command_processor.next()
                if not ret:
                    break
                frame_cut = (
                    frame[:, : self.width] if not position else frame[:, self.width :]
                )
                out.write(frame_cut)
            out.release()
            tmp.seek(0)
            return tmp.read()
