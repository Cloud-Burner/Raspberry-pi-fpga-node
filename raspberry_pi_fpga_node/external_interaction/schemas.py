from pydantic import AnyUrl, BaseModel

from raspberry_pi_fpga_node.core.enums import LangExecutionType


class FpgaTask(BaseModel):
    number: str
    username: str
    flash_file: str
    instruction_file: str
    execution_type: LangExecutionType = LangExecutionType.lite


class ResultFpgaTask(BaseModel):
    number: str
    username: str
    link: AnyUrl
