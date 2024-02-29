import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

urls=['https://www.pressian.com/pages/articles/272055', 'https://www.pressian.com/pages/articles/271899', 'https://www.pressian.com/pages/articles/271443', 'https://www.pressian.com/pages/articles/271283', 'https://www.pressian.com/pages/articles/271113', 'https://www.pressian.com/pages/articles/271017', 'https://www.pressian.com/pages/articles/270954', 'https://www.pressian.com/pages/articles/270977', 'https://www.pressian.com/pages/articles/270516', 'https://www.pressian.com/pages/articles/270389', 'https://www.pressian.com/pages/articles/270294', 'https://www.pressian.com/pages/articles/270079', 'https://www.pressian.com/pages/articles/270030', 'https://www.pressian.com/pages/articles/269544', 'https://www.pressian.com/pages/articles/269222', 'https://www.pressian.com/pages/articles/269118', 'https://www.pressian.com/pages/articles/268973', 'https://www.pressian.com/pages/articles/268927', 'https://www.pressian.com/pages/articles/268773', 'https://www.pressian.com/pages/articles/268422', 'https://www.pressian.com/pages/articles/268428', 'https://www.pressian.com/pages/articles/268408', 'https://www.pressian.com/pages/articles/268198', 'https://www.pressian.com/pages/articles/267583', 'https://www.pressian.com/pages/articles/267305', 'https://www.pressian.com/pages/articles/267022', 'https://www.pressian.com/pages/articles/266696', 'https://www.pressian.com/pages/articles/266507', 'https://www.pressian.com/pages/articles/266397', 'https://www.pressian.com/pages/articles/266386']


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
plt.title("프레시안 코로나 <1달 전-사회> 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("프레시안 코로나 관련 <1달 전-사회> 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

# 사용자 입력 대기
input("Press Enter to exit...")