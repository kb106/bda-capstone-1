from pathlib import Path
import yt_dlp
from library import downloadvideo, readdownloadvideos

if __name__ == "__main__":
    Path("videos").mkdir(exist_ok=True)
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    downloadvideo(url)
    readdownloadvideos("../data/video_urls.csv", "../reports/sequential_report.md")



