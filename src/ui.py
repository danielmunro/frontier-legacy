from src.constants import Colors


class Button:
    def __init__(self, font, label):
        self.font = font
        self.label = label
        self.surface = self.font.render(
            f"Move Units",
            True,
            Colors.WHITE.value,
            Colors.BLACK.value,
        )
