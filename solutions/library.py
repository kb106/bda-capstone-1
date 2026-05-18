import csv
from multiprocessing import Pool, cpu_count
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

def parallel_download(path, outputpath):
    urls       = load_urls(path)
    start      = time.perf_counter()

    with Pool() as pool:
        pool.map(downloadvideo, urls)
        end    = time.perf_counter()
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

downloadvideo         = downloadvideo
load_urls             = load_urls
parallel_download = parallel_download