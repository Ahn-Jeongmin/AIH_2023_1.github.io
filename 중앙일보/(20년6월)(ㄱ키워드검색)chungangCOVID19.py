# 중앙일보 코로나 후
import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

html_urls = []

#한 번에 검색 결과 5000개까지만 표시, 1달씩 나누어서 크롤링
base_url = "https://www.joongang.co.kr/search/news?keyword=코로나&startDate=2020-06-01&endDate=2020-06-30&sfield=all&page={}"
for page in range(1,144):
    url = base_url.format(page)
    html_urls.append(url)

base_url = "https://www.joongang.co.kr/search/news?keyword=코로나&startDate=2020-07-01&endDate=2020-07-31&sfield=all&page={}"
for page in range(1,129):
    url = base_url.format(page)
    html_urls.append(url)

# 기사 미리보기 페이지에서 추출한 기사 목록 저장을 위한 빈 배열
urls = []
num=0
for url in html_urls:
    response = requests.get(url)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # URL 추출
    cards = soup.select(
        'div#wrapper>main#container>section.contents>div.row>section.chain_wrap.col_lg9>ul.story_list>li.card>div.card_body>h2.headline>a')
    for card in cards:
        article_url = card['href']
        urls.append(article_url)
        num+=1

#####################
# 전체 단어 빈도를 저장할 Counter 객체
total_word_counts = Counter()

okt = Okt()

for url in urls:
    response = requests.get(url)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 기사 본문 선택
    article_body_elements = soup.select(
        'div#wrapper>main#container>section.contents>article.article>div#article_body.article_body.fs3>p')
    for article_body_element in article_body_elements:
        # 특수 문자 제거 및 소문자 변환
        article_body = re.sub(r"[^\w\s]", "", str(article_body_element)).lower()

        # 명사 추출
        nouns = okt.nouns(article_body)

        ex.excluded_words.extend(["코로나","코로나바이러스"])

        # 단어 빈도 분석
        word_counts = Counter(word for word in nouns if word not in ex.excluded_words)

        # 단어 빈도를 전체 빈도에 누적
        total_word_counts += word_counts

# 가장 많이 등장한 단어 50개 추출
top_words = total_word_counts.most_common(50)

# 시각화를 위한 데이터 준비
labels, counts = zip(*top_words)
x = np.arange(len(labels))

# 막대 그래프 그리기
plt.bar(x, counts, align="center")
plt.xticks(x, labels)
plt.xlabel("단어")
plt.ylabel("빈도수")
plt.title("중앙일보 20년 6월 코로나19 키워드 검색 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("중앙일보 20년 6월 코로나19 지급 후 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")
print("총 분석 기사 수 :",num)
# 사용자 입력 대기
input("Press Enter to exit...")