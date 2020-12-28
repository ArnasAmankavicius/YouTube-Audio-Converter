from logger import Logger
class Config(object):
    __slots__ = ["verbose", "logger", "export_path", "workers", "out_format"]

    # General configuration options
    def __init__(self, verbose: bool, export_path: str, workers: int, out_format: str):
        self.verbose = verbose
        self.logger = Logger()
        self.export_path = export_path
        self.workers = workers
        self.out_format = out_format