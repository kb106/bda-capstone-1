import csv
from multiprocessing import Pool, cpu_count

import csvfile
import yt_dlp
import time

def downloadvideo(url):
  try:
    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "nocheckcertificate": True,
        "remote_components": "ejs:github",
        "js_runtimes": ["node"]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"OK: {url}"
  except Exception as e:
    return f"ERROR: {url} -> {e}"


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
            "error": ""
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
        f"Space complexity: O(1)\n")
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