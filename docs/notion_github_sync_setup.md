# Notion → GitHub 논문 리뷰 자동화 설정

이 자동화는 Notion에 올라온 논문 리뷰 카드에서 본문과 첨부 PDF를 읽어 GitHub에 정리합니다.

## 자동화가 하는 일

1. Notion 논문 리뷰 카드 읽기
2. 카드에 첨부된 PDF를 `algorithms/{algorithm}/02_paper_review/papers/`에 저장
3. Notion 본문 또는 PDF 텍스트를 AI가 읽고 논문 개요 문체로 요약
4. `algorithms/{algorithm}/02_paper_review/README.md`에 자동 요약 섹션 추가
5. `main`에 바로 넣지 않고 Pull Request 생성

## GitHub Secrets

GitHub 저장소의 `Settings → Secrets and variables → Actions`에 아래 값을 등록합니다.

| 이름 | 설명 |
|---|---|
| `NOTION_API_KEY` | Notion integration secret |
| `OPENAI_API_KEY` | OpenAI API key |

선택으로 `Variables`에 아래 값을 등록할 수 있습니다.

| 이름 | 기본값 | 설명 |
|---|---|---|
| `OPENAI_MODEL` | `gpt-5.6-terra` | README 요약 생성에 사용할 모델 |

## Notion 쪽 준비

Notion integration을 만든 뒤, 스터디 페이지 또는 과제 데이터베이스에 integration 접근 권한을 줘야 합니다.

팀원 제출 규칙은 단순하게 유지합니다.

- 논문 리뷰 카드는 `상태 = 완료`로 바꾸기
- 보고서 본문은 Notion 카드에 작성하기
- 최종 제출 PDF는 카드의 `파일` 속성 또는 카드 본문에 첨부하기

## GitHub에서 실행하는 방법

1. GitHub 저장소로 이동
2. `Actions` 탭 클릭
3. `Sync Notion paper reviews` 선택
4. `Run workflow` 클릭
5. 입력값 작성

| 입력값 | 예시 |
|---|---|
| `algorithm` | `svm` |
| `week` | `w7` |
| `notion_pages` | Notion 카드 URL 여러 개 |
| `target_branch` | `main` |

실행이 끝나면 자동으로 PR이 생성됩니다. README 요약문을 확인한 뒤 merge하면 됩니다.

## 완전 자동 모드

매번 카드 URL을 넣기 싫다면 `notion_source_id`에 Notion 데이터소스 또는 데이터베이스 ID를 넣을 수 있습니다.

이 경우 데이터베이스에 아래 속성이 있으면 자동 필터링됩니다.

| 속성 | 기본값 |
|---|---|
| 상태 | 완료 |
| 유형 | 논문 |
| 주차 | w7 |
| 알고리즘 | svm |

현재 Notion 구조에 `주차`, `알고리즘` 속성이 없다면 처음에는 `notion_pages`에 카드 URL을 직접 넣는 방식이 가장 안전합니다.
