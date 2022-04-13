from bs4 import BeautifulSoup
import urllib.request as request
import pandas as pd
import mplfinance as mpf

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
url = 'https://finance.naver.com/item/sise_day.naver?code=005380'
req = request.Request(url, headers=headers)
with request.urlopen(req) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('table', class_='Nnavi').find('td', class_='pgRR')
    last_page = str(pgrr.a['href']).split('=')[-1]

df = pd.DataFrame()
for page in range(1, int(last_page) + 1):
    page_url = '{}&page={}'.format(url, page)
    req = request.Request(page_url, headers=headers)
    with request.urlopen(req) as doc:
        df = pd.concat([df, pd.read_html(doc, header=0)[0]])
    print(page, '...')
df = df.dropna()
df = df.iloc[0:30]
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, title='Hyundai Car candle chart', type='candle', style=s)

mpf.plot(df, title='Hyundai Car ohlc chart', type='ohlc')

kwargs = dict(title='Hyundai Car customized chart', type='candle', mav=(2,4,6), volume=True, ylabel='ohlc candles')
mpf.plot(df, **kwargs, style=s)
