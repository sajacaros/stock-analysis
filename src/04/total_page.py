from bs4 import BeautifulSoup
import urllib.request as request
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
url = 'https://finance.naver.com/item/sise_day.naver?code=005380'
req = request.Request(url, headers=headers)
with request.urlopen(req) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('table', class_='Nnavi').find('td', class_='pgRR')
    last_page = str(pgrr.a['href']).split('=')[-1]

page_url = '{}&page={}'.format(url, 1)
req = request.Request(page_url, headers=headers)
with request.urlopen(req) as doc:
    print(pd.read_html(doc, header=0)[0])

df = pd.DataFrame()
for page in range(1, int(last_page) + 1):
    page_url = '{}&page={}'.format(url, page)
    req = request.Request(page_url, headers=headers)
    with request.urlopen(req) as doc:
        df = pd.concat([df, pd.read_html(doc, header=0)[0]])
    print(page, '...')
df = df.dropna()
print(df)