"""This module contains the settings for the all app"""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class for the Raspberry Pi Fpga node"""

    green_board_q: str = "green_1"
    log_level: str = "info"
    max_threads: int = 3
    camera_number: int = 1
    fourcc_codec: str = "mp4v"
    video_format: str = "mp4"
    fps: int = 20

    fpga_address: str = "ax9999"
    fpga_camera_position: Literal[0, 1] = 0

    s3_url: str = "http://localhost:9000"
    access_key: str = "f0Sxs0Bf2pqJDQtFNQZF"
    secret_key: str = "hrGuLOhzFZBNWtmL5TJ8wiB2e5d9jIHeSzdEYXbW"
    result_bucket: str = "test"
    task_bucket: str = "test"


settings = Settings()
