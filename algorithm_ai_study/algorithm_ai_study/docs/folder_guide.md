# Folder Guide

팀원들이 같은 구조로 정리할 수 있도록 폴더별 사용 방법을 정리한 문서입니다.

## 기본 규칙

- 폴더명과 파일명은 영어 소문자와 `_`를 사용합니다.
- 한글 설명은 문서 안에 작성해도 됩니다.
- 개인 실험 파일은 자기 브랜치에서 작업하고, 정리된 파일만 Pull Request로 올립니다.
- `data/`, `outputs/`, `models/`처럼 용량이 크거나 개인 PC 환경에 따라 달라지는 파일은 GitHub에 올리지 않습니다.

## 최상위 폴더

```text
algorithm_ai_study/
  algorithms/
  projects/
  papers/
  templates/
  docs/
  assets/
```

## algorithms/

알고리즘별 공부 자료를 넣는 핵심 폴더입니다.

예시:

```text
algorithms/
  graph/
  dynamic_programming/
  optimization/
```

각 알고리즘 폴더는 아래 구조를 사용합니다.

```text
algorithms/<topic>/
  README.md
  theory.md
  math.md
  implementation/
  practice/
  project/
  papers.md
```

### README.md

해당 알고리즘 주제의 전체 소개를 적습니다.

### theory.md

알고리즘의 핵심 개념, 동작 방식, 장단점, 사용 상황을 정리합니다.

### math.md

알고리즘을 이해하는 데 필요한 수학 개념을 정리합니다.

### implementation/

직접 구현한 코드를 저장합니다.

예시:

```text
implementation/
  dijkstra.py
  bellman_ford.py
```

### practice/

백준, 프로그래머스, 예제 문제 풀이를 저장합니다.

예시:

```text
practice/
  boj_1753_shortest_path.py
```

### project/

해당 알고리즘을 적용한 작은 실험이나 프로젝트를 저장합니다.

### papers.md

관련 논문 목록과 간단한 리뷰를 정리합니다.

## projects/

여러 알고리즘을 함께 사용한 미니 프로젝트를 넣습니다.

예시:

```text
projects/
  route_optimization/
  recommendation_experiment/
```

## papers/

전체 논문 리뷰를 모아두는 폴더입니다.

알고리즘별 `papers.md`에는 간단히 정리하고, 긴 리뷰는 `papers/`에 따로 문서로 저장합니다.

## templates/

팀원들이 같은 형식으로 작성할 수 있도록 템플릿을 모아둡니다.

현재 템플릿:

```text
algorithm_note_template.md
paper_review_template.md
project_report_template.md
```

## docs/

협업 방식, 폴더 사용법, 회의 기록 등 팀원 안내 문서를 저장합니다.

## assets/

README, 발표 자료, 프로젝트 설명에 사용할 이미지와 구조도를 저장합니다.

