import csv
import yt_dlp
import time

def downloadvideo(url):
    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "nocheckcertificate": True,
        # FIXES THE WARNING:
        # Downloads the required EJS challenge components automatically
        "remote_components": "ejs:github",

        # If using Node.js instead of Deno, uncomment the next line:
        # "js_runtimes": ["node"]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Note: on MAC install homebrew & run: brew install ffmpeg and then run brew install node (bash - node.js for jscript support)
def readdownloadvideos(path, outputpath):
    with open(path, mode="r", encoding="utf-8") as videofile:
        reader = csv.reader(videofile)
        for row in reader:
            if len(row) > 1:
                start = time.perf_counter()
                print("downloading video from...",row[1])
                ydl_opts = {
                    "outtmpl": "%(title)s.%(ext)s",
                    "nocheckcertificate": True
                }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(row[1])
            end         = time.perf_counter()
            elapsed     = end - start
            serial_time = round(elapsed,2)
            print("downloading video took",serial_time,"seconds")
    with open(outputpath, mode="w", encoding="utf-8") as outputmetrics:
        outputmetrics.write(f"# Report \n ## Serial execution \\n Total time: {serial_time} \n What is the time complexity and space complexity of downloading the videos one by one? \n\n ## Complexity \n\n Time complexity: 0(n) \n Space complexity: 0(1)")

downloadvideo         = downloadvideo
readdownloadvideos    = readdownloadvideos