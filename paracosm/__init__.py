from typing import Annotated
from fastapi import Depends, FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from shlex import split as parse_args

from .beats.gatekeeper import EnableGatekeeper
from .program import eightball, help, read, seek, splash
from .device import Device
from .shell import Shell

app = FastAPI()

security = HTTPBasic()


static = StaticFiles(directory="static")
app.mount("/static", static, name="static")


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await websocket.accept()

    device = Device("flamango")
    device.add_file_locale("poe.diff")
    device.add_file_locale("README")
    device.add_file_locale("severance.txt")
    device.add_file_locale("pwned.txt")

    shell = Shell(websocket)
    shell.add_program(help, eightball, splash, seek, read)
    shell.event_handler = EnableGatekeeper(shell, device)

    while True:
        line = await shell.readline()

        cmd, *args = parse_args(line)
        program = shell.get_program(cmd)
        if program:
            await program.run(args, shell, device)
        else:
            await shell.writeline(f"Alas, no '{cmd}' found.\nCruel world.")


@app.get("/")
async def read_index(
    request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return await static.get_response("index.html", scope=request.scope)
