from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func
import sys
import requests

def main():
  ytdlOpts = {
    'postprocessors': [{
      'key': 'FFmpegVideoConvertor',
      'preferedformat': 'mp4',
      }], 
    'force_keyframes_at_cuts': True, 
    'quiet': True, 
    'overwrites': True
    }
  url = input('\nPls enter URL...\n')
  try:
    response = requests.get(url)
    if not response.ok:
      pauseForLeave('@opening url fail')
      return
    if response.url != url:
      print('redirecting to ' + response.url)
    if 'https://www.youtube.com/watch?' not in response.url:
      pauseForLeave('@no valid video in url')
      return
  except Exception as ex:
    pauseForLeave('@opening url except\n' + str(ex))
    return
  isClip = input('\nDo you want to clip video? (y/n)\n*Notice: quality decline to clip precisely\n').upper()
  if isClip == 'Y':
    try:
      startSec = int(input('Pls enter number as start second...\n'))
      endSec = int(input('Pls enter number as end second...\n'))
      if startSec < 0 or endSec < 0:
        pauseForLeave('@negative number entered')
        return
      elif startSec >= endSec:
        pauseForLeave('@start time over end time')
        return
    except:
      pauseForLeave('@non number entered')
      return
    ytdlOpts.update({
      'download_ranges': download_range_func(None, [(startSec, endSec)])
      })
  elif isClip != 'N':
    pauseForLeave('@unexpected answer')
    return
  try:
    ytdl = YoutubeDL(ytdlOpts)
    #ytdl.download(url) #original method
    info = ytdl.extract_info(url)
    #fullFilename = ytdl.prepare_filename(info, warn=True) #other filename
    #tempFilename = ytdl.prepare_filename(info, 'temp') #other filename
    filename = ytdl.prepare_filename(info)
    pauseForLeave(f'{filename} is downloaded successfully')
    return 0
  except Exception as ex:
    pauseForLeave('@downloading except\n' + str(ex))
    return

def pauseForLeave(message):
  print('\n' + message)
  tmp = input('Pls press enter to close...\n')

main()
