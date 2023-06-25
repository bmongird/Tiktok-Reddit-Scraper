import praw
import os
import io
import TTS
import random
import moviepy.editor
from pathlib import Path
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from moviepy.video.fx.crop import crop as moviecrop
from mutagen.mp3 import MP3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

service = ChromeDriverManager().install()

abs_path = Path().absolute()

reddit = praw.Reddit(
    client_id="id", #Enter your info here
    client_secret="secret",
    user_agent="name",
)

def texttospeech(index):
    voice = 'en_us_001' #You can change this -> see TTS.py for options
    file = f'text{index}.txt'
    session = 'session' 
    TTS.main(voice, file, session, index)
    ttsAudio = MP3(f"audio{index}.mp3")
    return ttsAudio.info.length


def clipEdit(audiolength, endTime, index):
    video = moviepy.editor.VideoFileClip('example.mp4').without_audio() #Insert the exact name of your mp4 file with the extension .mp4
    length = audiolength + MP3('silence.mp3').info.length
    if endTime == 0:
        startTime = random.uniform(120, video.duration - 600) #This means that the latest a video will start is 10 mins before the end, should be enough time to complete
    else:
        startTime = endTime
    endTime = startTime + length
    print(startTime, endTime)

    videoclip = video.subclip(startTime, endTime)
    originalw = videoclip.w # width of the clip
    h = 1080      
    w = int(h * (9/16)) + 1 
    #resizes the clip to a standard 9:16 aspect ratio
    videoclip = moviecrop(videoclip, width=w, height=h, x_center=originalw/2, y_center=h/2)
    audioclips = [moviepy.editor.AudioFileClip(f'audio{index}.mp3'), moviepy.editor.AudioFileClip('silence.mp3')]
    videoclip.audio = moviepy.editor.concatenate_audioclips(audioclips)
    
    image = Image.open(f'image{index}.png')
    height = image.height
    width = image.width
    size = int(w), int(((w * height / width)))
    while size[1] > 1080: #this resizes the image to fit on the video
        w -= 20
        size = int(w), int(w * height / width)
    print(size)
    image = image.resize(size, Image.ANTIALIAS) # fit onto video
    image.save(f'image{index}.png')
    startImageClip = moviepy.editor.ImageClip(f'image{index}.png').subclip(0, audiolength).set_pos(("center","center"))

    videoclip = moviepy.editor.CompositeVideoClip([videoclip, startImageClip])
    videoclip.write_videofile(f"clip{index}.mp4", codec='libx264', audio_codec='aac', ffmpeg_params=["-pix_fmt", "yuv420p"])
    return endTime


def concatenate_clips(nofclips, timesCalled): #concatenates all of the clips
    videosfile = open('video.txt', 'w')
    print("file cliptitle.mp4", file=videosfile)
    for n in range (nofclips):
        print(f"file clip{n}.mp4", file=videosfile)
    videosfile.close()
    os.system(f'ffmpeg -f concat -i {abs_path}/video.txt -c copy finishedClip{timesCalled}.mp4')
    os.remove(f'{abs_path}/video.txt')


def screenshot(posturl, index, id):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(service=Service(service), options=options)
    driver.get(posturl)
    driver.set_window_size(400, 1080)
    attempts = 0
    element = None
    print(id)
    print(posturl)
    while attempts < 3:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))
            element = driver.find_element(By.ID, id)
            attempts = 3
            print("Element found!")
        except:
            attempts += 1
            driver.refresh()
            print("Unable to locate element, trying again")
    if element == None:
        print("Never found element.")
        return False
    driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)

    img = Image.open(io.BytesIO(element.screenshot_as_png))
    img.save(f'image{index}.png')
    return True

def get_submission():
    j = False
    subreddit = reddit.subreddit("AskReddit") # Insert any subreddit you want
    for submission in subreddit.hot(limit=25): #this line changes which filter to use i.e #time_filter="all". Also, changes type of posts (subreddit.new, subreddit.top, etc.) See reddit API documentation for more info
        submission.comment_sort = 'best' #Default is best, can change, see reddit API docs
        if not submission.stickied: #Excludes stickied posts which are usually rules/other info abt subreddit
            with open('visited.txt') as file: #Records every visited post so that videos are not repeated
                for line in file:
                    if f'{submission.url}\n' == line:
                        j = True
                        break
                    else:
                        j = False
            if j == False:
                break
    if j == True:
        print("All submissions visited") #Will only print if you have combed all of the posts returned by the API call (can change where limit=25)
        exit()
    else:
        return submission


def main():
    submission = get_submission() #Should only have to call API once, this will get optimized
    if submission == 1:
        return 1
    file = open('visited.txt', 'a')
    print(submission.url, file=file)
    file.close()
    id = 't3_' + str(submission.id)
    returnValue = screenshot(str(submission.url), 'title', id)
    if submission.is_self and returnValue == True:
        titleFile = open("texttitle.txt", 'w')
        print(submission.title, file=titleFile)
        titleFile.close()
        print(submission.url)
        audiolength = texttospeech('title')

        starttime = clipEdit(audiolength, 0, 'title')
        titleFile.close()
        os.remove(f'{abs_path}/texttitle.txt')
        os.remove(f'{abs_path}/imagetitle.png')
        os.remove(f'{abs_path}/audiotitle.mp3')
        commenttree = submission.comments
        commentUrls = []
        commentIds = []
        x = 0
        for n in range(11): #Will attempt to fetch 11 comments total
            if not commenttree[n].stickied:
                commentUrls.append('https://reddit.com' + str(commenttree[n].permalink))
                commentIds.append('t1_' + str(commenttree[n].id))
                file = open(f'text{x}.txt', 'w')
                print(commenttree[n].body, file=file)
                file.close()
                x += 1
        #
        x = 0
        i = 0
        for comment in commentUrls:
            id = commentIds[i]
            returnValue = screenshot(comment, x, id)
            if returnValue == True:
                audiolength = texttospeech(x)
                if audiolength < 180: #This ignores any comments longer than 3 minutes as they become hard to read and extremely long/boring, but you can change this length
                    starttime = clipEdit(audiolength, starttime, x)
                    os.remove(f'{abs_path}/text{x}.txt')
                    os.remove(f'{abs_path}/image{x}.png')
                    os.remove(f'{abs_path}/audio{x}.mp3')
                    x += 1
                    i += 1
                else:
                    i += 1
            else:
                i += 1
        timesCalled = 0
        with open('timescalled.txt', 'r') as file:
            timesCalled = int(file.read()) - 1
        print(f"This script has been called a total of {timesCalled} times")
        with open('timescalled.txt', 'w') as file:
            print(timesCalled + 2, file=file) #Keeps track of the total number of times the program has been run to name videos correctly
        concatenate_clips(x, timesCalled)
        os.remove(f'{abs_path}/cliptitle.mp4')
        for i in range(0, x):
            os.remove(f'{abs_path}/clip{i}.mp4')

for i in range(1): #Change this number to the amount of videos you want, not exceeding the limit set above in get_submission
    main()

    





    
        
