from multiprocessing import Pool
from pathlib import Path
import yt_dlp
from library import get_video_metadata, parallel_download

if __name__ == "__main__":
    Path("videos").mkdir(exist_ok=True)
    parallel_download("../data/video_urls.csv", "../reports/sequential_report.md" , "../data/video_metadata.csv")

