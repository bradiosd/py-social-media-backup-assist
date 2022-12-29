import requests
import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# can be changed to webdav url if using remotely
root_path = os.getenv('SOCIALS_ROOT')

video_find_base_path = root_path + '/_/facebook'
thumbnail_find_base_path = root_path + '/_/facebook'
base_path = root_path + '/facebook'
video_index_file_path = base_path + '/photos_and_videos/your_videos.html'
videos_path_prefix = base_path + '/photos_and_videos/videos'
thumbnails_path_prefix = base_path + '/photos_and_videos/thumbnails'

video_index_html_file = open(video_index_file_path, mode='r', encoding='utf-8')
video_index_html = BeautifulSoup(video_index_html_file, 'html.parser')

print('--- parsing html file "' + video_index_file_path + '"')

# get raw videos

# find all video links
links = video_index_html.find_all('video')

for link in links:
  link_href = link.get('src')
  
  if link_href.startswith('photos_and_videos'):
    link_href_parts = link_href.split('/')
    video_filename = link_href_parts[2]
    target_path = base_path + '/photos_and_videos/videos/'
    
    video_exists = os.path.exists(target_path + video_filename)
              
    if video_exists:
      print('--- video already exists so skipping "' + video_filename + '"')
      continue
    
    print('--- attempting to find video "' + video_filename + '"')
  
    video_find_path = video_find_base_path + '/' + video_filename
    video_found = os.path.exists(video_find_path)
        
    if video_found != True:
      print('--- video not found or possibly already moved to photo album "' + video_find_path + '"')
    else:
      os.system('mv ' + video_find_path + ' ' + target_path)
      print('--- video moved to target location "' + video_filename + '"')
      
# get thumbnails

# find all video links
thumbnails = video_index_html.find_all('img')

for thumbnail in thumbnails:
  link_href = thumbnail.get('src')
  
  if link_href.startswith('photos_and_videos'):
    link_href_parts = link_href.split('/')
    thumbnail_filename = link_href_parts[2]
    target_path = base_path + '/photos_and_videos/thumbnails/'
    
    if thumbnail_filename.find('mp4') != -1:
      print('--- thumbnail is an mp4 so skipping "' + thumbnail_filename + '"')
      continue
    
    thumbnail_exists = os.path.exists(target_path + thumbnail_filename)
              
    if thumbnail_exists:
      print('--- thumbnail already exists so skipping "' + thumbnail_filename + '"')
      continue
    
    print('--- attempting to find thumbnail "' + thumbnail_filename + '"')
  
    thumbnail_find_path = thumbnail_find_base_path + '/' + thumbnail_filename
    thumbnail_found = os.path.exists(thumbnail_find_path)
        
    if thumbnail_found != True:
      print('--- thumbnail not found or possibly already moved to photo album "' + thumbnail_find_path + '"')
    else:
      os.system('mv ' + thumbnail_find_path + ' ' + target_path)
      print('--- thumbnail moved to target location "' + thumbnail_filename + '"')
