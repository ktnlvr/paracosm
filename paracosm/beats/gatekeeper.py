from ..program import program, Shell, Device
from ..device import File
from ..events import EventHandler


class EnableGatekeeper(EventHandler):
    def on_file_read(self, file: File):
        if file.name == "README":
            self.shell.add_program(gatekeeper)


@program(name="gatekeeper", brief="training tool for handling memetic information")
async def gatekeeper(args: list[str], shell: Shell, device: Device):
    await shell.writeline("THE END XOXO")
