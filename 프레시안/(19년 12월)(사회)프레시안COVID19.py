import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

urls=['https://www.pressian.com/pages/articles/272152', 'https://www.pressian.com/pages/articles/272162', 'https://www.pressian.com/pages/articles/272101', 'https://www.pressian.com/pages/articles/272077', 'https://www.pressian.com/pages/articles/272054', 'https://www.pressian.com/pages/articles/272107', 'https://www.pressian.com/pages/articles/272063', 'https://www.pressian.com/pages/articles/271868', 'https://www.pressian.com/pages/articles/272034', 'https://www.pressian.com/pages/articles/271945', 'https://www.pressian.com/pages/articles/271902', 'https://www.pressian.com/pages/articles/271914', 'https://www.pressian.com/pages/articles/271889', 'https://www.pressian.com/pages/articles/271865', 'https://www.pressian.com/pages/articles/271372', 'https://www.pressian.com/pages/articles/271830', 'https://www.pressian.com/pages/articles/271812', 'https://www.pressian.com/pages/articles/271808', 'https://www.pressian.com/pages/articles/271777', 'https://www.pressian.com/pages/articles/271803', 'https://www.pressian.com/pages/articles/271773', 'https://www.pressian.com/pages/articles/271766', 'https://www.pressian.com/pages/articles/271760', 'https://www.pressian.com/pages/articles/271756', 'https://www.pressian.com/pages/articles/271592', 'https://www.pressian.com/pages/articles/271666', 'https://www.pressian.com/pages/articles/271647', 'https://www.pressian.com/pages/articles/271583', 'https://www.pressian.com/pages/articles/271594', 'https://www.pressian.com/pages/articles/271560', 'https://www.pressian.com/pages/articles/271557', 'https://www.pressian.com/pages/articles/271531', 'https://www.pressian.com/pages/articles/271525', 'https://www.pressian.com/pages/articles/271387', 'https://www.pressian.com/pages/articles/271472', 'https://www.pressian.com/pages/articles/271401', 'https://www.pressian.com/pages/articles/271423', 'https://www.pressian.com/pages/articles/271409', 'https://www.pressian.com/pages/articles/271368', 'https://www.pressian.com/pages/articles/271232', 'https://www.pressian.com/pages/articles/270641', 'https://www.pressian.com/pages/articles/271279', 'https://www.pressian.com/pages/articles/271301', 'https://www.pressian.com/pages/articles/271267', 'https://www.pressian.com/pages/articles/271262', 'https://www.pressian.com/pages/articles/271203', 'https://www.pressian.com/pages/articles/271237', 'https://www.pressian.com/pages/articles/271216', 'https://www.pressian.com/pages/articles/271204', 'https://www.pressian.com/pages/articles/271181', 'https://www.pressian.com/pages/articles/271195', 'https://www.pressian.com/pages/articles/270651', 'https://www.pressian.com/pages/articles/271087', 'https://www.pressian.com/pages/articles/271037', 'https://www.pressian.com/pages/articles/271082', 'https://www.pressian.com/pages/articles/271081', 'https://www.pressian.com/pages/articles/271041', 'https://www.pressian.com/pages/articles/271022', 'https://www.pressian.com/pages/articles/271014', 'https://www.pressian.com/pages/articles/270996', 'https://www.pressian.com/pages/articles/270846', 'https://www.pressian.com/pages/articles/270948', 'https://www.pressian.com/pages/articles/270945', 'https://www.pressian.com/pages/articles/270907', 'https://www.pressian.com/pages/articles/270633', 'https://www.pressian.com/pages/articles/270855', 'https://www.pressian.com/pages/articles/270718', 'https://www.pressian.com/pages/articles/270834', 'https://www.pressian.com/pages/articles/270581', 'https://www.pressian.com/pages/articles/270244', 'https://www.pressian.com/pages/articles/270768', 'https://www.pressian.com/pages/articles/270743', 'https://www.pressian.com/pages/articles/270731', 'https://www.pressian.com/pages/articles/270746', 'https://www.pressian.com/pages/articles/270580', 'https://www.pressian.com/pages/articles/270597', 'https://www.pressian.com/pages/articles/270695', 'https://www.pressian.com/pages/articles/270589', 'https://www.pressian.com/pages/articles/270559', 'https://www.pressian.com/pages/articles/270555', 'https://www.pressian.com/pages/articles/270534', 'https://www.pressian.com/pages/articles/270541', 'https://www.pressian.com/pages/articles/270455', 'https://www.pressian.com/pages/articles/270517', 'https://www.pressian.com/pages/articles/270476', 'https://www.pressian.com/pages/articles/270427', 'https://www.pressian.com/pages/articles/270361', 'https://www.pressian.com/pages/articles/270349', 'https://www.pressian.com/pages/articles/270290', 'https://www.pressian.com/pages/articles/270322', 'https://www.pressian.com/pages/articles/270250', 'https://www.pressian.com/pages/articles/270269', 'https://www.pressian.com/pages/articles/270147', 'https://www.pressian.com/pages/articles/270181', 'https://www.pressian.com/pages/articles/270176', 'https://www.pressian.com/pages/articles/270158', 'https://www.pressian.com/pages/articles/270124', 'https://www.pressian.com/pages/articles/270112', 'https://www.pressian.com/pages/articles/270055', 'https://www.pressian.com/pages/articles/269976', 'https://www.pressian.com/pages/articles/269984', 'https://www.pressian.com/pages/articles/269979', 'https://www.pressian.com/pages/articles/269972', 'https://www.pressian.com/pages/articles/269967', 'https://www.pressian.com/pages/articles/269962', 'https://www.pressian.com/pages/articles/269963', 'https://www.pressian.com/pages/articles/269946', 'https://www.pressian.com/pages/articles/268910', 'https://www.pressian.com/pages/articles/269793', 'https://www.pressian.com/pages/articles/269739', 'https://www.pressian.com/pages/articles/269808', 'https://www.pressian.com/pages/articles/269766', 'https://www.pressian.com/pages/articles/269746', 'https://www.pressian.com/pages/articles/269704', 'https://www.pressian.com/pages/articles/269624', 'https://www.pressian.com/pages/articles/269626', 'https://www.pressian.com/pages/articles/269689', 'https://www.pressian.com/pages/articles/269667', 'https://www.pressian.com/pages/articles/269666', 'https://www.pressian.com/pages/articles/269659', 'https://www.pressian.com/pages/articles/269620', 'https://www.pressian.com/pages/articles/269618', 'https://www.pressian.com/pages/articles/269566', 'https://www.pressian.com/pages/articles/269568', 'https://www.pressian.com/pages/articles/269556', 'https://www.pressian.com/pages/articles/269564', 'https://www.pressian.com/pages/articles/269540', 'https://www.pressian.com/pages/articles/269550', 'https://www.pressian.com/pages/articles/269528', 'https://www.pressian.com/pages/articles/269473', 'https://www.pressian.com/pages/articles/269431', 'https://www.pressian.com/pages/articles/269436', 'https://www.pressian.com/pages/articles/269402', 'https://www.pressian.com/pages/articles/269393', 'https://www.pressian.com/pages/articles/269319', 'https://www.pressian.com/pages/articles/269336', 'https://www.pressian.com/pages/articles/269342', 'https://www.pressian.com/pages/articles/269258', 'https://www.pressian.com/pages/articles/269280', 'https://www.pressian.com/pages/articles/269269', 'https://www.pressian.com/pages/articles/269262', 'https://www.pressian.com/pages/articles/269242', 'https://www.pressian.com/pages/articles/269202', 'https://www.pressian.com/pages/articles/269197', 'https://www.pressian.com/pages/articles/269170', 'https://www.pressian.com/pages/articles/269183', 'https://www.pressian.com/pages/articles/269147', 'https://www.pressian.com/pages/articles/269112', 'https://www.pressian.com/pages/articles/269066', 'https://www.pressian.com/pages/articles/269021', 'https://www.pressian.com/pages/articles/269003', 'https://www.pressian.com/pages/articles/269057', 'https://www.pressian.com/pages/articles/269011', 'https://www.pressian.com/pages/articles/268976', 'https://www.pressian.com/pages/articles/268985', 'https://www.pressian.com/pages/articles/268977', 'https://www.pressian.com/pages/articles/268974', 'https://www.pressian.com/pages/articles/268946', 'https://www.pressian.com/pages/articles/268944', 'https://www.pressian.com/pages/articles/268943', 'https://www.pressian.com/pages/articles/268802', 'https://www.pressian.com/pages/articles/268841', 'https://www.pressian.com/pages/articles/268794', 'https://www.pressian.com/pages/articles/268796', 'https://www.pressian.com/pages/articles/268691', 'https://www.pressian.com/pages/articles/268761', 'https://www.pressian.com/pages/articles/268533', 'https://www.pressian.com/pages/articles/268695', 'https://www.pressian.com/pages/articles/268697', 'https://www.pressian.com/pages/articles/268680', 'https://www.pressian.com/pages/articles/268523', 'https://www.pressian.com/pages/articles/268673', 'https://www.pressian.com/pages/articles/268626', 'https://www.pressian.com/pages/articles/268590', 'https://www.pressian.com/pages/articles/268499', 'https://www.pressian.com/pages/articles/268503', 'https://www.pressian.com/pages/articles/268364', 'https://www.pressian.com/pages/articles/268359', 'https://www.pressian.com/pages/articles/268354', 'https://www.pressian.com/pages/articles/268339', 'https://www.pressian.com/pages/articles/268331', 'https://www.pressian.com/pages/articles/268299', 'https://www.pressian.com/pages/articles/268234', 'https://www.pressian.com/pages/articles/268255', 'https://www.pressian.com/pages/articles/268211', 'https://www.pressian.com/pages/articles/268205', 'https://www.pressian.com/pages/articles/268210', 'https://www.pressian.com/pages/articles/268186', 'https://www.pressian.com/pages/articles/267143', 'https://www.pressian.com/pages/articles/268132', 'https://www.pressian.com/pages/articles/268095', 'https://www.pressian.com/pages/articles/268030', 'https://www.pressian.com/pages/articles/268058', 'https://www.pressian.com/pages/articles/268048', 'https://www.pressian.com/pages/articles/267982', 'https://www.pressian.com/pages/articles/267990', 'https://www.pressian.com/pages/articles/267983', 'https://www.pressian.com/pages/articles/267977', 'https://www.pressian.com/pages/articles/267966', 'https://www.pressian.com/pages/articles/267884', 'https://www.pressian.com/pages/articles/267878', 'https://www.pressian.com/pages/articles/267874', 'https://www.pressian.com/pages/articles/267725', 'https://www.pressian.com/pages/articles/267825', 'https://www.pressian.com/pages/articles/267768', 'https://www.pressian.com/pages/articles/267760', 'https://www.pressian.com/pages/articles/267744', 'https://www.pressian.com/pages/articles/267712', 'https://www.pressian.com/pages/articles/267715', 'https://www.pressian.com/pages/articles/267703']


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
plt.title("프레시안 코로나 <1달 전-정치> 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("프레시안 코로나 관련 <1달 전-정치> 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

# 사용자 입력 대기
input("Press Enter to exit...")