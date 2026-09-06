# SVM - 02 Paper Review

SVM 2주차 논문/페이퍼 리뷰 결과를 보관하는 공간입니다.

Notion은 과제 제출과 스케줄 관리를 위한 공간으로 사용하고, GitHub에는 최종 보관용 PDF와 요약본을 정리합니다.

## 제출 자료

| 작성자 | 논문 출처 | 주요 키워드 | GitHub PDF | Notion |
|---|---|---|---|---|
| 박중현 | 유지현·고진환(2025), 「초음파 어레이를 활용한 One-Class SVM 낙상 탐지」 | One-Class SVM, 이상치 탐지, 낙상 탐지, 초음파 어레이, 클래스 불균형 | [PDF](./papers/w7_svm_paper_review_박중현.pdf) | [Notion](https://app.notion.com/p/w7_svm_PaperReview-3ca917c0e640803181a8fb2ca4c71de6?pvs=25) |
| JAESUNGKANG | Baly, R. & Hajj, H. (2012), *Wafer Classification Using Support Vector Machines*, IEEE Transactions on Semiconductor Manufacturing | 반도체 수율 예측, 웨이퍼 분류, 중간 공정 데이터, RBF SVM, False Negative | [PDF](./papers/w7_wafer_classification_jaesung.pdf) | [Notion](https://app.notion.com/p/3cb917c0e64080c39945d7e1ed7cb300?pvs=25) |
| wjddbsl03 | *Sentiment Analysis for IMDb Movie Review Using SVM Method* | 감성 분석, IMDb Review, SVM, BoW, TF-IDF, Grid Search | [PDF](./papers/w7_imdb_sentiment_svm_wjddbsl03.pdf) | [Notion](https://app.notion.com/p/w7-_-SVM-3ca917c0e6408039896cc410effdb6e4?pvs=25) |

## AI 요약 초안

아래 요약은 Notion에 제출된 PDF 및 본문 내용을 바탕으로 정리한 초안입니다.

작성자는 논문명, 수치, 해석이 맞는지 확인한 뒤 수정하면 됩니다.

### 박중현

#### 논문 개요

본 논문은 낙상 탐지 문제에서 이상 데이터 수집의 어려움과 클래스 불균형 문제를 완화하기 위해 정상 데이터만을 학습하는 One-Class SVM의 적용 가능성을 검토한다. 연구에서는 초음파 어레이로 수집한 신호를 이미지 데이터로 변환하고, 정상·이상 데이터를 모두 사용하는 TC-CNN과 정상 데이터만을 사용하는 OC-CNN, OC-SVM을 비교하였다.

실험 결과 TC-CNN이 가장 높은 정확도를 기록하였으나, RBF 커널 기반 OC-SVM 역시 정상 데이터만을 학습했음에도 높은 정확도와 F1-Score를 보였다. 이는 낙상처럼 이상 데이터 확보가 제한적인 환경에서 OC-SVM이 현실적인 이상치 탐지 대안으로 활용될 수 있음을 시사한다.

#### 데이터 및 방법

- 초음파 어레이로 수집한 사람의 움직임 데이터를 이미지 형태로 변환하였다.
- 정상 행동과 낙상 행동을 구분하는 문제로 구성하였다.
- TC-CNN, OC-CNN, OC-SVM을 비교하여 정상 데이터 기반 이상 탐지 가능성을 확인하였다.

#### 주요 결과 및 프로젝트 연결

- 이상 데이터가 충분하지 않은 상황에서도 OC-SVM을 활용할 수 있다는 점이 핵심이다.
- 3주차 프로젝트에서는 정상 데이터만 학습한 뒤 이상치를 탐지하는 방식으로 작은 이상 탐지 실험을 구성할 수 있다.
- 예시 주제: 정상 센서 데이터 기반 이상 탐지, 정상 거래 데이터 기반 이상 탐지, 정상 이미지 특징 기반 이상 탐지.

#### 피드백 체크포인트

- 논문 저자명과 연도 표기가 정확한지 확인하기
- OC-SVM 성능 수치가 PDF와 일치하는지 확인하기
- 프로젝트 아이디어를 실제 사용할 데이터셋에 맞게 좁히기

### JAESUNGKANG

#### 논문 개요

본 논문은 반도체 제조 공정에서 최종 EOL 검사 이전에 확보되는 중간 공정 측정 데이터를 이용해 웨이퍼를 Low-Yield와 High-Yield로 조기 분류하는 문제를 다룬다. 연구의 목적은 최종 수율이 확정될 때까지 기다리지 않고, 공정 중간 단계에서 수율 저하 가능성이 높은 웨이퍼를 선별할 수 있는지 검증하는 데 있다.

연구에서는 실제 IC 제조시설에서 수집된 두 개의 웨이퍼 데이터셋을 대상으로 Z-score 정규화와 Gaussian RBF Kernel SVM을 적용하였다. 이후 C4.5 Decision Tree, kNN, PLS Regression, GRNN과 비교하여 SVM의 분류 성능과 제조 리스크 관리 관점에서의 효용을 평가하였다.

#### 데이터 및 방법

- Dataset 1은 1,150개 웨이퍼와 138개 변수로 구성되었다.
- Dataset 2는 238개 웨이퍼와 30개 변수로 구성되었다.
- 입력 변수는 Z-score 방식으로 정규화하였다.
- Gaussian RBF Kernel SVM을 사용하고, 커널 폭과 패널티 파라미터를 Cross Validation으로 탐색하였다.
- 단순 정확도뿐 아니라 실제 Bad Wafer를 Good Wafer로 판단하는 False Negative를 중요한 평가 기준으로 보았다.

#### 주요 결과 및 프로젝트 연결

- SVM은 비교 모델과 동등하거나 더 높은 분류 정확도를 보였다.
- 제조 공정에서는 False Negative가 실제 손실로 이어질 수 있으므로, 단순 정확도보다 위험 비용을 함께 고려해야 한다는 점이 중요하다.
- Dataset 1에서는 전체 변수 중 일부 변수만 사용해도 성능이 유지 또는 개선되었고, 공정 변화 이후에는 Adaptive Model Update가 성능 개선에 기여하였다.
- 3주차 프로젝트에서는 SECOM 반도체 데이터와 같이 공정 변수 기반 품질 예측 데이터를 사용해 SVM 분류 실험을 구성할 수 있다.

#### 피드백 체크포인트

- “최종 수율 예측”인지 “Low-Yield / High-Yield 조기 분류”인지 표현을 통일하기
- False Negative를 제조 리스크 관점에서 설명하는 문장을 유지할지 확인하기
- Dataset 1, Dataset 2의 변수 개수와 웨이퍼 수가 PDF와 일치하는지 확인하기
- 프로젝트 적용 데이터셋을 SECOM으로 할지, 다른 반도체 공개 데이터로 할지 결정하기

### wjddbsl03

#### 논문 개요

본 논문은 IMDb 영화 리뷰 데이터를 활용하여 SVM 기반 긍정·부정 감성 분류 모델을 구현하고, BoW와 TF-IDF 특성 추출 방식에 따른 성능 차이를 비교한다. 텍스트 데이터는 그대로 SVM에 입력할 수 없기 때문에, 전처리 과정을 거쳐 수치형 벡터로 변환한 뒤 분류 모델을 학습한다.

실험 결과 TF-IDF 기반 SVM이 BoW 기반 SVM보다 더 높은 정확도와 F1-Score를 보였다. 이는 단순히 단어 등장 횟수를 세는 방식보다, 여러 문서에 흔하게 등장하는 단어의 영향은 낮추고 문서별로 구분력이 큰 단어의 가중치를 높이는 방식이 SVM의 결정 경계 학습에 더 효과적이었음을 보여준다.

#### 데이터 및 방법

- Kaggle의 IMDb Movie Review 데이터셋을 사용하였다.
- 전체 50,000개 리뷰 중 40,000개를 학습 데이터, 10,000개를 테스트 데이터로 사용하였다.
- 긍정 리뷰와 부정 리뷰가 각각 25,000개로 구성된 이진 분류 문제이다.
- HTML 제거, 소문자화, 불용어 제거, stemming, lemmatization 등의 전처리를 수행하였다.
- BoW와 TF-IDF를 각각 적용한 뒤 SVM을 학습하고 Grid Search로 하이퍼파라미터를 탐색하였다.

#### 주요 결과 및 프로젝트 연결

- BoW 기반 SVM의 정확도는 88.59%, TF-IDF 기반 SVM의 정확도는 91.27%로 보고되었다.
- 테스트 데이터 10,000건 기준 오분류 수는 BoW 1,468건, TF-IDF 1,145건으로 TF-IDF가 더 낮았다.
- 이 논문은 모델 자체뿐 아니라 입력 특성 표현 방식이 분류 성능에 큰 영향을 준다는 점을 보여준다.
- 3주차 프로젝트에서는 영화 리뷰, 상품 리뷰, 뉴스 댓글 등 짧은 텍스트 데이터를 대상으로 BoW와 TF-IDF 기반 SVM 성능을 비교할 수 있다.

#### 피드백 체크포인트

- 논문 출처의 저자명, 학회/저널 정보가 PDF에 있는지 확인하기
- BoW와 TF-IDF 성능 수치가 정확히 맞는지 확인하기
- “SVM 성능”과 “특성 추출 방식의 차이” 중 발표의 중심을 어디에 둘지 정하기
- 한국어 리뷰 데이터로 확장할 경우 형태소 분석이 필요하다는 점을 프로젝트 계획에 넣을지 검토하기
