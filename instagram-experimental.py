import json
import os

from dotenv import load_dotenv

# load env
load_dotenv()

root_path = os.getenv('SOCIALS_ROOT')
target_path = os.getenv('TARGET_SOCIALS_FOLDER')

json_path = f'{root_path}/{target_path}/media.json'

with open(json_path, encoding='utf-8-sig') as json_file:
  data = json.load(json_file)
  
  json_keys = ['photos', 'videos', 'profile', 'stories', 'direct']
  
  for json_key in json_keys:
    if json_key in data:
      for asset in data[json_key]:
        filename = asset['path'].rsplit('/', 1)[1].rstrip()
        path = asset['path'].rsplit('/', 1)[0]
        existing_asset_path = f'{root_path}/_/instagram/{filename}'
        new_asset_path = f'{root_path}/{target_path}/{path}/{filename}'
        asset_exists = os.path.exists(existing_asset_path)
        
        if asset_exists:
          os.system(f'mv {existing_asset_path} {new_asset_path}')
          print(f'--- asset moved to target location {new_asset_path}')
