from config import Config

class YTConfig:
    __slots__ = ["link", "config"]
    def __init__(self, link: str, config: Config):
        self.link = link
        self.config = config