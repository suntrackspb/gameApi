import json
import random
import time
import base64
from PIL import Image
from io import BytesIO
import requests

from main import data as loader


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Proxy-Authorization': 'Basic N2JuNjNwbWUtZms4cWJ2Zzpwc3llNmFjcXZo',
    'Connection': 'keep-alive',
    'Referer': 'https://fusionbrain.ai/diffusion',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'
}


def run_generate(prompt):
    print(prompt)
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(36)])
    content_type = f"multipart/form-data; boundary=---------------------------{random_number}"
    url = 'https://fusionbrain.ai/api/v1/text2image/run'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Proxy-Authorization': 'Basic N2JuNjNwbWUtZms4cWJ2Zzpwc3llNmFjcXZo',
        'Content-Type': content_type,
        'Origin': 'https://fusionbrain.ai',
        'Referer': 'https://fusionbrain.ai/diffusion',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    # Установка уникального разделителя
    boundary = f"---------------------------{random_number}"

    # Определение параметров запроса
    payload = [
        ("queueType", "generate"),
        ("query", prompt),
        ("preset", "1"),
        ("style", "in anime style")
    ]
    body = []
    for name, value in payload:
        body.append(b'--' + boundary.encode('ascii'))
        body.append(('Content-Disposition: form-data; name="' + name + '"').encode('ascii'))
        body.append(b'')
        body.append(value.encode('utf-8'))
    body.append(b'--' + boundary.encode('ascii') + b'--')
    body.append(b'')
    response = requests.post(url, headers=headers, data=b"\r\n".join(body))
    print(response.status_code)
    print(response.text)
    return json.loads(response.text)


def check_queue():
    url = 'https://fusionbrain.ai/api/v1/text2image/inpainting/checkQueue'
    response = requests.get(url, headers=headers)
    print(response.text)
    return json.loads(response.text)


def check_status(uid):
    url = f'https://fusionbrain.ai/api/v1/text2image/generate/pockets/{uid}/status'
    response = requests.get(url, headers=headers)
    print(response.text)
    return json.loads(response.text)


def get_image(uid):
    url = f'https://fusionbrain.ai/api/v1/text2image/generate/pockets/{uid}/entities'
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
    print(result['result'][0]['params'])
    return result


def save_image(data, tid):
    image_data = base64.b64decode(data['response'][0])
    img = Image.open(BytesIO(image_data))
    img.save(f"{tid}.png")
    print("===" * 15 + " File save: " + f"{tid}.png")


def generate_image(tld, desc):
    success = check_queue()
    if success['success']:
        generator = run_generate(desc)
        if generator['success']:
            pid = generator['result']['pocketId']
            while True:
                time.sleep(5)
                status = check_status(pid)
                if status['result'] == 'SUCCESS':
                    break
            data = get_image(pid)
            save_image(data['result'][0], tld)
    time.sleep(5)


for i in loader['stars']:
    generate_image(i['id'], i['star'])


