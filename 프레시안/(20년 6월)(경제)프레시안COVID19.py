import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

urls=['https://www.pressian.com/pages/articles/2020080320353648148', 'https://www.pressian.com/pages/articles/2020080317272091757', 'https://www.pressian.com/pages/articles/2020080316104767466', 'https://www.pressian.com/pages/articles/2020080311074053906', 'https://www.pressian.com/pages/articles/2020080309211395249', 'https://www.pressian.com/pages/articles/2020073114470232145', 'https://www.pressian.com/pages/articles/2020073110322233951', 'https://www.pressian.com/pages/articles/2020073017541358252', 'https://www.pressian.com/pages/articles/2020073013521896613', 'https://www.pressian.com/pages/articles/2020073010332641274', 'https://www.pressian.com/pages/articles/2020072816025340975', 'https://www.pressian.com/pages/articles/2020072815002059785', 'https://www.pressian.com/pages/articles/2020072715442748645', 'https://www.pressian.com/pages/articles/2020072714215915684', 'https://www.pressian.com/pages/articles/2020072421172130206', 'https://www.pressian.com/pages/articles/2020072312050505345', 'https://www.pressian.com/pages/articles/2020072214360202954', 'https://www.pressian.com/pages/articles/2020072117452635018', 'https://www.pressian.com/pages/articles/2020072116230476317', 'https://www.pressian.com/pages/articles/2020072013501492164', 'https://www.pressian.com/pages/articles/2020072014060848673', 'https://www.pressian.com/pages/articles/2020072011442314030', 'https://www.pressian.com/pages/articles/2020072008395692303', 'https://www.pressian.com/pages/articles/2020071715454642559', 'https://www.pressian.com/pages/articles/2020071613071143701', 'https://www.pressian.com/pages/articles/2020071514552350722', 'https://www.pressian.com/pages/articles/2020071413480314381', 'https://www.pressian.com/pages/articles/2020071318055123827', 'https://www.pressian.com/pages/articles/2020071413501933942', 'https://www.pressian.com/pages/articles/2020071410141505210', 'https://www.pressian.com/pages/articles/2020071013553028893', 'https://www.pressian.com/pages/articles/2020070917352043648', 'https://www.pressian.com/pages/articles/2020070910240449004', 'https://www.pressian.com/pages/articles/2020070815460036014', 'https://www.pressian.com/pages/articles/2020070814594970525', 'https://www.pressian.com/pages/articles/2020070715452331068', 'https://www.pressian.com/pages/articles/2020070317201940975', 'https://www.pressian.com/pages/articles/2020070215340602486', 'https://www.pressian.com/pages/articles/2020070217531904054', 'https://www.pressian.com/pages/articles/2020070212032898991', 'https://www.pressian.com/pages/articles/2020070211360275668', 'https://www.pressian.com/pages/articles/2020062914442848080', 'https://www.pressian.com/pages/articles/2020063010234302469', 'https://www.pressian.com/pages/articles/2020062918573357954', 'https://www.pressian.com/pages/articles/2020062914572892580', 'https://www.pressian.com/pages/articles/2020062910371109480', 'https://www.pressian.com/pages/articles/2020062514431957390', 'https://www.pressian.com/pages/articles/2020062513341948804', 'https://www.pressian.com/pages/articles/2020062410060325583', 'https://www.pressian.com/pages/articles/2020062215303374136', 'https://www.pressian.com/pages/articles/2020062315005627083', 'https://www.pressian.com/pages/articles/2020062311323699682', 'https://www.pressian.com/pages/articles/2020062209574601595', 'https://www.pressian.com/pages/articles/2020061614032910014', 'https://www.pressian.com/pages/articles/2020061719380872406', 'https://www.pressian.com/pages/articles/2020061711355815308', 'https://www.pressian.com/pages/articles/2020061616043839524', 'https://www.pressian.com/pages/articles/2020061621332889269', 'https://www.pressian.com/pages/articles/2020061613494954428', 'https://www.pressian.com/pages/articles/2020061611241223786', 'https://www.pressian.com/pages/articles/2020061517500663274', 'https://www.pressian.com/pages/articles/2020061515565549259', 'https://www.pressian.com/pages/articles/2020061514264231232', 'https://www.pressian.com/pages/articles/2020061214261242009', 'https://www.pressian.com/pages/articles/2020061214320687819', 'https://www.pressian.com/pages/articles/2020061118112958568', 'https://www.pressian.com/pages/articles/2020061015275608503', 'https://www.pressian.com/pages/articles/2020061014141547711', 'https://www.pressian.com/pages/articles/2020060916592143876', 'https://www.pressian.com/pages/articles/2020060911332157544', 'https://www.pressian.com/pages/articles/2020060813425671291', 'https://www.pressian.com/pages/articles/2020060810390503932', 'https://www.pressian.com/pages/articles/2020060713562320860', 'https://www.pressian.com/pages/articles/2020060412244244377', 'https://www.pressian.com/pages/articles/2020060315211297106', 'https://www.pressian.com/pages/articles/2020060310292001787', 'https://www.pressian.com/pages/articles/2020060217493849175', 'https://www.pressian.com/pages/articles/2020060212164425750', 'https://www.pressian.com/pages/articles/2020053012203613663', 'https://www.pressian.com/pages/articles/2020052815405340171']


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
plt.title("프레시안 코로나 <20년 6월-경제> 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("프레시안 코로나 관련 <20년 6월-경제> 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

# 사용자 입력 대기
input("Press Enter to exit...")