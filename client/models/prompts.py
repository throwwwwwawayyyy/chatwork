class Prompt:
    content: str
    color: int
    keep_color: bool

    def __init__(self, content: str, color: int, keep_color: bool) -> None:
        self.content = content
        self.color = color
        self.keep_color = keep_color