from .device import Device
from .shell import Shell


class EventHandler:
    def __init__(self, shell: Shell, device: Device):
        self.shell = shell
        self.device = device

    def on_file_read(self, name: str):
        ...
