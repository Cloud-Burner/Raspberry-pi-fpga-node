"""This module contains the settings for the all app"""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """Settings class for the Raspberry Pi Fpga node"""

    rabbit_host: str = "192.168.1.39"
    rabbit_port: int = 5672
    rabbit_user: str = "user"
    rabbit_password: str = "password"
    green_board_q: str = "green_1"
    result_queue: str = "result"

    log_level: str = "DEBUG"
    max_threads: int = 3
    camera_number: int = 0
    fourcc_codec: str = "mp4v"
    video_format: str = "mp4"
    fps: int = 20

    fpga_address: str = "ax9999"
    fpga_camera_position: Literal[0, 1] = 0

    connected_pins: set[int] = {5, 6}

    s3_url: str = "http://192.168.1.39:9000"
    access_key: str = "f0Sxs0Bf2pqJDQtFNQZF"
    secret_key: str = "hrGuLOhzFZBNWtmL5TJ8wiB2e5d9jIHeSzdEYXbW"
    result_bucket: str = "test"
    task_bucket: str = "test"

    project_dir: str = str(Path.cwd())
    dynamic_dir: str = project_dir + "/raspberry_pi_fpga_node/processing/dynamic_files"
    static_dir: str = project_dir + "/raspberry_pi_fpga_node/processing/static_confs"


settings = Settings()
