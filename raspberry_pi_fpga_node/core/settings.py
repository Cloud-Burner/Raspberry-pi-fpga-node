"""This module contains the settings for the all app"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class for the Raspberry Pi Fpga node"""

    green_board_q: str = "green_1"
    log_level: str = "debug"


settings = Settings()
