from fastapi import WebSocket

from .expunger import Expunger

class Shell:
    def __init__(self, ws: WebSocket):
        self.ws = ws
        self.programs = []
        self.expunger = Expunger()
        self.event_handler = None

    def add_program(self, *program):
        self.programs.extend(program)

    async def writeline(self, *text: str):
        raw = "\n".join(text)
        expunged = self.expunger.expunge(raw)
        await self.ws.send_text(expunged)

    async def readline(self) -> str:
        return await self.ws.receive_text()

    async def close(self):
        await self.ws.close()

    def get_program(self, name: str):
        for program in self.programs:
            if program.name == name:
                return program
        return None
