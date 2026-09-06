# SVM

## 논문 리뷰

| 작성자 | 논문 출처 | 키워드 | PDF | Notion |
|---|---|---|---|---|
| 박중현 | 유지현·고진환(2025), 「초음파 어레이를 활용한 One-Class SVM 낙상 탐지」 | One-Class SVM, 이상치 탐지, 낙상 탐지, 초음파 어레이 | [PDF](./papers/w7_svm_paper_review_박중현.pdf) | [Notion](https://app.notion.com/p/w7_svm_PaperReview-3ca917c0e640803181a8fb2ca4c71de6?pvs=25) |
| 강재성 | Baly, R. & Hajj, H. (2012), *Wafer Classification Using Support Vector Machines* | 반도체 수율 예측, 웨이퍼 분류, RBF SVM, False Negative | [PDF](./papers/w7_wafer_classification_jaesung.pdf) | [Notion](https://app.notion.com/p/3cb917c0e64080c39945d7e1ed7cb300?pvs=25) |
| 신정윤 | *Sentiment Analysis for IMDb Movie Review Using SVM Method* | 감성 분석, IMDb Review, SVM, BoW, TF-IDF | [PDF](./papers/w7_imdb_sentiment_svm_wjddbsl03.pdf) | [Notion](https://app.notion.com/p/w7-_-SVM-3ca917c0e6408039896cc410effdb6e4?pvs=25) |

## 요약

### 박중현

- 낙상 탐지에서 이상 데이터 수집이 어렵다는 문제를 One-Class SVM으로 다룬 논문이다.
- 초음파 어레이 신호를 이미지 형태로 변환하고 TC-CNN, OC-CNN, OC-SVM을 비교했다.
- RBF 기반 OC-SVM은 정상 데이터만 학습해도 높은 탐지 성능을 보여 이상치 탐지 프로젝트로 이어지기 좋다.

### 강재성

- 반도체 중간 공정 데이터를 이용해 웨이퍼를 Low-Yield / High-Yield로 조기 분류하는 연구다.
- 실제 IC 제조 데이터에 RBF SVM을 적용하고 Decision Tree, kNN, PLS, GRNN과 비교했다.
- False Negative를 낮추는 것이 핵심이며, 이는 제조 공정의 리스크 관리 문제와 직접 연결된다.
- SECOM 반도체 데이터처럼 공정 변수 기반 품질 예측 데이터로 미니 프로젝트를 구성하기 좋다.

### 신정윤

- IMDb 영화 리뷰를 긍정/부정으로 분류하는 SVM 기반 감성 분석 연구다.
- BoW와 TF-IDF로 텍스트를 벡터화하고 Grid Search로 SVM 하이퍼파라미터를 탐색했다.
- TF-IDF 기반 SVM이 BoW보다 높은 성능을 보여 텍스트 분류에서 특성 표현 방식의 중요성을 확인했다.
- 영화 리뷰나 상품 리뷰 데이터로 BoW와 TF-IDF 성능을 비교하는 프로젝트로 확장하기 좋다.
