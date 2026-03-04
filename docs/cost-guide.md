# 비용 가이드

Claude Code + GitHub Actions를 사용할 때 발생하는 비용을 상세히 분석하고 최적화 방법을 안내합니다.

---

## 목차

1. [Claude 사용 비용](#1-claude-사용-비용)
2. [GitHub Actions 비용](#2-github-actions-비용)
3. [워크플로우별 평균 비용](#3-워크플로우별-평균-비용)
4. [최적화 팁](#4-최적화-팁)
5. [비용 비교 테이블](#5-비용-비교-테이블)

---

## 1. Claude 사용 비용

### 방식 A: Claude Max 구독 (OAuth 토큰)

| 항목 | 내용 |
|------|------|
| **인증 방식** | `CLAUDE_CODE_OAUTH_TOKEN` |
| **과금** | 월 고정 구독료 |
| **추가 비용** | 없음 (구독 범위 내) |
| **제한** | 사용량 한도 있을 수 있음 (구독 플랜에 따라 다름) |

Claude Max 구독이 있다면 OAuth 토큰을 사용하는 것이 가장 경제적입니다. API 호출 건수나 토큰 수에 관계없이 구독료만 발생합니다.

### 방식 B: Anthropic API Key

| 항목 | 내용 |
|------|------|
| **인증 방식** | `ANTHROPIC_API_KEY` |
| **과금** | 토큰당 과금 (사용한 만큼) |
| **추가 비용** | Input/Output 토큰에 따라 변동 |
| **제한** | 없음 (잔액 범위 내) |

### 모델별 API 가격

| 모델 | Input (1M 토큰당) | Output (1M 토큰당) | 특징 |
|------|-------------------|-------------------|------|
| Claude Haiku | $0.25 | $1.25 | 빠르고 저렴, 단순 작업에 적합 |
| Claude Sonnet | $3 | $15 | 균형 잡힌 성능, 대부분의 작업에 적합 |
| Claude Opus | $15 | $75 | 최고 성능, 복잡한 추론에 적합 |

> **참고**: 가격은 변경될 수 있습니다. 최신 가격은 [Anthropic 가격 페이지](https://www.anthropic.com/pricing)에서 확인하세요.

### 토큰 수 감각 익히기

| 내용 | 대략적인 토큰 수 |
|------|-----------------|
| 한국어 1글자 | 약 1-2 토큰 |
| 영어 1단어 | 약 1 토큰 |
| 코드 한 줄 | 약 10-20 토큰 |
| 일반적인 프롬프트 | 100-500 토큰 |
| 파일 하나 분석 요청 | 1,000-5,000 토큰 |
| 전체 프로젝트 분석 | 10,000-50,000 토큰 |

---

## 2. GitHub Actions 비용

### 무료 한도

| 플랜 | 저장소 유형 | 무료 한도 (분/월) |
|------|-----------|-----------------|
| Free | Public | 2,000분 |
| Free | Private | 500분 |
| Pro | Private | 3,000분 |
| Team | Private | 3,000분 |
| Enterprise | Private | 50,000분 |

> **팁**: Public 저장소는 무료 한도가 넉넉하므로, 학습 및 실습에는 Public 저장소를 사용하는 것이 좋습니다.

### 초과 시 과금

무료 한도를 초과하면 분당 과금됩니다:

| Runner 유형 | 분당 비용 |
|------------|----------|
| Linux | $0.008 |
| Windows | $0.016 |
| macOS | $0.08 |

### 실행 시간 계산

- 실행 시간은 **분 단위로 올림** 처리됩니다
- 예: 실제 실행 42초 = 1분으로 계산
- Linux runner를 사용하면 비용이 가장 저렴합니다

---

## 3. 워크플로우별 평균 비용

### API Key 사용 시 예상 비용 (Sonnet 기준)

| 워크플로우 유형 | 평균 실행 시간 | Claude 토큰 | Claude 비용 | Actions 비용 |
|---------------|-------------|-----------|-----------|-------------|
| Hello Claude (단순 응답) | 1-2분 | ~2K | ~$0.03 | 무료 한도 내 |
| 코드 분석 | 3-5분 | ~10K | ~$0.15 | 무료 한도 내 |
| PR 리뷰 | 3-10분 | ~20K | ~$0.30 | 무료 한도 내 |
| 콘텐츠 생성 + 커밋 | 2-5분 | ~5K | ~$0.08 | 무료 한도 내 |
| MCP + 웹 분석 | 5-15분 | ~30K | ~$0.45 | 무료 한도 내 |

### Haiku 모델로 비용 절감 예시

| 워크플로우 유형 | Sonnet 비용 | Haiku 비용 | 절감률 |
|---------------|-----------|-----------|--------|
| 단순 응답 | ~$0.03 | ~$0.003 | 약 90% |
| 코드 분석 | ~$0.15 | ~$0.013 | 약 91% |
| PR 리뷰 | ~$0.30 | ~$0.025 | 약 92% |

### 월간 비용 시뮬레이션

매일 1회 스케줄 실행 (Sonnet, API Key 기준):

| 시나리오 | 일 실행 횟수 | 월 Claude 비용 | 월 Actions 비용 |
|---------|-----------|--------------|----------------|
| 일일 TIL 생성 | 1회 | ~$2.4 | 무료 한도 내 |
| 일일 코드 분석 | 1회 | ~$4.5 | 무료 한도 내 |
| 매시간 모니터링 | 24회 | ~$21.6 | 무료 한도 내 |
| PR 리뷰 (주 10건) | ~1.4회 | ~$13 | 무료 한도 내 |

---

## 4. 최적화 팁

### 팁 1: --max-turns 설정

Claude가 사용하는 턴 수를 제한하면 불필요한 토큰 소비를 방지합니다.

```yaml
run: |
  claude -p "간단한 요약을 해줘" \
    --max-turns 3 \
    --output-format text \
    --dangerously-skip-permissions
```

| 작업 유형 | 권장 max-turns |
|----------|---------------|
| 단순 질답 | 1-3 |
| 파일 분석 | 5-10 |
| 코드 수정 | 10-15 |
| 복잡한 멀티스텝 | 15-25 |

### 팁 2: 프롬프트 길이 최적화

```yaml
# 비효율: 불필요하게 상세한 프롬프트
run: |
  claude -p "이 프로젝트의 모든 디렉토리를 하나하나 살펴보고 \
    각 파일의 역할을 분석하고 전체 아키텍처를 파악한 다음 \
    개선할 점을 찾아서 상세하게 보고서를 작성해줘. \
    보고서에는 각 파일의 라인 수도 포함하고..." ...

# 효율적: 핵심만 간결하게
run: |
  claude -p "src/ 폴더 구조를 분석하고 주요 개선점 3가지를 알려줘" \
    --max-turns 5 ...
```

### 팁 3: 모델 선택

작업 난이도에 따라 모델을 선택합니다:

```yaml
# 단순 분류/요약 → Haiku
run: |
  claude -p "이 Issue를 bug/feature/docs 중 하나로 분류해줘" \
    --model haiku \
    --max-turns 1 ...

# 코드 리뷰/분석 → Sonnet
run: |
  claude -p "이 PR의 코드를 리뷰해줘" \
    --model sonnet \
    --max-turns 10 ...
```

### 팁 4: 조건부 실행

불필요한 실행을 방지합니다:

```yaml
# 특정 파일이 변경된 경우에만 실행
on:
  push:
    paths:
      - 'src/**'

# 특정 라벨이 있는 PR만 리뷰
jobs:
  review:
    if: contains(github.event.pull_request.labels.*.name, 'needs-review')
```

### 팁 5: 캐싱 활용

npm 설치 시간을 절약합니다:

```yaml
- name: Cache npm packages
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-claude-code
    restore-keys: |
      ${{ runner.os }}-npm-

- name: Install Claude Code
  run: npm install -g @anthropic-ai/claude-code
```

### 팁 6: 결과 재사용

같은 분석을 반복하지 않도록 결과를 캐싱합니다:

```yaml
- name: Check cached analysis
  id: cache
  uses: actions/cache@v4
  with:
    path: analysis-cache/
    key: analysis-${{ hashFiles('src/**') }}

- name: Run analysis (only if cache miss)
  if: steps.cache.outputs.cache-hit != 'true'
  run: |
    claude -p "src/ 분석해줘" \
      --output-format text \
      --dangerously-skip-permissions > analysis-cache/result.md
```

---

## 5. 비용 비교 테이블

### 이 방식 vs VPS vs 미니PC

Claude Code를 자동화하는 세 가지 방법의 비용을 비교합니다.

#### 초기 비용

| 항목 | GitHub Actions | VPS | 미니PC |
|------|---------------|-----|--------|
| 하드웨어 | $0 | $0 | $200-500 |
| 설정 시간 | 30분 | 2-4시간 | 4-8시간 |
| 도메인/IP | 불필요 | VPS에 포함 | 별도 구매 필요시 $10/년 |

#### 월간 운영 비용 (일 1회 실행 기준)

| 항목 | GitHub Actions | VPS | 미니PC |
|------|---------------|-----|--------|
| 서버 비용 | $0 (무료 한도) | $5-20/월 | 전기료 $3-5/월 |
| Claude (Max) | 구독료 | 구독료 | 구독료 |
| Claude (API, Sonnet) | ~$2-5/월 | ~$2-5/월 | ~$2-5/월 |
| 합계 (Max) | 구독료만 | 구독료 + $5-20 | 구독료 + $3-5 |
| 합계 (API) | $2-5 | $7-25 | $5-10 |

#### 기능 비교

| 기능 | GitHub Actions | VPS | 미니PC |
|------|---------------|-----|--------|
| 설정 난이도 | 쉬움 | 보통 | 어려움 |
| 실행 시간 제한 | 6시간/Job | 없음 | 없음 |
| 스케일링 | 자동 | 수동 | 제한적 |
| 유지보수 | 불필요 | 필요 | 필요 |
| GitHub 연동 | 최적 | 설정 필요 | 설정 필요 |
| 커스텀 소프트웨어 | 제한적 | 자유로움 | 자유로움 |
| 네트워크 안정성 | 높음 | 높음 | 가정 인터넷에 의존 |
| GPU 사용 | 불가 | 가능 (추가 비용) | 가능 |

### 추천 시나리오

| 용도 | 추천 방식 | 이유 |
|------|----------|------|
| CI/CD, PR 리뷰 | GitHub Actions | GitHub와의 연동이 최적 |
| 일일 콘텐츠 생성 | GitHub Actions | 무료 한도로 충분 |
| 장시간 크롤링/분석 | VPS | 실행 시간 제한 없음 |
| 로컬 데이터 처리 | 미니PC | 데이터 전송 불필요 |
| 복잡한 자동화 파이프라인 | VPS | 환경 커스터마이징 자유 |
| 학습/실습 | GitHub Actions | 설정이 가장 간편 |

---

## 요약

| 질문 | 답변 |
|------|------|
| 가장 저렴한 방법? | Claude Max + Public repo GitHub Actions |
| API Key 월 비용? | 일 1회 실행 기준 Sonnet ~$2-5, Haiku ~$0.5 미만 |
| 무료로 시작 가능? | Public repo + Claude Max 구독이 있다면 추가 비용 없음 |
| 비용 폭증 방지? | `--max-turns` 설정 + 조건부 실행 |
| 대규모 사용 시? | API Key + Haiku 모델 + 캐싱 전략 |

---

| 이전 | 다음 |
|------|------|
| [트러블슈팅](./troubleshooting.md) | [README](../README.md) |
