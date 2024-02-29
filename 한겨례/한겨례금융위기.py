import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

base_url = "https://search.hani.co.kr/search/newslist?searchword=%EA%B8%88%EC%9C%B5%EC%9C%84%EA%B8%B0&startdate=2008.09.14&enddate=2008.11.14&page={}&sort=desc"  #객관적인 자료 확보를 위해 아무 검색 키워드 없이 정치 면 크롤링 (정치일반)

html_urls = []
for page in range(1,155):
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
        'div#container>div#contents-section.search-page>div.section-left>div#section-left-scroll-start>div#section-left-scroll-in>div.search-list.section-list-area>div.list>div.article-area>span.article-photo>a')
    for card in cards:
        article_url = card['href']
        urls.append(article_url)

##여기까지는 기사 잘 추출됨

#####################
# 전체 단어 빈도를 저장할 Counter 객체
total_word_counts = Counter()

okt = Okt()

for url in urls:
    response = requests.get(url)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 기사 본문 선택
    article_body_element = soup.select(
        'div#container>div#contents-article>div.article-body.type01>div.a-left>div#a-left-scroll-start>div#a-left-scroll-in>div.article-text>div.article-text-font-size>div.text')

    if article_body_element:
        # 특수 문자 제거 및 소문자 변환
        article_body = re.sub(r"[^\w\s]", "", str(article_body_element)).lower()

        # 명사 추출
        nouns = okt.nouns(article_body)

        ex.excluded_words.extend(["금융위기"])

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
plt.title("한겨레 금융위기 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("한겨례 금융위기 관련 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

# 사용자 입력 대기
input("Press Enter to exit...")