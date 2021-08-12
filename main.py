import sys, re
from typing import List
from price_inform import exchange_inform
from scrap_news import news_scraper
from datetime import datetime, timedelta
import pandas as pd
import argparse

def export_multi_sheets(df_list: List, filename: str):
    f = filename + '.xlsx'
    with pd.ExcelWriter(f) as writer: # pylint: disable=abstract-class-instantiated
        for i in range(len(df_list)):
            df_list[i].to_excel(writer, index=False, sheet_name='sheet_{}'.format(str(i)))
    print(' >> {}로 내보내기 완료'.format(f))


if __name__ == '__main__':
    welcome = '''
    ====================
    Stock Tracker has been run
    code by Junmay
    https://github.com/jonas-jun/stock_management
    ====================
    '''

    print(welcome)

    today = datetime.today().date()
    today_str = re.sub('-', '', str(today))
    ago_3 = today - timedelta(days=3)
    ago_3_str = re.sub('-', '', str(ago_3))

    parser = argparse.ArgumentParser()
    #parser.add_argument('--corps', type=str, default='NAVER 위세아이텍 이엔드디 라온피플 그린플러스') # NAVER 위세아이텍 이엔드디 라온피플 그린플러스
    parser.add_argument('--start', type=int, default=ago_3_str) # 20210801
    parser.add_argument('--end', type=int, default=today_str) # 20210803
    #parser.add_argument('--path_chrome', type=str, default='/Users/jonas/github/N_shop_scraper/chromedriver')
    parser.add_argument('--sort', type=int, default=1) # 1: 최신순
    parser.add_argument('--max_page', type=int, default=3) # 네이버에서 검색시 최대 0페이지의 기사 크롤링
    args = parser.parse_args()

    print("상장 기업명을 space로 구분하여 정확하게 입력해주세요. ex) NAVER 카카오 삼성전자 라온피플 그린플러스")
    inputs = sys.stdin.readline().split()

    c = exchange_inform(inputs)
    c.get_code()
    result_dict = c.get_price()
    price_df = c.build_df()

    news = news_scraper(inputs)
    news_dict = news.get_news(sort=args.sort, start=args.start, end=args.end, maxpage=args.max_page)
    news_df = pd.DataFrame(news_dict)

    file_name = '{}_mystocks'.format(today_str)
    export_multi_sheets(df_list=[price_df, news_df], filename=file_name)