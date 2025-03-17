from pydantic import BaseModel

from raspberry_pi_fpga_node.core.enums import LangExecutionType


class FpgaTask(BaseModel):
    flash_file: str
    instruction_file: str
    execution_type: LangExecutionType = LangExecutionType.lite
