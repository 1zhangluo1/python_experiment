from scrapy.aiyiqi_scrapy import AiqiyiSpider

headers = {
    'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'''
}


def init_scrapy():
    _heat_rank = AiqiyiSpider(rank_name='热搜榜', route='/ranks1/1/0', headers=headers)
    _speed_rank = AiqiyiSpider(rank_name='飙升榜', route='/ranks1/1/-1', headers=headers)
    _must_watch_rank = AiqiyiSpider(rank_name='必看榜', route='/ranks1/1/-6', headers=headers)
    _high_score_rank = AiqiyiSpider(rank_name='高分榜', route='/ranks1/1/-4', headers=headers)
    return _heat_rank, _speed_rank, _must_watch_rank, _high_score_rank


if __name__ == '__main__':
    heat_rank, speed_rank, must_watch_rank, high_score_rank = init_scrapy()
    spiders = [heat_rank, speed_rank, must_watch_rank, high_score_rank]
    for spider in spiders:
        print(spider.full_url)
        spider.run()

