"""This module contains the settings for the all app"""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class for the Raspberry Pi Fpga node"""

    MODE: Literal["sync", "async"] = "async"

    rabbit_host: str = "192.168.1.39"
    rabbit_port: int = 5672
    rabbit_user: str = "user"
    rabbit_password: str = "password"
    async_node_q: str = "green_1"
    async_node_avr: str = "arduino_nano_1"
    sync_node_q: str = "sync_de10_lite_1"
    result_queue: str = "result"

    log_level: str = "DEBUG"
    max_threads: int = 2
    camera_number: int = 0
    fourcc_codec: str = "mp4v"
    video_format: str = "mp4"
    fps: int = 20

    fpga_address: str = "0x020f10dd"  # de10lite =
    fpga_camera_position: Literal[0, 1] = 0
    arduino_camera_position: Literal[0, 1] = 1

    connected_pins: set[int] = {5, 6}
    fpga_pins: set[int] = {5, 6}
    arduino_pins: set[int] = {7, 8}
    bootloader_old: bool = True
    arduino_nano_port: str = "/dev/ttyUSB0"

    s3_url: str = "http://192.168.1.39:9000"
    access_key: str = "f0Sxs0Bf2pqJDQtFNQZF"
    secret_key: str = "hrGuLOhzFZBNWtmL5TJ8wiB2e5d9jIHeSzdEYXbW"
    result_bucket: str = "test"
    task_bucket: str = "test"

    project_dir: str = str(Path.cwd())
    dynamic_dir: str = project_dir + "/raspberry_pi_fpga_node/processing/dynamic_files"
    static_dir: str = project_dir + "/raspberry_pi_fpga_node/processing/static_confs"


settings = Settings()
