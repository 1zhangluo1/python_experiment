import os
import requests
from bs4 import BeautifulSoup
from scrapy.movie import Movie


class AiqiyiSpider:

    def __init__(self, rank_name, route, movies=None, headers=None, base_url='https://www.iqiyi.com'):
        self.base_url = base_url
        self.headers = headers
        self.movies = movies
        self.base_url = base_url
        self.full_url = base_url + route
        self.rank_name = rank_name
        self.result_dir = os.path.join('results')
        self.picture_dir = os.path.join('pictures', rank_name)
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
        if not os.path.exists(self.picture_dir):
            os.makedirs(self.picture_dir)

    def fetch_page(self):
        try:
            response = requests.get(self.full_url, headers=self.headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {self.full_url}: {e}")
            return None

    def parse_movie_info(self, html_text):
        movies = []
        soup = BeautifulSoup(html_text, 'html.parser')
        movie_infos = soup.select(
            '#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > div.rvi__list > a')
        for movie in movie_infos:
            heat = movie.select_one(
                '#__layout > div > div.ph-skin-wrap > div:nth-child(3) > div:nth-child(2) > div > '
                'div.rvi__list > a > div.rvi__right > div > span').text.strip()
            post = movie.select_one('div.rvi__img__box > picture').get('id')
            full_post_url = 'https:' + post
            content = movie.select_one('div.rvi__con')
            title = content.select_one('div.rvi__tit1').text.strip()
            filter = content.select_one('div.rvi__type1').text.strip()
            introduce = content.select_one('p').text.strip()
            single_movie = Movie(name=title, filter=filter, introduce=introduce, post=full_post_url, heat=heat)
            print(single_movie)
            movies.append(single_movie)
        self.movies = movies

    def replace_invalid_name(self,file_name):
        invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            file_name = file_name.replace(char, '_')
        return file_name

    def download_image(self):
        for movie in self.movies:
            image_url = movie.post
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                movie_name = self.replace_invalid_name(file_name=movie.name)
                picture_save_path = os.path.join(self.picture_dir, f"{movie_name}.jpg")
                with open(picture_save_path, 'wb') as file:
                    file.write(response.content)
                print(f"成功保存图片: {picture_save_path}")
            except requests.exceptions.RequestException as e:
                print(f"下载图片失败: {image_url}，错误: {e}")

    def save_movie(self):
        if self.movies is None:
            print("当前数据为空，不能进行保存")
            return
        file_name = self.rank_name + '.txt'
        file_path = os.path.join(self.result_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as result_file:
            for movie in self.movies:
                content = f"电影：{movie.name}\n人物：{movie.filter}\n介绍：{movie.introduce}\n海报路径：{movie.post}\n热度：{movie.heat}"
                result_file.write(content)
                result_file.write("\n\n")
                print(f"成功保存{movie.name}基本信息")

    def run(self):
        html_text = self.fetch_page()
        self.parse_movie_info(html_text=html_text)
        self.save_movie()
        self.download_image()

    def log_result(self):
        movies = self.movies
        if movies is None:
            print("当前结果为空")
            return
        for movie in movies:
            f"电影：{movie.name} 人物：{movie.filter} 介绍：{movie.introduce} 海报路径：{movie.post} 热度：{movie.heat}"
