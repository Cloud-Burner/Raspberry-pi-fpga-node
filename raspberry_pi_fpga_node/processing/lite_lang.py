from raspberry_pi_fpga_node.processing.command_proccessing_base import (
    CommandProcessingBase,
)


class LiteLangExecutor(CommandProcessingBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def next(self):
        # todo lang exec
        self.frame_counter -= 1
        if self.frame_counter == 0:
            self.execution_state = False
