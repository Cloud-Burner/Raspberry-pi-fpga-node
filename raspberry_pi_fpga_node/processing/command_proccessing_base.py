"""This module contains the definition of the Command ProccessingBase class."""


class CommandProcessingBase:
    """Command processing base class needs for subclasses of command execution."""

    def __init__(self, instruction: bytes) -> None:
        self._instruction = instruction
        self.execution_state = True
        self.frame_counter = 200

    def parse_instruction(self) -> None:
        """Parses the instruction and save list of commands."""
        pass

    def next(self) -> None:
        """Method that calls every frame of the video stream."""
        raise NotImplementedError
