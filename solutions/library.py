import csv
from asyncio import timeout
from multiprocessing import Pool, cpu_count
import yt_dlp
import time

from _testcapi import error


def downloadvideo(url):
  try:
    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "nocheckcertificate": True,
        "socket_timeout": 30,
        "remote_components": "ejs:github",
        "js_runtimes": ["node"]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if timeout(ydl.download([url])): return {
            "url": url,
            "status": "OK",
            "error": "Download timeout"
        }
        else:
            ydl.download(url)
    return {
          "url": url,
          "status": "OK"
      }
  except Exception as e:
      return {
          "url": url,
          "status": "Failed",
          "error": "failed to download"
      }


# Note: on MAC install homebrew & run: brew install ffmpeg and then run brew install node (bash - node.js for jscript support)
def load_urls(path):
    urls = []
    with open(path, mode="r", encoding="utf-8") as videofile:
            reader = csv.reader(videofile)
            for row in reader:
                if len(row) > 1:
                    urls.append(row[1])
    return urls

def get_video_metadata(url):
    try:
        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "nocheckcertificate": True,
            "socket_timeout": 30,
            "remote_components": "ejs:github",
            "js_runtimes": {"node": {}},   # FIXED
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info     = ydl.extract_info(url, download=False)
                return{
                "url":url,
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "views": info.get("view_count"),
                "extension": info.get("ext"),
                "status": "OK",
                "error": ""
                }

    except Exception as e:
        return {
            "url":url,
            "status": "OK",
            "error": "failed to get metadata"
        }

def parallel_download(path, outputpath, outputmetadatapath):
    urls            = load_urls(path)
    metadatarows    =  []
    start           = time.perf_counter()

    with Pool() as pool:
        pool.map(downloadvideo, urls)
        end      = time.perf_counter()
        elapsed= round(end - start,2)

        print("downloading video took",elapsed,"seconds")

    with open(outputpath, mode="w", encoding="utf-8") as outputmetrics:
        outputmetrics.write(f"# Report\n"
        f"## Serial execution\n"
        f"Total time: {elapsed} seconds\n"
        f"## Complexity\n"
        f"Time complexity: O(n)\n"
        f"Space complexity: O(1)\n"
        f"Download status\n"
        f"Successful downloads: {urls} \n"
        f"Failed downloads:{urls}, {error} \n"
        )
    print("All videos downloaded successfully in: ", elapsed, "seconds")

    for url in urls:
        metadata = get_video_metadata(url)
        metadatarows.append(metadata)

    with open(outputmetadatapath, mode="w", encoding="utf-8", newline="") as csvfile:
        fieldnames = ["url", "title", "duration", "uploader", "views", "extension","status", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadatarows)

downloadvideo         = downloadvideo
load_urls             = load_urls
parallel_download = parallel_download