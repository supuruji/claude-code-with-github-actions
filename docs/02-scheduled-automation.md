# Step 2: 스케줄 자동화

두 번째 실습에서는 Claude Code를 스케줄에 따라 자동으로 실행하는 방법을 배웁니다. cron 문법, 자동 커밋/푸시 패턴, 프롬프트 작성 팁을 다룹니다.

---

## 목차

1. [Cron 문법 이해하기](#1-cron-문법-이해하기)
2. [Cron 표현식 예시](#2-cron-표현식-예시)
3. [workflow_dispatch로 테스트하기](#3-workflow_dispatch로-테스트하기)
4. [Git Commit/Push 자동화 패턴](#4-git-commitpush-자동화-패턴)
5. [프롬프트 작성 팁](#5-프롬프트-작성-팁)
6. [실행 모니터링](#6-실행-모니터링)
7. [실습 과제](#7-실습-과제)

---

## 1. Cron 문법 이해하기

GitHub Actions의 `schedule` 트리거는 cron 표현식을 사용합니다.

### 기본 구조

```
┌───────────── 분 (0-59)
│ ┌───────────── 시 (0-23)
│ │ ┌───────────── 일 (1-31)
│ │ │ ┌───────────── 월 (1-12)
│ │ │ │ ┌───────────── 요일 (0-6, 일요일=0)
│ │ │ │ │
* * * * *
```

### 특수 문자

| 문자 | 의미 | 예시 |
|------|------|------|
| `*` | 모든 값 | `* * * * *` = 매분 |
| `,` | 여러 값 | `0,30 * * * *` = 매시 0분, 30분 |
| `-` | 범위 | `1-5` = 월~금 (요일) |
| `/` | 간격 | `*/15 * * * *` = 15분마다 |

> **주의**: GitHub Actions의 cron 시간은 **UTC 기준**입니다. 한국 시간(KST)은 UTC+9이므로, KST 오전 9시 = UTC 0시입니다.

---

## 2. Cron 표현식 예시

| 표현식 | 의미 | KST 기준 |
|--------|------|----------|
| `0 * * * *` | 매시간 정각 | 매시간 정각 |
| `0 0 * * *` | 매일 UTC 0시 | 매일 오전 9시 |
| `30 1 * * *` | 매일 UTC 1:30 | 매일 오전 10:30 |
| `0 0 * * 1-5` | 평일 UTC 0시 | 평일 오전 9시 |
| `0 0 * * 1` | 매주 월요일 UTC 0시 | 매주 월요일 오전 9시 |
| `0 0 1 * *` | 매월 1일 UTC 0시 | 매월 1일 오전 9시 |
| `*/30 * * * *` | 30분마다 | 30분마다 |
| `0 */6 * * *` | 6시간마다 | 6시간마다 |
| `0 0 * * 0` | 매주 일요일 UTC 0시 | 매주 일요일 오전 9시 |

### 워크플로우에서 사용 예시

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # 매일 KST 오전 9시
```

> **팁**: [crontab.guru](https://crontab.guru)에서 cron 표현식을 테스트해볼 수 있습니다.

> **참고**: GitHub Actions의 스케줄은 정확한 시각에 실행되지 않을 수 있습니다. 부하에 따라 최대 수분~수십 분 지연될 수 있습니다.

---

## 3. workflow_dispatch로 테스트하기

스케줄 워크플로우를 개발할 때는 `workflow_dispatch`를 함께 설정하여 수동으로 테스트합니다.

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # 실제 스케줄
  workflow_dispatch:       # 수동 실행 (테스트용)
```

### 테스트 과정

1. `workflow_dispatch`를 추가하고 push
2. Actions 탭에서 **"Run workflow"** 클릭하여 수동 실행
3. 로그 확인 및 결과 검증
4. 정상 동작 확인 후 스케줄 대기

```bash
# CLI로 수동 실행
gh workflow run "Step 2 - Scheduled Automation" --ref main
```

---

## 4. Git Commit/Push 자동화 패턴

Claude가 생성한 결과물을 자동으로 커밋하고 푸시하는 패턴입니다.

### 기본 패턴

```yaml
jobs:
  scheduled-task:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # push 권한 필요
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude
        env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
        run: |
          claude -p "오늘의 TIL(Today I Learned)을 작성해서 til/ 폴더에 저장해줘" \
            --output-format text \
            --dangerously-skip-permissions

      - name: Commit and Push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          # 변경사항이 있을 때만 커밋
          git diff --staged --quiet || git commit -m "auto: daily TIL update"
          git push
```

### 핵심 포인트

| 항목 | 설명 |
|------|------|
| `permissions: contents: write` | 저장소에 push할 수 있는 권한 부여 |
| `git config` | 커밋 작성자를 GitHub Actions 봇으로 설정 |
| `git diff --staged --quiet \|\| git commit` | 변경사항이 있을 때만 커밋 (빈 커밋 방지) |

### 날짜 기반 파일명 패턴

```yaml
- name: Run Claude with date
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  run: |
    DATE=$(date -u +%Y-%m-%d)
    claude -p "오늘 날짜(${DATE})를 파일명에 포함하여 \
      daily/${DATE}.md 파일을 생성해줘. \
      내용은 오늘의 프로그래밍 팁 하나를 작성해줘." \
      --output-format text \
      --dangerously-skip-permissions
```

---

## 5. 프롬프트 작성 팁

자율 실행 환경에서의 프롬프트는 대화형과 다릅니다. Claude가 한 번에 올바른 결과를 만들어야 합니다.

### 원칙 1: 구체적으로 작성

```yaml
# 나쁜 예
run: claude -p "뭔가 유용한 글을 써줘" ...

# 좋은 예
run: |
  claude -p "다음 조건으로 기술 블로그 포스트를 작성해줘:
  - 주제: GitHub Actions 초보자 가이드
  - 길이: 500-800자
  - 형식: Markdown
  - 저장 위치: posts/$(date -u +%Y-%m-%d)-github-actions.md
  - 어조: 친근하고 쉽게 설명" \
    --output-format text \
    --dangerously-skip-permissions
```

### 원칙 2: 출력 형식 명시

```yaml
run: |
  claude -p "분석 결과를 다음 형식으로 작성해줘:
  ## 요약
  (3줄 이내)

  ## 상세 분석
  (항목별 설명)

  ## 권장 사항
  (번호 매기기)" \
    --output-format text \
    --dangerously-skip-permissions
```

### 원칙 3: 파일 경로 명시

```yaml
run: |
  claude -p "결과를 output/report.md 파일로 저장해줘. \
    폴더가 없으면 생성해줘." \
    --output-format text \
    --dangerously-skip-permissions
```

### 원칙 4: 실패 시 행동 지정

```yaml
run: |
  claude -p "package.json이 있으면 의존성을 분석해줘. \
    없으면 '해당 파일 없음'이라고 출력해줘." \
    --output-format text \
    --dangerously-skip-permissions
```

---

## 6. 실행 모니터링

### Actions 로그 확인법

1. **Actions** 탭 클릭
2. 실행된 워크플로우 이름 클릭
3. Job 이름 클릭 (예: `scheduled-task`)
4. 각 Step을 펼쳐서 로그 확인

### 로그에서 확인할 항목

- Claude Code 설치 성공 여부
- Claude 실행 결과 (프롬프트 응답)
- git commit/push 성공 여부
- 에러 메시지 (있는 경우)

### 실패 알림 설정

워크플로우 실패 시 이메일 알림을 받으려면:

```
GitHub → Settings → Notifications → Actions → Email notifications 활성화
```

### CLI로 실행 상태 확인

```bash
# 최근 워크플로우 실행 목록
gh run list --workflow "Step 2 - Scheduled Automation"

# 특정 실행의 로그 확인
gh run view <run-id> --log
```

---

## 7. 실습 과제

### 과제 1: 스케줄 변경

cron 표현식을 수정하여 원하는 시간에 실행되도록 변경해 보세요.

```yaml
on:
  schedule:
    # 예: 매주 월요일 KST 오전 10시 (UTC 1시)
    - cron: '0 1 * * 1'
  workflow_dispatch:
```

### 과제 2: 프롬프트 변경

Claude에게 다른 종류의 콘텐츠를 생성하도록 프롬프트를 수정해 보세요.

아이디어:
- 매일 프로그래밍 퀴즈 생성
- 주간 기술 뉴스 요약
- 일일 코드 리뷰 체크리스트
- 매일 다른 디자인 패턴 설명

### 과제 3: 조건부 커밋

특정 조건에서만 커밋하도록 로직을 추가해 보세요.

```yaml
- name: Conditional commit
  run: |
    # 파일이 실제로 생성되었을 때만 커밋
    if [ -f "output/today.md" ]; then
      git add output/
      git commit -m "auto: add daily content"
      git push
    else
      echo "No output generated, skipping commit"
    fi
```

---

## 다음 단계

스케줄 자동화에 성공했다면, 다음 단계에서는 **MCP 서버를 연결하여 Claude의 능력을 확장**하는 방법을 배웁니다.

---

| 이전 | 다음 |
|------|------|
| [Step 1: Hello Claude](./01-hello-claude.md) | [Step 3: MCP 서버](./03-mcp-servers.md) |
