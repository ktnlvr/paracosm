from abc import ABC, abstractmethod
from random import choice
from asyncio import sleep

from .utils import chance
from .device import Device
from .shell import Shell


class Program(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def run(self, args: list[str], shell: Shell, device: Device): ...


def program(name, brief):
    def wrapper(func):
        class MicroProgram(Program):
            def __init__(self):
                super().__init__()
                self.name = name
                self.brief = brief

            async def run(self, args: list[str], shell: Shell, device: Device):
                await func(args, shell, device)

        return MicroProgram()

    return wrapper


@program(name="help", brief="prints the list of available commands")
async def help(args: list[str], shell: Shell, device: Device):
    lines = ["Thank you for using the help command!"]
    for program in shell.programs:
        lines.append(f"{program.name} - {program.brief}")
    await shell.writeline(*lines)


@program(name="splash", brief="prints the introductory splash screen")
async def splash(args: list[str], shell: Shell, device: Device):
    splash_messages = [
        "Now with twice as much RAM!",
        "Silver Initiative Co.",
        "Expanding since 18XX!",
        "Cutting-face technology.",
        "Make the future predictible.",
        "Business Edition",
    ]

    message = choice(splash_messages)

    lines = [
        " __        __        __   __   __            __   __  ",
        "|__)  /\  |__)  /\  /  ` /  \ /__`  |\/|    /  \ /__` ",
        "|    /~~\ |  \ /~~\ \__, \__/ .__/  |  |    \__/ .__/ ",
        "",
        f"- {message}",
        "",
        "Huzzah! Run `help` for help.",
    ]

    await shell.writeline(*lines)


@program(name="eightball", brief="whispers truths")
async def eightball(args: list[str], shell: Shell, device: Device):
    prelude = "The magic 8-ball says..."
    await shell.writeline(prelude)
    await sleep(1.5)

    answers = [
        "Certainly.",
        "Decidedly so.",
        "Yes.",
        "Better not to tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "Very doubtful.",
        "Outlook not so good.",
    ]

    answer = choice(answers)
    await shell.writeline(answer)


@program(name="seek", brief="looks for things, do NOT use with philosophical concepts")
async def seek(args: list[str], shell: Shell, device: Device):
    if len(args) < 1:
        await shell.writeline("Name something to seek, like `seek truth`.")
        return

    if args[0] == "guidance":
        text = "READMEs have text."
        if chance(0.01):
            text = "READMEs have eyes.    o.o"
        await shell.writeline(text)
        return

    for arg in args:
        if file := device.get_file(arg):
            await shell.writeline(f"File {file.name} exists, nothing to seek.")
            return

        results = device.seek(arg)
        if len(results) == 0:
            await shell.writeline(f"Seeking {arg}...")
            await shell.writeline(f"Alas, {arg} not found. Did you mean `guidance`?")
            return
        else:
            found_in = ", ".join([result.name for result in results])
            await shell.writeline(f"Found {arg} in {found_in}")
