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
    'force_keyframes_at_cuts': True
    }
  url = input('\nPls enter URL...\n')
  try:
    response = requests.get(url)
    if not response.ok:
      pauseAndLeave('@opening url fail')
      return
    if response.url != url:
      print('redirecting to ' + response.url)
    if 'https://www.youtube.com/watch?' not in response.url:
      pauseAndLeave('@no valid video in url')
      return
  except Exception as ex:
    pauseAndLeave('@opening url except\n' + str(ex))
    return
  isClip = input('\nDo you want to clip video? (y/n)\n*Notice: quality decline to clip precisely\n').upper()
  if isClip == 'Y':
    try:
      startSec = int(input('Pls enter number as start second...\n'))
      endSec = int(input('Pls enter number as end second...\n'))
      if startSec < 0 or endSec < 0:
        pauseAndLeave('@negative number entered')
        return
      elif startSec >= endSec:
        pauseAndLeave('@start time over end time')
        return
    except:
      pauseAndLeave('@non number entered')
      return
    ytdlOpts.update({
      'download_ranges': download_range_func(None, [(startSec, endSec)])
      })
  elif isClip != 'N':
    pauseAndLeave('@unexpected answer')
    return
  ytdl = YoutubeDL(ytdlOpts)
  ytdl.download(url)

def pauseAndLeave(message):
  print('\n' + message)
  tmp = input('Pls press enter to close...\n')

main()
