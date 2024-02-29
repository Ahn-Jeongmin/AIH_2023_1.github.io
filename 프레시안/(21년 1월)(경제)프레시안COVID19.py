import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

urls=['https://www.pressian.com/pages/articles/2021031014482314718', 'https://www.pressian.com/pages/articles/2021030811004046927', 'https://www.pressian.com/pages/articles/2021030810065752026', 'https://www.pressian.com/pages/articles/2021030716260947100', 'https://www.pressian.com/pages/articles/2021030716132604380', 'https://www.pressian.com/pages/articles/2021030515591303554', 'https://www.pressian.com/pages/articles/2021030216420454720', 'https://www.pressian.com/pages/articles/2021030210495833987', 'https://www.pressian.com/pages/articles/2021030111272981189', 'https://www.pressian.com/pages/articles/2021022812083682074', 'https://www.pressian.com/pages/articles/2021022514423670010', 'https://www.pressian.com/pages/articles/2021022316445098773', 'https://www.pressian.com/pages/articles/2021022214502681515', 'https://www.pressian.com/pages/articles/2021022210055083460', 'https://www.pressian.com/pages/articles/2021021810332690380', 'https://www.pressian.com/pages/articles/2021021615315007302', 'https://www.pressian.com/pages/articles/2021021617463844174', 'https://www.pressian.com/pages/articles/2021021609295449125', 'https://www.pressian.com/pages/articles/2021021509592439219', 'https://www.pressian.com/pages/articles/2021021509551362849', 'https://www.pressian.com/pages/articles/2021021411405030363', 'https://www.pressian.com/pages/articles/2021021411311463502', 'https://www.pressian.com/pages/articles/2021021013155417027', 'https://www.pressian.com/pages/articles/2021020922282615241', 'https://www.pressian.com/pages/articles/2021020913160748906', 'https://www.pressian.com/pages/articles/2021020811235855400', 'https://www.pressian.com/pages/articles/2021020810390353164', 'https://www.pressian.com/pages/articles/2021020810211316699', 'https://www.pressian.com/pages/articles/2021020717155710537', 'https://www.pressian.com/pages/articles/2021020417461705600', 'https://www.pressian.com/pages/articles/2021020420094416299', 'https://www.pressian.com/pages/articles/2021020111194990213', 'https://www.pressian.com/pages/articles/2021012516575817317', 'https://www.pressian.com/pages/articles/2021012423515341390', 'https://www.pressian.com/pages/articles/2021012216550812144', 'https://www.pressian.com/pages/articles/2021011713370264682', 'https://www.pressian.com/pages/articles/2021011414142474750', 'https://www.pressian.com/pages/articles/2021011313391895009', 'https://www.pressian.com/pages/articles/2021011215410674528', 'https://www.pressian.com/pages/articles/2021011217042312343', 'https://www.pressian.com/pages/articles/2021011116525729080', 'https://www.pressian.com/pages/articles/2021010808380956465', 'https://www.pressian.com/pages/articles/2021010710345226380', 'https://www.pressian.com/pages/articles/2021010615522618216', 'https://www.pressian.com/pages/articles/2021010612442499330', 'https://www.pressian.com/pages/articles/2021010409071617731', 'https://www.pressian.com/pages/articles/2020123111590568364', 'https://www.pressian.com/pages/articles/2020123016481243237', 'https://www.pressian.com/pages/articles/2020122915475388276', 'https://www.pressian.com/pages/articles/2020122909260481279']


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
plt.title("프레시안 코로나 <21년 1월-경제> 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("프레시안 코로나 관련 <21년 1월-경제> 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

# 사용자 입력 대기
input("Press Enter to exit...")