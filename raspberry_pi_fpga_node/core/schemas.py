from pydantic import BaseModel, HttpUrl
from raspberry_pi_fpga_node.core.enums import LangExecutionType


class FpgaTask(BaseModel):
    flash_file: HttpUrl
    instruction_file: HttpUrl
    execution_type: LangExecutionType = LangExecutionType.lite
