import os
import time
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


from movie import Movie

url = 'https://www.iqiyi.com/ranks1/1/0'
robot_url = 'https://www.iqiyi.com/robots.txt'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}

results = []

def check_permission():
    rp = RobotFileParser()
    rp.set_url(robot_url)
    rp.read()
    if rp.can_fetch('''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36''', url):
        return True
    else:
        return False

def download_image(movies):
    if not os.path.exists('pictures1'):
        os.makedirs('pictures1')
    for movie in movies:
        image_url = movie.post
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            name = replace_invalid_name(movie.name)
            file_name = f"pictures1/{name}.jpg"
            with open(file_name, 'wb') as file:
                file.write(response.content)
                print(f'保存图片{movie.name}成功')
        except requests.exceptions.RequestException as e:
            print(f"下载图片失败: {image_url}，错误: {e}")


def save_movie(movies):
    with open('../result.txt', 'w', encoding='utf-8') as result_file:
        for movie in movies:
            content = f"电影：{movie.name}\n人物：{movie.filter}\n介绍：{movie.introduce}\n海报路径：{movie.post}\n热度：{movie.heat}"
            result_file.write(content)
            result_file.write("\n\n")
        print('保存电影信息完成')

def getData(html_text):
        movies = html_text.select(
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
        print(len(results))

def replace_invalid_name(file_name):
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        file_name = file_name.replace(char, '_')
    return file_name


def test_driver():
    driver = webdriver.Chrome()
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 向下滚动
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待加载更多内容
        time.sleep(2)
        # 计算新的滚动高度并与之前的高度比较
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # 如果新高度与最后高度相同，说明已经到达底部
        last_height = new_height  # 更新 last_height
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup

if __name__ == '__main__':
    isValid = check_permission()
    if isValid:
        html_text = test_driver()
        getData(html_text=html_text)
        save_movie(results)
        download_image(results)
    else:
        print('不允许爬')


