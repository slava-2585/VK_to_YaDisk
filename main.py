import requests
from pprint import pprint
from time import *
import json

from progress.bar import IncrementalBar
import yadisk
import vk_api

with open('token.txt', 'r') as file_object:
    token = file_object.readline().strip()
    token_ya = file_object.readline().strip()

version = '5.131'
dir = 'vk'

    
def get_photo (id, count):
    params = {
                'owner_id': id,
                'album_id': 'profile',
                'v':version,
                'extended': 1,
                'count': count
            }
    
    session = vk_api.VkApi(token=token)
    vk_photo = session.method('photos.get', params)['items']
    bar_download = IncrementalBar('Download Files VK', max = len(vk_photo))
    all_list_photo = []
    for photo in vk_photo:
        bar_download.next()
        list_photo = {}
        list_sort = sorted(photo['sizes'], key = lambda d: d['height'])
        list_photo['url'] = list_sort[-1]['url']
        list_photo['size'] = list_sort[-1]['type']
        if 'likes' in photo:
            list_photo['likes'] = photo['likes']['count']
        else:
            list_photo['likes'] = 0
        list_photo['date'] = photo['date']
        all_list_photo.append(list_photo)
    bar_download.finish()
        
    return all_list_photo
              
def upload_disk(list_ph=[], dir=''):
    bar_upload = IncrementalBar('Upload Files disk', max = len(list_ph))
    list_upload_file = []
    ya = yadisk.YaDisk(token=token_ya)
    if not ya.exists(dir):
        ya.mkdir(dir)
    for file in list_ph:
        bar_upload.next()
        dic_upload_file = {}
        name_photo = f'{dir}/{ctime(file["date"])}_{file["likes"]}.jpeg'
        ya.upload_url(file['url'], name_photo)
        dic_upload_file['file_name'] = name_photo
        dic_upload_file['size'] = file['size']
        list_upload_file.append(dic_upload_file)
    with open ('vk_photo.json', 'w') as f:
        json.dump(list_upload_file, f, indent=4)
    bar_upload.finish()
    print('Upload Finish')
    return list_upload_file

    
if __name__ == '__main__':
    my_id = '8792649'
    upload_disk(get_photo('1', 6), dir)    
    