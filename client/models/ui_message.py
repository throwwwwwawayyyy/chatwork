class UIMessage:
    content: str
    color: int
    keep_color_after_username: bool

    def __init__(self, content: str, color: int, keep_color_after_username: bool) -> None:
        self.content = content
        self.color = color
        self.keep_color_after_username = keep_color_after_username