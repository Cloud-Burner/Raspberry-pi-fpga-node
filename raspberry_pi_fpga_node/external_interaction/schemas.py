"""This module contains the outer validation schemas."""

from pydantic import BaseModel

from raspberry_pi_fpga_node.core.enums import LangExecutionType


class FpgaTask(BaseModel):
    """FpgaTask represents a task from user."""

    number: str
    user_id: int
    flash_file: str
    instruction_file: str
    execution_type: LangExecutionType = LangExecutionType.LITE


class ResultFpgaTask(BaseModel):
    """ResultFpgaTask represents a answer on user task"""

    number: str
    user_id: int
    link: str
