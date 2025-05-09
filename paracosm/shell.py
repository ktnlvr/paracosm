from fastapi import WebSocket


class Shell:
    def __init__(self, ws: WebSocket):
        self.ws = ws
        self.programs = []

    async def writeline(self, *text: str):
        await self.ws.send_text("\n".join(text))

    async def readline(self) -> str:
        return await self.ws.receive_text()

    async def close(self):
        await self.ws.close()

    def get_program(self, name: str):
        for program in self.programs:
            if program.name == name:
                return program
        return None
