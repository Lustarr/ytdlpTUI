"""
https://www.youtube.com/watch?v=BaW_jenozKc
"""

from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func
import sys
import requests
import os

def main():
  # download options
  ytdlOpts = {
    'postprocessors': [{
      'key': 'FFmpegVideoConvertor',
      'preferedformat': 'mp4',
    }],
    'verbose': False,
    'force_keyframes_at_cuts': True,
    'quiet': True,
    'overwrites': True,
  }

  # processing url
  url = input('Pls enter URL...\n')
  try:
    response = requests.get(url)
    if not response.ok:
      print('\n@url fail')
      return
    if response.url != url:
      print('redirecting to ' + response.url)
    if 'https://www.youtube.com/watch?' not in response.url:
      print('\n@invalid url')
      return
  except Exception as ex:
    print('\n@url except\n' + str(ex))
    return

  # clip decision
  isClip = input(
    '\nDo you want to clip video? (y/n) *Notice: quality decline to clip precisely\n'
  ).upper()
  if isClip == 'Y':
    try:
      startSec = int(input('Pls enter positive integer as start second...\n'))
      endSec = int(input('Pls enter positive integer as end second...\n'))
      if startSec < 0 or endSec < 0:
        print('\n@negative number entered')
        return
      elif startSec >= endSec:
        print('\n@start second exceed end second')
        return
    except Exception as ex:
      print('\n@invalid number\n' + str(ex))
      return
    ytdlOpts.update(
      {'download_ranges': download_range_func(None, [(startSec, endSec)])})
  elif isClip != 'N':
    print('\n@unexpected answer')
    return

  # download action
  try:
    ytdl = YoutubeDL(ytdlOpts)
    print(
      '\n*Downloading now(the longer video is, the longer to wait)')
    # ytdl.download(url) #original method
    info = ytdl.extract_info(url)
    # fullFilename = ytdl.prepare_filename(info, warn=True) #other filename
    # tempFilename = ytdl.prepare_filename(info, 'temp') #other filename
    filename = ytdl.prepare_filename(info)
    print(f'\ndownload {filename} successfully')
    return
  except Exception as ex:
    print('\n@download except\n' + str(ex))
    return

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  except Exception as ex:
    print('\n' + f'main except {ex}')
  finally:
    tmp = input('\nPls press enter to close...\n')
