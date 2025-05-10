class Expunger:
    def __init__(self):
        ...
    
    def expunge(self, text: str) -> str:
        return text.replace("␀", "█")
