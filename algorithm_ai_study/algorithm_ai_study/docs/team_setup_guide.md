# Algorithm & AI Study Lab 팀원 안내서

이 문서는 스터디 프로젝트 폴더를 처음 받은 팀원이 같은 구조로 작업하고, GitHub에 본인 작업을 올릴 수 있도록 정리한 안내서입니다.

---

## 1. 압축 파일을 만들 때 주의할 점

### 1.1 `.git` 폴더는 압축에 넣지 않기

`.git` 폴더는 개인 컴퓨터의 Git 기록과 GitHub 연결 정보를 담고 있습니다.

팀원에게 공유할 압축 파일에는 `.git` 폴더를 넣지 않습니다.

### 1.2 큰 파일 폴더는 압축에 넣지 않기

아래 폴더는 압축 파일과 GitHub에 올리지 않습니다.

```text
data/
outputs/
models/
```

이 폴더들은 용량이 크거나 개인 컴퓨터 환경마다 달라질 수 있습니다.

### 1.3 압축은 프로젝트 폴더 바깥에서 만들기

예시:

```text
C:\project
```

위 위치에서 `algorithm_ai_study` 폴더를 우클릭해서 압축합니다.

추천 압축 파일명:

```text
algorithm_ai_study_structure.zip
```

---

## 2. 프로젝트 폴더 구조

```text
algorithm_ai_study/
  algorithms/
  projects/
  papers/
  templates/
  docs/
  assets/
```

### `algorithms/`

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

### `algorithms/<topic>/README.md`

해당 알고리즘 주제의 전체 소개를 적습니다.

### `algorithms/<topic>/theory.md`

알고리즘의 핵심 개념, 동작 방식, 장단점, 사용 상황을 정리합니다.

### `algorithms/<topic>/math.md`

알고리즘을 이해하는 데 필요한 수학 개념을 정리합니다.

### `algorithms/<topic>/implementation/`

직접 구현한 코드를 저장합니다.

예시:

```text
implementation/
  dijkstra.py
  bellman_ford.py
```

### `algorithms/<topic>/practice/`

백준, 프로그래머스, 예제 문제 풀이를 저장합니다.

예시:

```text
practice/
  boj_1753_shortest_path.py
```

### `algorithms/<topic>/project/`

해당 알고리즘을 적용한 작은 실험이나 프로젝트를 저장합니다.

### `algorithms/<topic>/papers.md`

관련 논문 목록과 간단한 리뷰를 정리합니다.

### `projects/`

여러 알고리즘을 함께 사용한 미니 프로젝트를 넣습니다.

예시:

```text
projects/
  route_optimization/
  recommendation_experiment/
```

### `papers/`

전체 논문 리뷰를 모아두는 폴더입니다.

알고리즘별 `papers.md`에는 간단히 정리하고, 긴 리뷰는 `papers/`에 따로 문서로 저장합니다.

### `templates/`

팀원들이 같은 형식으로 작성할 수 있도록 템플릿을 모아둡니다.

현재 템플릿:

```text
algorithm_note_template.md
paper_review_template.md
project_report_template.md
```

### `docs/`

폴더 사용법, 협업 방식, 회의 기록 등 팀원 안내 문서를 저장합니다.

### `assets/`

README, 발표 자료, 프로젝트 설명에 사용할 이미지와 구조도를 저장합니다.

---

## 3. 팀원 최초 사용 방법

### 3.1 압축 파일 풀기

압축 파일을 원하는 위치에 풉니다.

예시:

```powershell
C:\project\algorithm_ai_study
```

### 3.2 프로젝트 폴더로 이동하기

터미널 또는 명령 프롬프트에서 아래 명령어를 실행합니다.

```powershell
cd C:\project\algorithm_ai_study
```

### 3.3 Git 연결하기

```powershell
git init
```

```powershell
git branch -M main
```

```powershell
git remote add origin https://github.com/JHPark-kor/algorithm-ai-study.git
```

### 3.4 본인 작업용 브랜치 만들기

```powershell
git checkout -b feature/본인이름-작업명
```

예시:

```powershell
git checkout -b feature/minsu-graph
```

---

## 4. 작업 후 GitHub에 올리는 방법

### 4.1 변경된 파일 확인

```powershell
git status
```

### 4.2 변경한 파일을 Git 저장 목록에 올리기

```powershell
git add .
```

### 4.3 작업 내용을 커밋하기

```powershell
git commit -m "Add graph theory notes"
```

### 4.4 본인 브랜치를 GitHub에 올리기

```powershell
git push -u origin HEAD
```

### 4.5 Pull Request 만들기

GitHub 저장소에 들어가서 Pull Request를 만듭니다.

Pull Request 방향:

```text
내 브랜치 -> main
```

예시:

```text
feature/minsu-graph -> main
```

---

## 5. 작업 규칙

### 파일명 규칙

파일명과 폴더명은 영어 소문자, 숫자, `_`를 사용합니다.

좋은 예시:

```text
dynamic_programming
paper_review_template.md
boj_1753_shortest_path.py
```

피하는 예시:

```text
동적계획법
Graph Study Final 진짜최종.py
```

### 브랜치 규칙

개인 작업은 본인 브랜치에서 진행합니다.

브랜치 이름 예시:

```text
feature/minsu-graph
feature/jiyoon-dp
feature/pjh-optimization
```

### GitHub 업로드 규칙

정리된 내용만 Pull Request로 `main`에 반영합니다.

아래 폴더는 GitHub에 올리지 않습니다.

```text
data/
outputs/
models/
```

### README 수정 규칙

`README.md`는 저장소 첫 화면입니다.

큰 수정이 필요하면 팀원들과 먼저 상의한 뒤 수정합니다.

---

## 6. 자주 쓰는 명령어

### 현재 상태 확인

```powershell
git status
```

### 현재 브랜치 확인

```powershell
git branch
```

### main 최신 내용 받기

```powershell
git checkout main
```

```powershell
git pull origin main
```

### 기존 브랜치로 다시 이동

```powershell
git checkout feature/본인이름-작업명
```

예시:

```powershell
git checkout feature/minsu-graph
```

### 작업 후 GitHub에 올리기

```powershell
git add .
```

```powershell
git commit -m "작업 내용 설명"
```

```powershell
git push -u origin HEAD
```

---

## 7. 참고 문서

더 자세한 폴더 설명은 아래 문서를 참고합니다.

```text
docs/folder_guide.md
```

