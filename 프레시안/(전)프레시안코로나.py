import requests
from bs4 import BeautifulSoup

base_url = "https://www.pressian.com/pages/news-society-list?page={}"  #객관적인 자료 확보를 위해 아무 검색 키워드 없이 정치 면 크롤링 (정치일반)

html_urls = []
for page in range(491,532):
    url = base_url.format(page)
    html_urls.append(url)

# 기사 미리보기 페이지에서 추출한 기사 목록 저장을 위한 빈 배열
urls = []

for url in html_urls:

    response = requests.get(url)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # URL 추출
    cards = soup.select(
        'div#wrap>div#container>div.inner>div.section.list_arl_group>div.arl_022>ul.list>li>div.box>p.title>a')
    for card in cards:
        a = card['href']
        article_url="https://www.pressian.com"+a
        urls.append(article_url)

print(urls)