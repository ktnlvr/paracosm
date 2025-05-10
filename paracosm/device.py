from dataclasses import dataclass

from .locale import get


@dataclass
class File:
    name: str
    text: str

    @staticmethod
    def from_locale(name: str) -> 'File':
        text = get(name)
        return File(name, text)


class Device:
    def __init__(self, name):
        self.name = name
        self.files = {}

    def add_file_locale(self, name: str):
        file = File.from_locale(name)
        self.add_file(name, file)

    def add_file(self, name: str, file: File):
        self.files[name] = file

    def get_file(self, name: str) -> File | None:
        return self.files.get(name)

    def seek(self, text: str) -> list[File]:
        out = []
        for filename in self.files:
            file = self.files[filename]
            if text in file.text:
                out.append(file)
        return out
