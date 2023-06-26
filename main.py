import requests
from pprint import pprint
import vk_api
import yadisk
from time import *
import json
from progress.bar import IncrementalBar

with open('token.txt', 'r') as file_object:
    token = file_object.readline().strip()
    token_ya = file_object.readline().strip()

version = '5.131'
url = 'https://api.vk.com/method/'
url_test = 'https://sun9-77.userapi.com/impf/zYNdlqs1MjZPPCwHOvD7b7gI5wQ9kCUeeHN-ow/-i2A_-ZO7GU.jpg?size=1280x1184&quality=96&sign=9a774e2eeced8aad7c41856e77b2ca2b&c_uniq_tag=C_NW9L8NEBuWHsSCuMWwz8kh6BqnOs6vt3PUcDc-f84&type=album'
dir = 'vk'

    
def get_photo (id):
    params = {
                'owner_id': id,
                'album_id': 'profile',
                'v':version,
                'extended': 1
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
              
def upload_disk(dict={}, dir='vk'):
    bar_upload = IncrementalBar('Upload Files disk', max = len(dict))
    list_upload_file = []
    ya = yadisk.YaDisk(token=token_ya)
    if not ya.exists(dir):
        ya.mkdir(dir)
    #ya.upload_url(url_test, 'vk/ya.jpeg')
    for file in dict:
        bar_upload.next()
        dic_upload_file = {}
        name_photo = f'{dir}/{ctime(file["date"])}_{file["likes"]}.jpeg'
        ya.upload_url(file['url'], name_photo)
        dic_upload_file['file_name'] = name_photo
        dic_upload_file['size'] = file['size']
        list_upload_file.append(dic_upload_file)
        with open ('vk_photo.txt', 'w') as f:
            json.dump(list_upload_file, f, indent=4)
    bar_upload.finish()
    print('Upload Finish')
    return list_upload_file

    
if __name__ == '__main__':
    my_id = '8792649'
    id_olga = '1173138'
    #pprint(get_photo(my_id))
    upload_disk(get_photo(my_id), dir)
    #upload_disk()
    
    