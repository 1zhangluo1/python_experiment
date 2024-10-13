import os
import requests
from bs4 import BeautifulSoup
from movie import Movie

url = 'https://www.iqiyi.com/ranks1/1/0'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}

results = []

def download_image(movies):
    if not os.path.exists('pictures1'):
        os.makedirs('pictures1')
    for movie in movies:
        image_url = movie.post
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            file_name = f"pictures1/{movie.name}.jpg"
            with open(file_name, 'wb') as file:
                file.write(response.content)
        except requests.exceptions.RequestException as e:
            print(f"下载图片失败: {image_url}，错误: {e}")


def save_movie(movies):
    with open('../result.txt', 'w', encoding='utf-8') as result_file:
        for movie in movies:
            content = f"电影：{movie.name}\n人物：{movie.filter}\n介绍：{movie.introduce}\n海报路径：{movie.post}\n热度：{movie.heat}"
            result_file.write(content)
            result_file.write("\n\n")

def getData(url,header):
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.select(
            '#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a')
        for movie in movies:
            heat = movie.select_one('#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > '
                                    'div.rvi__list > a > div.rvi__right > div > span').text.strip()
            post = movie.select_one('div.rvi__img__box > picture').get('id')
            full_post_url = 'https:' + post
            content = movie.select_one('div.rvi__con')
            title = content.select_one('div.rvi__tit1').text.strip()
            filter = content.select_one('div.rvi__type1').text.strip()
            introduce = content.select_one('p').text.strip()
            single_movie = Movie(name=title, filter=filter, introduce=introduce, post=full_post_url, heat=heat)
            results.append(single_movie)
            print(single_movie)
        print("爬取完成")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        
getData(url=url, header=headers)
save_movie(results)
download_image(results)


