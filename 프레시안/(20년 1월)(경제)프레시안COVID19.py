import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

urls=['https://www.pressian.com/pages/articles/284698', 'https://www.pressian.com/pages/articles/284566', 'https://www.pressian.com/pages/articles/284539', 'https://www.pressian.com/pages/articles/284216', 'https://www.pressian.com/pages/articles/283942', 'https://www.pressian.com/pages/articles/283583', 'https://www.pressian.com/pages/articles/283521', 'https://www.pressian.com/pages/articles/283353', 'https://www.pressian.com/pages/articles/283313', 'https://www.pressian.com/pages/articles/283170', 'https://www.pressian.com/pages/articles/283053', 'https://www.pressian.com/pages/articles/282776', 'https://www.pressian.com/pages/articles/282571', 'https://www.pressian.com/pages/articles/280803', 'https://www.pressian.com/pages/articles/282008', 'https://www.pressian.com/pages/articles/281278', 'https://www.pressian.com/pages/articles/281449', 'https://www.pressian.com/pages/articles/281361', 'https://www.pressian.com/pages/articles/280898', 'https://www.pressian.com/pages/articles/280669', 'https://www.pressian.com/pages/articles/280363', 'https://www.pressian.com/pages/articles/279787', 'https://www.pressian.com/pages/articles/279948', 'https://www.pressian.com/pages/articles/279320', 'https://www.pressian.com/pages/articles/279183', 'https://www.pressian.com/pages/articles/278812', 'https://www.pressian.com/pages/articles/278632', 'https://www.pressian.com/pages/articles/278499', 'https://www.pressian.com/pages/articles/278301', 'https://www.pressian.com/pages/articles/277921', 'https://www.pressian.com/pages/articles/277503', 'https://www.pressian.com/pages/articles/277264', 'https://www.pressian.com/pages/articles/277294', 'https://www.pressian.com/pages/articles/276501', 'https://www.pressian.com/pages/articles/276499', 'https://www.pressian.com/pages/articles/276470', 'https://www.pressian.com/pages/articles/275994', 'https://www.pressian.com/pages/articles/275768', 'https://www.pressian.com/pages/articles/275766', 'https://www.pressian.com/pages/articles/275537', 'https://www.pressian.com/pages/articles/275449', 'https://www.pressian.com/pages/articles/275419', 'https://www.pressian.com/pages/articles/275237', 'https://www.pressian.com/pages/articles/275241', 'https://www.pressian.com/pages/articles/275116', 'https://www.pressian.com/pages/articles/274935', 'https://www.pressian.com/pages/articles/274738', 'https://www.pressian.com/pages/articles/274719', 'https://www.pressian.com/pages/articles/274663', 'https://www.pressian.com/pages/articles/274369']


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
        'div#wrap>div#container>div.inner>div.article_view>div.section.pr10>div.article_body.article_body')
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
plt.title("프레시안 코로나 <20년 1월-경제> 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("프레시안 코로나 관련 <20년 1월-경제> 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

# 사용자 입력 대기
input("Press Enter to exit...")