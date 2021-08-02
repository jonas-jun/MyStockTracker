from bs4 import BeautifulSoup
import requests

class news_scraper:

    def __init__(self, corps):
        self.final = dict()
        self.name = corps
    
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

