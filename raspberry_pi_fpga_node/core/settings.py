"""This module contains the settings for the all app"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class for the Raspberry Pi Fpga node"""

    green_board_q: str = "green_1"
    log_level: str = "debug"

    s3_url: str = "http://localhost:9000"
    access_key: str = "f0Sxs0Bf2pqJDQtFNQZF"
    secret_key: str = "hrGuLOhzFZBNWtmL5TJ8wiB2e5d9jIHeSzdEYXbW"
    result_bucket: str = "test"
    task_bucket: str = "test"


settings = Settings()
