import requests
from pprint import pprint
import vk_api

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

version = '5.131'
url = 'https://api.vk.com/method/'

    
def get_photo (id):
    params = {
                'owner_id': id,
                'album_id': 'profile',
                'v':'5.131'
            }
    
    #res = requests.get(url=url+'photos.get', params=params).json()
    session = vk_api.VkApi(token=token)
    #vk = session.get_api()
    vk_photo = session.method('photos.get', params)['items']
    list_url = []
    #for photo in vk_photo:
    #list_url =  [ i['url'] if i['type'] == 'w' for photo in vk_photo for i in photo['sizes'] ]
    for photo in vk_photo:
        list_sort = sorted(photo['sizes'], key = lambda d: d['height'])
        list_url.append(list_sort[-1]['url'])
            
    print (len(list_url))
    #return list_url
    
if __name__ == '__main__':
    my_id = '8792649'
    pprint(get_photo(my_id))
    