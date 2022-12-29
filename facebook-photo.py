import requests
import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# can be changed to webdav url if using remotely
root_path = os.getenv('SOCIALS_ROOT')

image_find_base_path = root_path + '/_/facebook'
base_path = root_path + '/facebook'
photo_index_file_path = base_path + '/photos_and_videos/your_photos.html'
album_path_prefix = base_path + '/photos_and_videos/album'

photo_index_html_file = open(photo_index_file_path, mode='r', encoding='utf-8')
photo_index_html = BeautifulSoup(photo_index_html_file, 'html.parser')

print('--- parsing html file "' + photo_index_file_path + '"')

album_count = 0

# find all album links
links = photo_index_html.find_all('a')

for link in links:
  link_href = link.get('href')
  
  if link_href.startswith('photos_and_videos/album'):
    album_count += 1
    
print('--- album links found "' + str(album_count + 1) + '"')
        
# find all image links per album and transfer to image_find_path
for album_number in range(album_count):
  album_html_file_path = album_path_prefix + '/' + str(album_number) + '.html'
  album_html_file = open(album_html_file_path, mode='r', encoding='utf-8')
  album_html = BeautifulSoup(album_html_file, 'html.parser')
  
  print('--- parsing html file "' + album_html_file_path + '"')
  
  links = album_html.find_all('a')
  
  for link in links:
    link_href = link.get('href')
    
    if link_href.startswith('photos_and_videos'):
      link_href_parts = link_href.split('/')
      album_id = link_href_parts[1]
      image_filename = link_href_parts[2]
      target_path = base_path + '/photos_and_videos/' + album_id + '/'
      
      image_exists = os.path.exists(target_path + image_filename)
            
      if image_exists:
        print('--- image already exists so skipping "' + album_id + '/' + image_filename + '"')
        continue
      
      print('--- attempting to find image "' + album_id + '/' + image_filename + '"')
    
      image_find_path = image_find_base_path + '/' + image_filename
      image_found = os.path.exists(image_find_path)
      
      
      if image_found != True:
        print('--- image not found "' + image_find_path + '"')
      else:
        os.system('mv ' + image_find_path + ' ' + target_path)
        print('--- image moved to target location "' + image_filename + '"')
