from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import List

class exchange_inform:

    def __init__(self, corps: List):
        self.corps = corps
        print('정보를 불러올 종목: ', corps)
        if not self.corps: raise ValueError ("기업을 입력해주세요")
    
    def get_code(self):
        source = pd.read_html('https://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
        def six_digits(code):
            return '{:06d}'.format(code)
        self.codes = list(map(six_digits, [source.loc[source['회사명'] == corp]['종목코드'].item() for corp in self.corps]))
        print('종목코드: ', self.codes)

    def get_price(self):
        
        self.rst = dict()

        for idx in range(len(self.codes)):
            corp = self.corps[idx]
            code = self.codes[idx]
            url = 'https://finance.naver.com/item/sise.nhn?code={}'.format(code)
            source = BeautifulSoup(requests.get(url).text, 'html.parser')
            table = source.find('table', {'class': 'type2 type_tax'})
            strong = table.find_all('strong')
            now_val = int(strong[0].get_text().replace(',', ''))
            #print('현재가: ', now_val)
            change_rate = float(strong[2].get_text().strip()[:-1])
            #print('등락율: ', change_rate)
            volume = int(table.find('span', {'id': '_quant'}).get_text().replace(',', ''))
            #print('거래량: ', volume)

            self.rst[corp] = [corp, code, now_val, change_rate, volume]
        
        print(' >> 오늘의 주가정보')
        for c in self.rst:
            print(c, self.rst[c])
        
        return self.rst

    def build_df(self):
        df = pd.DataFrame(self.rst).T
        df.columns = ['종목명', '종목코드', '현재가', '등락율', '거래량']
        print('주가 정보 DataFrame 생성 완료')
        return df

# for insert mode