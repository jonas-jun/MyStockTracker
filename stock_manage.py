from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta
import re

'''
Nov. 2020. by Junmai
'''

class stock_inform:
    
    def __init__(self):
        self.final = dict()
        self.date, self.name, self.code, self.today, self.rate, self.yday, self.start, self.low, self.high, \
        self.volumn, self.yvolumn, self.inst, self.foreign, self.f_rate = \
            list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
        self.krx_table = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
        
    def get_name(self, n):
        '기업명 하나씩 입력 받아서 self.name에 추가'
        self.name.append(n)
        # print(self.name)
        
    def get_names(self, n_list):
        '기업명 리스트를 입력 받아서 self.name에 추가'
        for i in n_list:
            self.name.append(i)
        # print(self.name)
        
    def get_code(self):
        'self.name의 기업들의 종목코드를 self.code에 추가'
        
        if self.name == list():
            raise ValueError("input stock names")
        
        for n in self.name:
            c = '{:06d}'.format(self.krx_table.loc[self.krx_table['회사명']==n, '종목코드'].item())
            self.code.append(c)
            
        code_dict = dict()
        for i in range(len(self.name)):
            code_dict[self.name[i]] = self.code[i]
        print('companies to get information')
        print(code_dict)
            
    def get_price(self):
        'self.code의 기업들의 당일 종가, 전일 종가, 저가, 고가, 거래량을 가져와 각각 리스트에 추가'
        
        for c in self.code:
            url = 'https://finance.naver.com/item/sise_day.nhn?code=' + c
            source = BeautifulSoup(requests.get(url).text, 'lxml')
            prices = source.find_all('span', {'class': 'tah p11'})
            today_, yday_, start_, high_, low_, volumn_, yvolumn_ = \
                prices[0], prices[5], prices[1], prices[2], prices[3], prices[4], prices[9]
            
            self.today.append(int(today_.get_text().replace(',', '')))
            self.yday.append(int(yday_.get_text().replace(',', '')))
            self.start.append(int(start_.get_text().replace(',', '')))
            self.low.append(int(low_.get_text().replace(',', '')))
            self.high.append(int(high_.get_text().replace(',', '')))
            self.volumn.append(int(volumn_.get_text().replace(',', '')))
            self.yvolumn.append(int(yvolumn_.get_text().replace(',', '')))
        print('가격정보 수집 완료')
            
    def get_sd(self):
        'self.code 기업들의 당일 매매동향(수급)을 각 리스트에 추가, sd: supply and demand'
        
        for c in self.code:
            url = 'https://finance.naver.com/item/frgn.nhn?code=' + c
            source = BeautifulSoup(requests.get(url).text, 'lxml')
            sd = source.find_all('td', {'class': 'num'})
            rate_, inst_, foreign_, f_rate_ = sd[14], sd[16], sd[17], sd[19]
            
            date_source = source.find_all('tr', {'onmouseover': 'mouseOver(this)'})
            self.date_ = datetime.strptime(date_source[0].find('td').get_text(), '%Y.%m.%d')
            
            self.rate.append(float(rate_.get_text().replace('%', '')))
            self.inst.append(int(inst_.get_text().replace(',', '')))
            self.foreign.append(int(foreign_.get_text().replace(',', '')))
            self.f_rate.append(float(f_rate_.get_text().replace('%', '')))
            self.date.append(self.date_.date())
        print('수급정보 수집 완료')
    
    def make_dict(self):
        cols = ['date', 'name', 'code', 'today', 'yday', 'rate', 'start', 'low', 'high', 'volumn', 'yvolumn',
               'inst', 'foreign', 'f_rate']
        data = [self.date, self.name, self.code, self.today, self.yday, self.rate, self.start, self.low, self.high, 
                self.volumn, self.yvolumn, self.inst, self.foreign, self.f_rate]
        
        for i in range(len(cols)):
            self.final[cols[i]] = data[i]
        
        return self.final
    
    def export_sheet(self):
        df = pd.DataFrame(self.final)
        df.to_excel('{}_mystocks.xlsx'.format(self.date_.date()), index=False)


class scrap_news:

    def __init__(self):
        self.final = dict()
        self.name = list()
        
    def get_name(self, n):
        '기업명 하나씩 입력 받아서 self.name에 추가'
        self.name.append(n)
        # print(self.name)
        
    def get_names(self, n_list):
        '기업명 리스트를 입력 받아서 self.name에 추가'
        for i in n_list:
            self.name.append(i)
        # print(self.name)
    
    def crawling(self, name, sort, start, end, maxpage):
        '기업명, 제목, 업로드일자, 언론사, 내용, 링크'
        max_ = (10*maxpage)-5
        base_url = 'https://search.naver.com/search.naver?&where=news&query={}&sort={}&nso=so:dd,p:from{}to{}&start='\
                    .format(name, sort, start, end)
        
        name_, title, date, media, content, link = list(), list(), list(), list(), list(), list()
        
        for i in range(1, max_, 10):
            web = requests.get(base_url+str(i))
            source = BeautifulSoup(web.text, 'lxml')
            
            # title
            title_list = source.find_all('a', {'class': 'news_tit'})
            for t in title_list:
                title.append(t.get_text())
                # link
                link.append(t.attrs['href'])
                # name
                name_.append(name)
                
            # content
            content_list = source.find_all('div', {'class': 'news_dsc'})
            for c in content_list:
                content.append(c.get_text())
                
            # media
            media_list = source.find_all('a', {'class': 'info press'})
            for m in media_list:
                media.append(m.get_text())
                
            # date
            date_list = source.find_all('span', {'class': 'info'})
            for d in date_list:
                if '면' not in str(d) and '단' not in str(d):
                    date.append(d.get_text())
                    
        
        result_dict = dict()
        result_dict['name'] = name_
        result_dict['title'] = title
        result_dict['date'] = date
        result_dict['media'] = media
        result_dict['content'] = content
        result_dict['link'] = link
        
        return result_dict

    def get_news(self, sort, start, end, maxpage=3):
        'self.name의 모든 기업들을 대상으로 크롤링 작업'
        self.final['name'], self.final['title'], self.final['date'], \
        self.final['media'], self.final['content'], self.final['link'] = \
        list(), list(), list(), list(), list(), list()
        
        for n in self.name:
            dict_ = self.crawling(name=n, sort=sort, start=start, end=end, maxpage=maxpage)
            self.final['name'] += dict_['name']
            self.final['title'] += dict_['title']
            self.final['date'] += dict_['date']
            self.final['media'] += dict_['media']
            self.final['content'] += dict_['content']
            self.final['link'] += dict_['link']
        print('기사 수집완료')
        return self.final

today = datetime.today().date() # for file name
ago_2 = today - timedelta(days=2)
today = re.sub('-', '', str(today))
ago_2 = re.sub('-', '', str(ago_2))

import sys
import os
folder = sys.path[0]

def export_multi_sheets(dicts, filename='{}_mystocks'.format(str(today))):
    f = filename + '.xlsx'
    with pd.ExcelWriter(f) as writer: # pylint: disable=abstract-class-instantiated
        for i in range(len(dicts)):
            pd.DataFrame(dicts[i]).to_excel(writer, index=False, sheet_name='sheet_{}'.format(str(i)))
    print('{}_mystocks.xlsx로 내보내기 완료'.format(str(today)))

def full_run(companies, start=ago_2, end=today, sort=1, maxpage=3):
    
    t1 = stock_inform()
    t1.get_names(companies)
    t1.get_code()
    t1.get_price()
    t1.get_sd()
    prices = t1.make_dict()

    t2 = scrap_news()
    t2.get_names(companies)
    news = t2.get_news(sort=sort, start=start, end=end, maxpage=maxpage)

    export_multi_sheets([prices, news])

#default parameters: 최근 3일 동안의 기사, 최신순(sort=1), 최대 3페이지
companies = ['두산중공업', '위세아이텍', '이엔드디', '셀트리온', '유니셈', 'DL이앤씨', 'DL', '와이엠티']
#full_run(companies=companies, start=20210112, sort=1, maxpage=3)

def only_news(companies, start=ago_2, end=today, sort=1, maxpage=3):
    t1 = scrap_news()
    t1.get_names(companies)
    news = t1.get_news(sort=sort, start=start, end=end, maxpage=maxpage)
    pd.DataFrame(news).to_excel(os.path.join(folder, '{}_stock_news.xlsx').format(str(today)), index=False)

only_news(companies, start=20210801, sort=1, maxpage=5)
