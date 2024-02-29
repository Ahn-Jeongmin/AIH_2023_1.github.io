#동아일보 코로나19 정치
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

base_url = "https://www.donga.com/news/Economy/List?p={}&prod=news&ymd={}&m="
# 페이지 범위 설정 (1부터 5까지)
start_page = 1
end_page = 5

# 날짜 범위 설정
start_date = 20200601
end_date = 20200630

# 반복문을 사용하여 웹 쿼리 생성
for date in range(start_date, end_date + 1):
    for page in range(start_page, end_page + 1):
        # 웹 쿼리 생성
        url = base_url.format((page-1)*20+1, date)
        html_urls.append(url)

# 날짜 범위 설정
start_date = 20200701
end_date = 20200731

# 반복문을 사용하여 웹 쿼리 생성
for date in range(start_date, end_date + 1):
    for page in range(start_page, end_page + 1):
        # 웹 쿼리 생성
        url = base_url.format((page-1)*20+1, date)
        html_urls.append(url)



# 기사 미리보기 페이지에서 추출한 기사 목록 저장을 위한 빈 배열
urls = []
#분석 대상 기사 수
num=0

for url in html_urls:
    response = requests.get(url)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # URL 추출
    cards = soup.select(
        'div#dongawrap > div#container.etcCon.etcPage > div#content > div.articleList.article_list > div.thumb > a')
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
    article_body_element = soup.select_one('div#dongawrap >div#view.open_view>div#container.view_wrap>div#content>div.scroll_start01>div.scroll_start01_in>div.article_view>div#article_txt.article_txt')

    if article_body_element:
        # 특수 문자 제거 및 소문자 변환
        article_body = re.sub(r"[^\w\s]", "", str(article_body_element)).lower()

        # 명사 추출
        nouns = okt.nouns(article_body)

        ex.excluded_words.extend(["코로나","코로나바이러스"])

        # 단어 빈도 분석
        word_counts = Counter(word for word in nouns if word not in ex.excluded_words)

        # 단어 빈도를 전체 빈도에 누적
        total_word_counts += word_counts

# 가장 많이 등장한 단어 30개 추출
top_words = total_word_counts.most_common(50)

# 시각화를 위한 데이터 준비
labels, counts = zip(*top_words)
x = np.arange(len(labels))

# 막대 그래프 그리기
plt.bar(x, counts, align="center")
plt.xticks(x, labels)
plt.xlabel("단어")
plt.ylabel("빈도수")
plt.title("동아일보 코로나19 <20년 6월-경제> 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

print("총 분석 기사 수 :",num)

# 사용자 입력 대기
input("Press Enter to exit...")