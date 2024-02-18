from urllib.parse import urlencode
import requests
import os
import json



APP_ID = '51843593'
OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
params = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token'
}

oauth_url = f'{OAUTH_BASE_URL}?{urlencode(params)}'
print(oauth_url)

# https://api.vk.com/method/status.get?<PARAMS>

TOKEN = ''
class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method'
    def __init__(self, token, client_id):
        self.token = token
        self.client_id = client_id

    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'
    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.131'
        }

    def get_photo(self):
        params = self.get_common_params()
        params.update({'owner_id': self.client_id, 'album_id': 'profile', 'rev': 0, 'extended': 1, 'photo_sizes': 1})
        respones = requests.get(self._build_url('photos.get'), params=params)
        return respones.json()


    class YandexDiskAPI:
        API_URL = 'https://cloud-api.yandex.net/v1/disk'

        def __init__(self, token):
            self.token = token

        def create_folder(self, folder_name):
            headers = {
                'Authorization': f'OAuth {self.token}',
                'Content-Type': 'application/json'
            }
            data = {'path': folder_name}
            response = requests.put(f'{self.API_URL}/resources', headers=headers, json=data)
            return response.status_code

        def upload_file(self, file_path, destination_path):
            headers = {
                'Authorization': f'OAuth {self.token}'
            }

            params = {
                'path': destination_path,
                'overwrite': 'true'
            }

            with open(file_path, 'rb') as f:
                response = requests.put(f'{self.API_URL}/resources/upload', params=params, headers=headers,
                                        files={'file': f})

            return response.status_code

if __name__ == '__main__':
    vk_client = VKAPIClient(TOKEN, 17917323)
    vk_response = vk_client.get_photo()
    photos_info = []
    for item in vk_response['response']['items']:
        photo_info = {
            'id': item['id'],
            'owner_id': item['owner_id'],
            'sizes': item['sizes']
        }
        photos_info.append(photo_info)

    TOKENYD = ''

    yandex_disk_api = YandexDiskAPI(TOKENYD)


    folder_name = '/Новая папка'
    if yandex_disk_api.create_folder(folder_name) == 201:
        print(f'Папка "{folder_name}" успешно создана на Яндекс.Диске.')


        for photo in photos:
            max_size_url =
            response = requests.get(max_size_url)
            if response.status_code == 200:
                filename = f'{photo["likes"]["count"]}.jpg'
                with open(filename, 'wb') as f:
                    f.write(response.content)
                destination_path = os.path.join(folder_name, filename)
                if yandex_disk_api.upload_file(filename, destination_path) == 201:
                    print(f'Фотография "{filename}" успешно загружена в папку "{folder_name}" на Яндекс.Диск.')


                    photo_info = {
                        'filename': filename,
                        'url': max_size_url,
                        'likes_count': photo['likes']['count']

                    }
                    photos_info.append(photo_info)
                else:
                    print(f'Ошибка при загрузке фотографии "{filename}" на Яндекс.Диск.')
            else:
                print('Ошибка при загрузке фотографии с сервера VK.')

        with open('photos_info.json', 'w') as f:
            json.dump(photos_info, f, indent=4)
            print('Информация о фотографиях сохранена в файл "photos_info.json".')
    else:
        print(f'Ошибка при создании папки "{folder_name}" на Яндекс.Диск.')