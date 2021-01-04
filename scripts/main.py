import os
import sys
import argparse
sys.path.append(os.path.dirname(__file__)) # Temporary fix for the ModuleNotFoundError for custom modules

import click
from validators import url
from converter import convert as conv
from pathlib import Path
from config import Config
from conversionjob import ConversionJob
from song_downloader import download_from_link, download_from_file, download_from_multi_links
from logger import Logger

from __info__ import __version__, __epilog__, __description__

def setupParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__description__, 
        epilog=__epilog__)
    parser.add_argument('--version', action='version', version="%(prog)s {}".format(__version__), help='Display version information.')
    parser.add_argument('links', type=str, help='Specify a file or a link (in quotes) to download from. You can specify multiple links seperated by spaces.')
    parser.add_argument('-w', dest='workers', default=5, type=int, help='Amount of processes to create for audio conversion (default: 5).')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose for debugging purposes.')
    parser.add_argument('-e', dest="export_path", type=str, help='Path where to convert the downloaded video files.')
    return parser.parse_args()

# Paste the link
def convert():
    args = setupParser()

    logger = Logger()
    verbose_flag = args.verbose_flag
    
    logger.verbose("Checking if export path has been specified", verbose_flag)
    if args.export_path == None:
        logger.warn("No export path as been specified. Using '{}'...".format(os.getcwd()))

    logger.verbose("Creating a config class...", verbose_flag)
    c = Config(
        verbose=verbose_flag,
        export_path=args.export_path if args.export_path != None else os.getcwd(),
        workers=args.workers,
        out_format=".mp3"
    )
    
    link_file = args.links.split(" ") if len(args.links.split(" ")) > 1 else args.links

    logger.verbose("Input : {}".format(link_file), verbose_flag)
    logger.verbose("Output : {}".format(c.export_path), verbose_flag)
    logger.verbose("Workers : {}\n".format(c.workers), verbose_flag)
    
    logger.verbose("Checking provided input validity...", verbose_flag)
    if isinstance(link_file, list):
        logger.verbose("Multiple links detected!", verbose_flag)
        for link in link_file:
            logger.verbose("Checking link '{}'...".format(link), verbose_flag)
            if not url(link):
                logger.error("'{}' is an invalid link.".format(link))
                link_file.remove(link)
        if len(link_file) <= 0:
            logger.error("No valid links were specified. Exiting...")
            exit(2)
        logger.verbose("Downloading from multiple links.", verbose_flag)
        download_from_multi_links(links=link_file, config=c)
    elif url(link_file):
        logger.verbose("'{}' is a valid URL".format(link_file), verbose_flag)
        download_from_link(link=link_file, config=c)
    else:
        if os.path.isfile(link_file):
            logger.verbose("'{}' is a valid file".format(link_file), verbose_flag)
            download_from_file(file_path=link_file, config=c)
        else:
            logger.error("Invalid file path '{}'. Exiting...".format(link_file))
            exit(1)
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    logger = None

    conv(config=c, output_format=c.out_format, workers=c.workers)
