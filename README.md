Please read the following before downloading:

### IMPORTANT: The project in its current state has been run and tested on MacOS, but is not designed to run on Windows (yet).

This is a project I undertook to hone my python skills and also to create something that generates content for TikTok/Instagram Reels. The world of TikTok was, and maybe currently still is (I'm unsure as I haven't been on it that much) polluted with reddit content similar to what is generated by this script. The idea is that these videos follow a certain formula and can be automatically created using this script.

This script will gather submissions from any subreddit using Reddit's API, and then proceed to create videos w/ TTS audio based on the submissions (posts) from this subreddit. The script uses the comments from the submissions as the main content, and thus it is optimal to use the subreddit r/AskReddit (or similar).

Thank you to [oscie57](https://github.com/oscie57) on github for the TTS script (TTS.py) that is used in my script. I've modified it to be able to run as an imported function within my own code, but most of the code is still the same.

# Usage:

First, make sure you have Python 3.9+ installed correctly on your system.

Also, this script uses ChromeDriver, so you must have the latest version of Chrome installed. Downloading ChromeDriver is unnecessary as the script will automatically download the latest version on startup.

## Required Libraries

The required libraries include PRAW, MoviePy, Selenium, Webdriver Manager, PIL, and Mutagen.

1. To install ffmpeg, a required dependency for MoviePy, open a terminal and enter the following command (MacOS):
`brew install ffmpeg`

2. To install the required libaries, open a terminal window and enter the following commands (1 per library):
```
pip install playsound requests
```
```
pip install praw
``` 
```
pip install moviepy
```
```
pip install selenium
```
```
pip install webdriver-manager
```
```
pip install pillow
```
```
pip install mutagen
```

Now that all of the required libraries and dependencies have been correctly installed, you can begin using the script.

## Initialization
In order to read NSFW posts, you must login to an 18+ Reddit account. However, because chrome directories may slightly vary from system to system (and I don't want to concern anyone by accessing these files through the script), you must first run redditInitializer.py to login to your reddit account. The chrome profile data folder is in the selenium folder, and the script only accesses the chrome data that is stored in this folder.

To run redditInitializer.py, open a command terminal and navigate to the folder in which your the folder tiktok_reddit_scraper is stored using cd commands. Execute the command
`python3 redditInitializer.py`
This will open reddit.com in a chrome window, in which you can login. Once you have logged in and the page has fully loaded, you can safely close the window.

## Script usage
You must first configure the script before using it. If you open script.py in any text editor, you will find a few commented lines in which I've indicated you input your own information/are able to modify numbers, etc. The first of these is the Reddit API client. 

### Reddit App Creation
To be able to access the API, you must register an app with Reddit. To do this, open [this](https://www.reddit.com/prefs/apps/) and press the "create another app" button. Fill out the name and a short description, and leave the about url and redirect url blank. Change the app to script and press create app. Now that you've created an app, you can see it listed on the same link as above, and if you press "edit", you'll see a bunch of information about the app. The ones that need to be plugged into the script are the secret, name, and id. The id is found at the top under "personal use script". Make sure to replace the text within the strings here: 
```
reddit = praw.Reddit(
    client_id="id", #Enter your info here
    client_secret="secret",
    user_agent="name",
)
```
with your own client id/secret/name.

A bit further down, you will see in the function "texttospeech" a variable titled "session". In order to call the TikTok TTS, you must input your session ID in that field. You can find instructions on how to do this [here](https://github.com/oscie57/tiktok-voice/wiki/Obtaining-SessionID).

The last required modification is obtaining a video to use. This video will serve as a background for the generated content. Most of the time on TikTok, it's either a Subway Surfers video or Minecraft video. I have not provided a video out of worry of copyright infringement/file size, but find a decently long video (I suggest 1hr+ in order to avoid too much repitition) and download it as an mp4. Place the mp4 into the tiktok_reddit_scraper folder and change the string in the `video = moviepy.editor.VideoFileClip(`example.mp4`).without_audio()` line to the name of your mp4. Note: you might have to try multiple different videos, as some crop better than others.

The script is now able to run! However, there are further modifications you can make if you so choose. These include changing the amount of videos generated, subreddit used, what to sort the subreddit by (hot, best, new), how many posts to fetch from the API, the TikTok voice used, etc. All of the lines where you can make modifications have comments on them (however, some lines w/ comments are there simply for reference and not for modification). Feel free to dig in and change these to your liking!

Finally, to run the script, open a command terminal, navigate to the tiktok_reddit_scraper folder using cd commands, and run the script by typing
`python3 script.py`.
The video will begin generating, and once it is finished, you will find your completed video/videos in the same folder as the script. They will be entitled "finishedClipx.mp4". Videos can take anywhere from 1-5 minutes to generate depending on your system and the length of the comments.

## Known issues
- The script makes an API call for every single video generated. This is because of an unoptimized section of code that I hope to fix in the near future. It was not a problem before (other than slowing the script down), but due to the new Reddit rules and costs associated with the API, the less calls, the better.
- Occasionally, ChromeDriver will spit out a random error. The first thing to always try is closing chrome and running the script again, as this seems to fix the issue.
- If the script crashes/is stopped while making the TikTok TTS call, a file named batch will be leftover in the main folder. If the script is run again with this folder present, it will continue to crash. Deleting the batch file will fix this issue. I plan on implementing a solution to this at some point.
- Extremely long comments will get cropped due to the window sizing of Chrome and how the script functions. This doesn't happen often (maybe once every 10 videos), but there is not a clean and easy solution. These comments are usually too long anyway and get boring fast as you finish reading them long before the TTS does.
- The TTS will read out links and emojis. I would love to implement some sort of checker to remove these links, but for now this remains.
- This is tested and working on MacOs Ventura on an M1 Macbook Pro, and should also work for Intel Macs. I have an ARM version of Windows 11 running on Parallels that I hope to be able to use to create another version for windows.
- I may have forgotten something under the usage header - please feel free to comment if you spot any issues or if I'm missing a library in the readme.
- I plan on implementing a GUI in the future for ease of use

Feel free to use this for your own projects/TikTok accounts. I ask that you credit me/my github.
