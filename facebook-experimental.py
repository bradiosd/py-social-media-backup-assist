import fnmatch
import pathlib
import shutil
import requests
import json
import os
import glob
import click
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# load env
load_dotenv()

# cli args
# @click.command()
# @click.option('--rebuild-cache', default = True, help = 'Choose whether to rebuild cached html links')
# def rebuild_link_cache(rebuild_link_cache):
#   return rebuild_link_cache
    
# # main
# if __name__ == '__main__':
#   abc = rebuild_link_cache()
#   print(abc)

rebuild_link_cache = False
rebuild_asset_cache = False

# can be changed to webdav url if using remotely
root_path = os.getenv('SOCIALS_ROOT')
target_path = os.getenv('TARGET_SOCIALS_FOLDER')

cache_path = './cache/' + target_path

# video_find_base_path = root_path + '/_/facebook'
# thumbnail_find_base_path = root_path + '/_/facebook'
base_path = root_path + '/' + target_path
# video_index_file_path = base_path + '/photos_and_videos/your_videos.html'
# videos_path_prefix = base_path + '/photos_and_videos/videos'
# thumbnails_path_prefix = base_path + '/photos_and_videos/thumbnails'

# video_index_html_file = open(video_index_file_path, mode='r', encoding='utf-8')
# video_index_html = BeautifulSoup(video_index_html_file, 'html.parser')

# print('--- parsing html file "' + video_index_file_path + '"')

# create cache folder for target socials folder if it does not exist
if not os.path.exists(cache_path):
  os.mkdir(cache_path)

# build html cache with links from all html files
if rebuild_link_cache or not os.path.exists(cache_path + '/html.txt'):
  print('--- writing cache file for ' + cache_path + '/html.txt')
  for html_file in pathlib.Path(base_path).rglob('*.html'):
    print('--- writing url entry for ' + str(html_file.absolute()))
    cache_html_file = open(cache_path + '/html.txt', 'a+')
    cache_html_file.write(str(html_file.absolute()) + '\r')
    cache_html_file.close()
  print('--- created cache file for ' + cache_path + '/html.txt')

# iterate through links and get asset paths
if rebuild_asset_cache or not os.path.exists(cache_path + '/assets.txt'):
  cache_html_file = open(cache_path + '/html.txt')
  links = cache_html_file.readlines()
  cache_html_file.close()

  for link_i, link in enumerate(links):
    link = link.rstrip()
    file = open(link, mode='r', encoding='utf-8')
    html = BeautifulSoup(file, 'html.parser')
    file.close()
    
    images = html.find_all('img')
    videos = html.find_all('video') 
    assets = images + videos

    cache_html_file = open(cache_path + '/assets.txt', 'a+')
    
    for asset in assets:
      if not asset.has_attr('src'):
        continue
      if asset['src'].startswith('data:') or asset['src'].startswith('https:'):
        continue
      print('--- writing asset entry for ' + asset['src'])
      cache_html_file.write(asset['src'] + '\r')
      
    cache_html_file.close()
    
    print('--- link parsed ' + link)
      
    unique_lines = set(open(cache_path + '/assets.txt').readlines())
    asset_file = open(cache_path + '/assets.txt', 'w')
    asset_file.writelines(sorted(unique_lines))
    asset_file.close()
    print('--- created cache file for ' + cache_path + '/assets.txt')
  
# find files in consolidated directory
cache_html_file = open(cache_path + '/assets.txt')
assets = cache_html_file.readlines()
cache_html_file.close()

for asset_i, asset in enumerate(assets):
  filename = asset.rsplit('/', 1)[1].rstrip()
  path = asset.rsplit('/', 1)[0]
  asset_exists = os.path.exists(root_path + '/_/facebook/' + filename)
  
  if asset_exists:
    os.system('mv ' + root_path + '/_/facebook/' + filename + ' ' + base_path + '/' + path + '/' + filename)
    print('--- asset moved to target location "' + path + '/' + filename + '"')

# for path, subdirs, files in os.walk(base_path + '/photos_and_videos'):
  # print(files)
  # for name in fnmatch.filter(files, '.html'):
  #   print(name)

# print(base_path + '/photos_and_videos/videos/**/*.html')

# os.listdir()

# html_files = glob.glob(base_path + '/photos_and_videos/videos/**/*.html', recursive=True)

# for html_file in html_files:
#   print(html_file)

# # get raw videos

# # find all video links
# links = video_index_html.find_all('video')

# for link in links:
#   link_href = link.get('src')
  
#   if link_href.startswith('photos_and_videos'):
#     link_href_parts = link_href.split('/')
#     video_filename = link_href_parts[2]
#     target_path = base_path + '/photos_and_videos/videos/'
    
#     video_exists = os.path.exists(target_path + video_filename)
              
#     if video_exists:
#       print('--- video already exists so skipping "' + video_filename + '"')
#       continue
    
#     print('--- attempting to find video "' + video_filename + '"')
  
#     video_find_path = video_find_base_path + '/' + video_filename
#     video_found = os.path.exists(video_find_path)
        
#     if video_found != True:
#       print('--- video not found or possibly already moved to photo album "' + video_find_path + '"')
#     else:
#       os.system('mv ' + video_find_path + ' ' + target_path)
#       print('--- video moved to target location "' + video_filename + '"')
      
# # get thumbnails

# # find all video links
# thumbnails = video_index_html.find_all('img')

# for thumbnail in thumbnails:
#   link_href = thumbnail.get('src')
  
#   if link_href.startswith('photos_and_videos'):
#     link_href_parts = link_href.split('/')
#     thumbnail_filename = link_href_parts[2]
#     target_path = base_path + '/photos_and_videos/thumbnails/'
    
#     if thumbnail_filename.find('mp4') != -1:
#       print('--- thumbnail is an mp4 so skipping "' + thumbnail_filename + '"')
#       continue
    
#     thumbnail_exists = os.path.exists(target_path + thumbnail_filename)
              
#     if thumbnail_exists:
#       print('--- thumbnail already exists so skipping "' + thumbnail_filename + '"')
#       continue
    
#     print('--- attempting to find thumbnail "' + thumbnail_filename + '"')
  
#     thumbnail_find_path = thumbnail_find_base_path + '/' + thumbnail_filename
#     thumbnail_found = os.path.exists(thumbnail_find_path)
        
#     if thumbnail_found != True:
#       print('--- thumbnail not found or possibly already moved to photo album "' + thumbnail_find_path + '"')
#     else:
#       os.system('mv ' + thumbnail_find_path + ' ' + target_path)
#       print('--- thumbnail moved to target location "' + thumbnail_filename + '"')
