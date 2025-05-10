import os

lines = {}

for root, dirs, files in os.walk('./texts'):
    for file in files:
        with open(os.path.join(root, file)) as f:
            lines[file] = f.read()

def get(name: str) -> str:
    return lines[name]
