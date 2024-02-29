import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

def plot_top_words(total_word_counts, category):
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
    plt.title("한겨레 코로나 관련 기사 단어 빈도수 분석")
    plt.show()

    # 결과 출력
    print("한겨례 코로나 관련 기사 중 가장 많이 등장한 단어 50개:")
    for word, count in top_words:
        print(f"{word}: {count}")






plt.rc("font", family="Malgun Gothic")

base_url = "https://www.hani.co.kr/arti/politics/politics_general/{}.html"

poli_total_word_counts = Counter()
eco_total_word_counts = Counter()
soci_total_word_counts = Counter()

okt = Okt()

html_urls = []
for page in range(919105,922773):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x=soup.select('div#container>div#contents-article>div#article_view_headline.article-head>p.category>strong>a')

    for element in x:
        href = element['href']
    if (href=='/arti/society/home01.html'):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 기사 본문 선택
        article_body_element = soup.select(
            'div#container>div#contents-article>div.article-body.type01>div.a-left>div#a-left-scroll-start>div#a-left-scroll-in>div.article-text>div.article-text-font-size>div.text')
        if article_body_element:
            # 특수 문자 제거 및 소문자 변환
            article_body = re.sub(r"[^\w\s]", "", str(article_body_element)).lower()

            # 명사 추출
            nouns = okt.nouns(article_body)

            ex.excluded_words.extend(["코로나","코로나바이러스"])

            # 단어 빈도 분석
            word_counts = Counter(word for word in nouns if word not in ex.excluded_words)

            # 단어 빈도를 전체 빈도에 누적
            soci_total_word_counts += word_counts


    elif (href=='/arti/politics/home01.html'):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 기사 본문 선택
        article_body_element = soup.select(
            'div#container>div#contents-article>div.article-body.type01>div.a-left>div#a-left-scroll-start>div#a-left-scroll-in>div.article-text>div.article-text-font-size>div.text')
        if article_body_element:
            # 특수 문자 제거 및 소문자 변환
            article_body = re.sub(r"[^\w\s]", "", str(article_body_element)).lower()

            # 명사 추출
            nouns = okt.nouns(article_body)

            ex.excluded_words.extend(["코로나","코로나바이러스"])

            # 단어 빈도 분석
            word_counts = Counter(word for word in nouns if word not in ex.excluded_words)

            # 단어 빈도를 전체 빈도에 누적
            poli_total_word_counts += word_counts


    elif(href=='/arti/economy/home01.html'):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 기사 본문 선택
        article_body_element = soup.select(
            'div#container>div#contents-article>div.article-body.type01>div.a-left>div#a-left-scroll-start>div#a-left-scroll-in>div.article-text>div.article-text-font-size>div.text')
        if article_body_element:
            # 특수 문자 제거 및 소문자 변환
            article_body = re.sub(r"[^\w\s]", "", str(article_body_element)).lower()

            # 명사 추출
            nouns = okt.nouns(article_body)

            ex.excluded_words.extend(["코로나","코로나바이러스"])

            # 단어 빈도 분석
            word_counts = Counter(word for word in nouns if word not in ex.excluded_words)

            # 단어 빈도를 전체 빈도에 누적
            eco_total_word_counts += word_counts



plot_top_words(poli_total_word_counts, "정치")
plot_top_words(eco_total_word_counts,"경제")
plot_top_words(soci_total_word_counts,"사회")


# 사용자 입력 대기
input("Press Enter to exit...")
