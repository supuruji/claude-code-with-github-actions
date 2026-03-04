# Step 1: Hello Claude

첫 번째 실습에서는 GitHub Actions에서 Claude Code를 실행하고, Issue에서 Claude와 대화하는 방법을 배웁니다.

---

## 목차

1. [저장소 Fork하기](#1-저장소-fork하기)
2. [Secret 설정하기](#2-secret-설정하기)
3. [수동으로 워크플로우 실행하기](#3-수동으로-워크플로우-실행하기)
4. [Issue에서 Claude 호출하기](#4-issue에서-claude-호출하기)
5. [워크플로우 YAML 상세 설명](#5-워크플로우-yaml-상세-설명)
6. [실습 과제](#6-실습-과제)

---

## 1. 저장소 Fork하기

```bash
# GitHub CLI로 Fork
gh repo fork <원본-repo-URL> --clone
cd claude-code-with-github-actions

# 또는 GitHub 웹에서 Fork 버튼 클릭 후 클론
git clone https://github.com/<your-username>/claude-code-with-github-actions.git
cd claude-code-with-github-actions
```

Fork한 저장소에서 **Actions 탭**으로 이동하여 워크플로우를 활성화합니다:

> "I understand my workflows, go ahead and enable them" 클릭

---

## 2. Secret 설정하기

[사전 준비 가이드](./00-prerequisites.md#4-github-repository-secrets-설정)를 참고하여 토큰을 등록합니다.

```bash
# CLI로 빠르게 설정
gh secret set CLAUDE_CODE_OAUTH_TOKEN --body "your-token-here"
```

---

## 3. 수동으로 워크플로우 실행하기

### Actions 탭에서 실행

1. 저장소의 **Actions** 탭으로 이동
2. 좌측 목록에서 **"Step 1 - Hello Claude"** 워크플로우 선택
3. 우측의 **"Run workflow"** 드롭다운 클릭
4. Branch 선택 (기본: `main`)
5. **"Run workflow"** 버튼 클릭

### 실행 결과 확인

1. 실행 중인 워크플로우를 클릭
2. Job 이름을 클릭하여 상세 로그 확인
3. 각 Step의 출력을 확인

성공하면 로그에 Claude의 응답이 표시됩니다:

```
Run claude -p "..." --output-format text
Hello! I'm Claude, running inside GitHub Actions...
```

---

## 4. Issue에서 Claude 호출하기

### Issue 생성 및 멘션

1. 저장소의 **Issues** 탭으로 이동
2. **New Issue** 클릭
3. 제목과 본문을 작성하고 `@claude`를 멘션

```markdown
제목: Claude에게 인사하기

본문:
@claude 안녕하세요! 이 저장소의 구조를 설명해주세요.
```

4. Issue를 생성하면 Claude가 자동으로 댓글을 달아 응답합니다.

> **참고**: `@claude` 멘션이 작동하려면 관련 워크플로우가 `issue_comment` 이벤트를 트리거하도록 설정되어 있어야 합니다.

---

## 5. 워크플로우 YAML 상세 설명

`step-01-hello-claude.yml` 파일의 각 부분을 살펴봅니다:

```yaml
name: "Step 1 - Hello Claude"
```

워크플로우의 이름입니다. Actions 탭의 좌측 목록에 표시됩니다.

```yaml
on:
  workflow_dispatch:
```

`workflow_dispatch`는 Actions 탭에서 수동으로 실행할 수 있게 하는 트리거입니다. "Run workflow" 버튼이 활성화됩니다.

```yaml
permissions:
  contents: read
  issues: write
```

이 워크플로우에 부여할 GitHub 토큰 권한입니다:
- `contents: read` - 저장소 내용 읽기
- `issues: write` - Issue에 댓글 작성

```yaml
jobs:
  hello-claude:
    runs-on: ubuntu-latest
```

Job 정의입니다. `ubuntu-latest` 환경에서 실행됩니다.

```yaml
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
```

저장소 코드를 Runner에 체크아웃합니다. Claude가 저장소 파일을 읽을 수 있게 됩니다.

```yaml
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
```

Claude Code CLI를 전역으로 설치합니다.

```yaml
      - name: Run Claude
        env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
        run: |
          claude -p "이 저장소의 구조를 분석하고 한국어로 설명해줘" \
            --output-format text \
            --dangerously-skip-permissions
```

핵심 실행 부분입니다:

| 옵션 | 설명 |
|------|------|
| `-p "..."` | 프롬프트를 직접 전달 (비대화형 모드) |
| `--output-format text` | 결과를 텍스트로 출력 |
| `--dangerously-skip-permissions` | 권한 확인 프롬프트 건너뛰기 (CI 환경 필수) |

### 환경 변수

```yaml
env:
  CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

GitHub Secret에 저장한 토큰을 환경 변수로 주입합니다. API key를 사용하는 경우:

```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## 6. 실습 과제

### 과제 1: 프롬프트 수정하기

워크플로우 파일의 프롬프트를 수정하여 다른 결과를 만들어 보세요.

```yaml
# 예시: README 개선 제안 요청
run: |
  claude -p "이 프로젝트의 README.md를 읽고 개선할 점을 3가지 제안해줘" \
    --output-format text \
    --dangerously-skip-permissions
```

### 과제 2: 결과를 파일로 저장하기

Claude의 출력을 파일로 저장하고 Artifact로 업로드해 보세요.

```yaml
- name: Run Claude and save output
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  run: |
    claude -p "이 저장소의 기술 스택을 분석해줘" \
      --output-format text \
      --dangerously-skip-permissions > analysis.txt

- name: Upload result
  uses: actions/upload-artifact@v4
  with:
    name: claude-analysis
    path: analysis.txt
```

### 과제 3: 여러 프롬프트 연속 실행

```yaml
- name: Multiple Claude calls
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  run: |
    echo "=== 분석 1: 구조 ==="
    claude -p "프로젝트 구조를 설명해줘" \
      --output-format text \
      --dangerously-skip-permissions

    echo "=== 분석 2: 의존성 ==="
    claude -p "package.json의 의존성을 분석해줘" \
      --output-format text \
      --dangerously-skip-permissions
```

---

## 다음 단계

수동 실행에 성공했다면, 다음 단계에서는 **스케줄 기반 자동 실행**을 배웁니다.

---

| 이전 | 다음 |
|------|------|
| [사전 준비](./00-prerequisites.md) | [Step 2: 스케줄 자동화](./02-scheduled-automation.md) |
