
# Scrap this idea
# While it's fully functional,
# it does not have much use.

from song_downloader import download_from_link, download_from_multi_links
from converter import convert
from config import Config
from logger import Logger
from pathlib import Path

class Interactive: 
    def __init__(self, config: Config):
        self.config = config
        self.logger = config.logger

    def intro(self):
        self.logger.info("""Welcome to interactive mode!

Here you can just enter a link, press enter, 
and it will automatically download it for you!
(All downloads will be placed in your current 
directory unless specified before)
To exit, type '.exit', and press enter.

        """)

    def start(self):
        self.intro()
        is_running = True
        while(is_running):
            usr_in = str(input("> "))        
            if usr_in.lower().startswith(".exit"):
                is_running = False
            elif usr_in.lower().startswith(".show"):
                if(len(usr_in.lower().split(" ")) > 1):
                    self.show(usr_in.lower().split(" ")[1:])
            elif usr_in.lower().startswith(".set"):
                if len(usr_in.split(" ")) > 2:
                    self.set(usr_in.split(" ")[1:])
            else:
                c = self.config
                if len(usr_in.split(" ")) > 1:
                    self.logger.verbose("Found multiple links", c.verbose)
                    link_list = usr_in.split(" ")
                    download_from_multi_links(link_list, c)
                    convert(c, c.out_format, c.workers)
                else:
                    self.logger.verbose("Single link found", c.verbose)
                    if(download_from_link(usr_in, c) == 0):
                        self.logger.verbose("Download return code 0", c.verbose)
                        convert(c, c.out_format, c.workers)

    def show(self, args):
        if(args[0] == "config"):
            self.logger.info("Showing current config")
            print(self.config.__str__())

    def set(self, args):
        if(args[0]."workers"):
            try:
                value = int(args[1])
                self.config.workers = value
                self.logger.success("Workers set to '{}'".format(self.config.workers))
            except ValueError:
                self.invalid(args[1], "Number value is required.")
        elif(args[0] == "verbose"):
            arg = args[1].lower()
            if(arg != "true" or arg != "false"):
                self.invalid(args[1], "true/false is required.")
            else:
                self.config.verbose = True if arg == "true" else False
                self.logger.success("Verbose set to '{}'".format(self.config.verbose))
        elif(args[0] == "export_path"):
            if not Path(args[1]).exists():
                self.invalid(args[1], "Provide an existing path.")
            else:
                self.config.export_path = args[1]
                self.logger.success("Export path set to '{}'".format(args[1]))

    def invalid(self, value, expect: str):
        self.logger.error("'{val}' is not a valid value. {expect}".format(val=value, expect=expect))
               