class CommandProcessingBase:
    def __init__(self, instruction: bytes):
        self.execution_state = True
        self.frame_counter = 200

    def next(self):
        raise NotImplementedError
