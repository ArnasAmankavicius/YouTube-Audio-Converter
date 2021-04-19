#USING pytube and moviepy
import pytube
import converter

from pathlib import Path
from multiprocessing import Pool

from config import Config
from ytconfig import YTConfig

# Download from a specific file containing the list of links
def download_from_file(file_path: str, config: Config):
    logger = config.logger
    with open(file_path) as file:
        song_list = [i.strip() for i in file]
        song_list = [ 
            YTConfig(
                link=link,
                config=config
            ) for link in song_list
        ]
        start_process(song_list, config)

def download_from_multi_links(links: list, config: Config):
    logger = config.logger
    song_list = [
        YTConfig(
            link=link,
            config=config
        ) for link in links
    ]
    start_process(song_list, config)

# wrapper for the start process
def start_process(song_list: list, config: Config):
    config.logger.verbose("Starting download worker processes...", config.verbose)
    with Pool(processes=config.workers) as worker:
        worker.map(download, song_list)

# Just a dumb wrapper around the download function
def download_from_link(link: str, config: Config):
    config.logger.verbose("Starting link download...", config.verbose)
    download(YTConfig(link, config))

# Download a video file from a single link
def download(ytconfig: YTConfig):
    logger = ytconfig.config.logger
    output_path = ytconfig.config.export_path
    verbose_flag = ytconfig.config.verbose
    link = ytconfig.link
    try:
        yt = pytube.YouTube(link)
        logger.info("Downloading <= '{}'".format(yt.title))
        if not Path(output_path).exists():
            logger.verbose("'{}' path doesn't exist. Creating...", verbose_flag)
            Path(output_path).mkdir(exist_ok=True)
        yt.streams.first().download(output_path)
        logger.success("Downloaded : '{}'".format(yt.title))
    except Exception:
        logger.error("Download Failed: '{}' is an invalid link.".format(link))