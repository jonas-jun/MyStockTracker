# Stock Investing Management Program
  
by Junmai [github](https://github.com/jonas-jun/stock_management), 2020-11-14
2021-08-03 major update
- existing stock price scraper did not work well, because 'naver.com/sise_day' pages might be changed not to be scrapped.
- the new program scrap stock informs from 'naver.com/sise' pages  
***
Code Description
-----------
## price_inform.py
get stock information: price, volume, rate, code

## scrap_news.py
get news information from Naver news.
- start, end: start date and end date (defualt: 3 days ago to today)
- sort: {0: reliable, 1: latest}
- max_page: how many pages (Naver news) to scrap?

## main.py
run all.  
- --start
- --end
- --sort
- --max_page

'NAVER 카카오 삼성전자' (split by a space)  

## How to run?
[example]  NAVER, 카카오, 삼성전자의 현재가(오늘 종가) 및 8월 1일 ~ 8월 3일 네이버뉴스 (최신순) 최대 3페이지까지 크롤링  
python main.py --start 20210801 --end 20210803 --sort 1 --max_page 3  
"상장 기업명을 space로 구분하여 정확하게 입력해주세요"  
NAVER 카카오 삼성전자   


---------
[outdated version]  

### _class stock_inform_ 
  get stock information: price, volumn, supply and demand, and so on.  
  **[example]** after market on 2020-11-13

![image_stock.jpg](./img/image_stock.jpg)
  
### _class scrap_news_
  get news information from Naver news. (start date to end date)  
  **[example]** maxpage=30, in late 2days, sorting=1 (from new ones to old ones)
    
    name, title, date, media, summary, link
![image_news.jpg](./img/image_news.jpg)
  
### _def full_run_
  1. debug all process.
  1. make xlsx file.

## How to Run?

companies = ['두산중공업', '세아제강', '위세아이텍', '이엔드디', '솔트룩스']  
full_run(companies=companies, start=20201111, end=20201114, maxpage=3)  
  
**[example]**
![image_run](./img/image_run.jpg)


```python

```
