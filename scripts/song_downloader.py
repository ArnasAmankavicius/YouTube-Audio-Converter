#USING pytube and moviepy
import pytube
import converter

from config import Config
from pathlib import Path
from multiprocessing import Pool

# Temporary class to enable multiprocessing down below
class DLConfig:
    __slots__ = ["link", "config"]

    def __init__(self, link: str, config: Config):
        self.link = link
        self.config = config

# Download from a specific file containing the list of links
def download_from_file(file_path: str, config: Config):
    logger = config.logger
    with open(file_path) as file:
        song_list = [i.strip() for i in file]
        song_list = [ 
            DLConfig(
                link=link,
                config=config
            ) for link in song_list
        ]
        logger.verbose("Starting download worker processes...", config.verbose)
        with Pool(processes=config.workers) as worker:
            worker.map(download, song_list)
    logger.verbose("Exiting download process.", config.verbose)


# Just a dumb wrapper around the download function
def download_from_link(link: str, config: Config):
    dlconfig = DLConfig(link, config)
    download(dlconfig)

# Download a video file from a single link
def download(dlconfig: DLConfig):
    try:
        logger = dlconfig.config.logger
        logger.info("Downloading " + dlconfig.link[:-1])
        yt = pytube.YouTube(dlconfig.link)
        audio_stream = yt.streams.get_audio_only()
        if not Path(dlconfig.config.yt_dl_path).exists():
            Path(dlconfig.config.yt_dl_path).mkdir(exist_ok=True)
        audio_stream.download(output_path=dlconfig.config.yt_dl_path)
        logger.success("Downloaded " + dlconfig.link[:-1])
    except Exception as e:
        logger.error("Download Failed:\n{}".format(e))


# os.chdir("downloaded_songs/")

'''
for file in glob.glob("*.mp4"):
    #print(file)
    try:
        video = AudioFileClip(file)
        file_mp3 = "../downloaded_songs_mp3/"+file[:-1]+"3"
        video.write_audiofile(file_mp3);
    except:
        print("mp3 conversion failed!")
'''