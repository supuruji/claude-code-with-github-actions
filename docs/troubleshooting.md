# 트러블슈팅 가이드

GitHub Actions에서 Claude Code를 실행할 때 발생할 수 있는 문제와 해결 방법을 정리합니다.

---

## 목차

1. [Permission Denials](#1-permission-denials)
2. [MCP 서버 시작 실패](#2-mcp-서버-시작-실패)
3. [Chrome 사용 불가](#3-chrome-사용-불가)
4. [Git Push 실패](#4-git-push-실패)
5. [OAuth 토큰 만료](#5-oauth-토큰-만료)
6. [워크플로우 타임아웃](#6-워크플로우-타임아웃)
7. [Actions 로그 분석 방법](#7-actions-로그-분석-방법)
8. [기타 문제](#8-기타-문제)

---

## 1. Permission Denials

### 증상

```
Error: Claude needs permission to use the <tool> tool.
```

Claude가 도구(파일 읽기, 명령 실행 등)를 사용하려 할 때 권한 확인 프롬프트에서 멈춥니다.

### 원인

CI 환경에서는 사용자 입력을 받을 수 없으므로, 권한 확인 프롬프트가 뜨면 작업이 중단됩니다.

### 해결

`--dangerously-skip-permissions` 플래그를 추가합니다:

```yaml
run: |
  claude -p "프롬프트 내용" \
    --output-format text \
    --dangerously-skip-permissions
```

> **주의**: 이 플래그는 모든 도구 사용을 자동 승인합니다. 프롬프트가 신뢰할 수 있는 내용인지 반드시 확인하세요.

### 부분 권한 설정이 필요한 경우

특정 도구만 허용하고 싶다면, `.claude/settings.json`에서 설정할 수 있습니다:

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": ["Bash"]
  }
}
```

---

## 2. MCP 서버 시작 실패

### 증상

```
Error: Failed to start MCP server 'fetch'
MCP server 'chrome' failed to initialize
```

### 원인과 해결

#### 원인 1: npm 패키지 설치 실패

```yaml
# 해결: 사전에 패키지 설치
- name: Pre-install MCP packages
  run: |
    npm install -g @anthropic-ai/mcp-fetch
    npm install -g @anthropic-ai/mcp-sequential-thinking
```

#### 원인 2: mcp.json 경로 오류

```yaml
# 잘못된 예
run: claude -p "..." --mcp-config mcp.json ...

# 올바른 예
run: claude -p "..." --mcp-config .claude/mcp.json ...
```

#### 원인 3: JSON 형식 오류

mcp.json 파일의 JSON 문법을 확인합니다:

```bash
# JSON 유효성 검사
- name: Validate MCP config
  run: |
    python3 -c "import json; json.load(open('.claude/mcp.json'))" \
      && echo "Valid JSON" \
      || echo "Invalid JSON"
```

#### 원인 4: npx 캐시 문제

```yaml
# npx 캐시 정리
- name: Clear npx cache
  run: |
    npx clear-npx-cache 2>/dev/null || true
    npm cache clean --force
```

### 디버깅 방법

```yaml
- name: Debug MCP server
  run: |
    # MCP 서버가 정상 실행되는지 테스트
    timeout 10 npx -y @anthropic-ai/mcp-fetch --help 2>&1 || echo "Server test complete"
```

---

## 3. Chrome 사용 불가

### 증상

```
Error: Failed to launch the browser process
Error: Chrome not found at /usr/bin/google-chrome
```

### 해결: Chrome 설치 추가

```yaml
steps:
  - name: Install Chrome
    uses: browser-actions/setup-chrome@latest
    with:
      chrome-version: stable

  - name: Verify Chrome installation
    run: |
      which google-chrome-stable || which chrome || echo "Chrome not found"
      google-chrome-stable --version 2>/dev/null || chrome --version 2>/dev/null
```

### 해결: 실행 옵션 추가

CI 환경에서는 반드시 다음 옵션이 필요합니다:

```json
{
  "mcpServers": {
    "chrome": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-puppeteer"],
      "env": {
        "PUPPETEER_LAUNCH_OPTIONS": "{\"headless\": true, \"args\": [\"--no-sandbox\", \"--disable-setuid-sandbox\", \"--disable-gpu\", \"--disable-dev-shm-usage\"]}"
      }
    }
  }
}
```

### 해결: 메모리 부족

Chrome은 메모리를 많이 사용합니다. 메모리 부족 시:

```yaml
- name: Run with memory optimization
  env:
    NODE_OPTIONS: "--max-old-space-size=4096"
  run: |
    claude -p "..." \
      --mcp-config .claude/mcp.json \
      --output-format text \
      --dangerously-skip-permissions
```

---

## 4. Git Push 실패

### 증상

```
remote: Permission to user/repo.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/user/repo.git/': The requested URL returned error: 403
```

### 원인 1: contents 쓰기 권한 없음

```yaml
# 해결: permissions에 contents: write 추가
permissions:
  contents: write
```

### 원인 2: 기본 GITHUB_TOKEN 권한 부족

Repository Settings에서 확인합니다:

```
Settings → Actions → General → Workflow permissions
→ "Read and write permissions" 선택
```

### 원인 3: 보호된 브랜치에 push

```yaml
# 해결: 별도 브랜치에 push 후 PR 생성
- name: Push to branch
  run: |
    BRANCH="auto/$(date -u +%Y%m%d-%H%M%S)"
    git checkout -b "$BRANCH"
    git add -A
    git commit -m "auto: generated content"
    git push origin "$BRANCH"

- name: Create PR
  env:
    GH_TOKEN: ${{ github.token }}
  run: |
    gh pr create \
      --title "Auto-generated content" \
      --body "Claude가 자동 생성한 콘텐츠입니다." \
      --base main \
      --head "$BRANCH"
```

### 원인 4: git config 미설정

```yaml
# 해결: 커밋 전에 git config 설정
- name: Configure git
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
```

---

## 5. OAuth 토큰 만료

### 증상

```
Error: Authentication failed
Error: Invalid or expired token
401 Unauthorized
```

### 해결

1. Claude Code CLI에서 다시 로그인:

```bash
claude login
```

2. 새 토큰을 확인:

```bash
cat ~/.claude/.credentials.json | jq -r '.oauthToken'
```

3. GitHub Secret 업데이트:

```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN --body "새-토큰-값"
```

### 토큰 갱신 주기

OAuth 토큰은 일정 기간 후 만료됩니다. 만료 시기가 가까워지면 다시 로그인하여 갱신해야 합니다.

### API Key 사용 시

API key는 명시적으로 삭제하지 않는 한 만료되지 않습니다. 토큰 관리가 번거롭다면 API key 사용을 고려하세요:

```bash
gh secret set ANTHROPIC_API_KEY --body "sk-ant-api03-xxxx..."
```

---

## 6. 워크플로우 타임아웃

### 증상

```
Error: The operation was canceled.
The job running on runner ... has exceeded the maximum execution time of 360 minutes.
```

### 해결: timeout-minutes 설정

```yaml
jobs:
  my-job:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # 기본값 360분 대신 30분으로 제한
    steps:
      - name: Run Claude
        timeout-minutes: 15  # Step 단위 타임아웃
        run: |
          claude -p "..." \
            --max-turns 10 \
            --output-format text \
            --dangerously-skip-permissions
```

### 해결: --max-turns으로 턴 수 제한

```yaml
run: |
  claude -p "간단한 작업만 수행해줘" \
    --max-turns 5 \
    --output-format text \
    --dangerously-skip-permissions
```

### 해결: 작업 분할

하나의 큰 작업을 여러 Job으로 분할합니다:

```yaml
jobs:
  step-1:
    timeout-minutes: 10
    steps:
      - run: claude -p "1단계 작업" --max-turns 5 ...

  step-2:
    needs: step-1
    timeout-minutes: 10
    steps:
      - run: claude -p "2단계 작업" --max-turns 5 ...
```

---

## 7. Actions 로그 분석 방법

### 로그 확인 순서

1. **Actions 탭** → 실행된 워크플로우 클릭
2. **Job 이름** 클릭
3. 실패한 **Step** 클릭하여 펼치기
4. 에러 메시지 확인

### CLI로 로그 확인

```bash
# 최근 실행 목록
gh run list --limit 5

# 실패한 실행만 보기
gh run list --status failure

# 특정 실행의 로그 확인
gh run view <run-id>

# 상세 로그 확인
gh run view <run-id> --log

# 실패한 로그만 보기
gh run view <run-id> --log-failed
```

### 자주 보는 에러 패턴

| 에러 메시지 | 의미 | 해결 |
|------------|------|------|
| `Process completed with exit code 1` | 명령어 실행 실패 | 해당 Step의 상세 로그 확인 |
| `Resource not accessible by integration` | 토큰 권한 부족 | permissions 설정 확인 |
| `No space left on device` | 디스크 공간 부족 | 불필요한 파일 정리 Step 추가 |
| `ENOMEM` | 메모리 부족 | 작업 분할 또는 메모리 최적화 |

### 디버깅용 환경 정보 출력

```yaml
- name: Debug info
  if: failure()
  run: |
    echo "=== Node version ==="
    node --version
    echo "=== npm version ==="
    npm --version
    echo "=== Claude Code version ==="
    claude --version 2>/dev/null || echo "not installed"
    echo "=== Disk space ==="
    df -h
    echo "=== Memory ==="
    free -h
    echo "=== Environment ==="
    env | grep -E "^(GITHUB_|RUNNER_)" | sort
```

---

## 8. 기타 문제

### Claude Code 설치 실패

```yaml
# 특정 버전 설치
- name: Install Claude Code
  run: |
    npm install -g @anthropic-ai/claude-code@latest
    claude --version
```

### 한국어 출력 깨짐

```yaml
# 로케일 설정
- name: Set locale
  run: |
    sudo locale-gen ko_KR.UTF-8 || true
    export LANG=ko_KR.UTF-8
    export LC_ALL=ko_KR.UTF-8
```

### 스케줄 워크플로우가 실행되지 않음

- 저장소에 최근 60일 내 활동(push, Issue 등)이 없으면 스케줄이 비활성화됩니다
- 기본 브랜치(main/master)에 워크플로우 파일이 있어야 합니다
- cron 시간은 UTC 기준입니다
- GitHub 부하에 따라 지연될 수 있습니다

```yaml
# 스케줄이 동작하지 않을 때: workflow_dispatch로 수동 테스트
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:  # 수동 실행으로 테스트
```

### 동시 실행 방지

```yaml
# 같은 워크플로우가 동시에 실행되는 것을 방지
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

## 빠른 참조 테이블

| 문제 | 가장 먼저 확인할 것 |
|------|-------------------|
| Permission denied | `--dangerously-skip-permissions` 플래그 |
| MCP 서버 실패 | `.claude/mcp.json` 경로 및 JSON 형식 |
| Chrome 실행 불가 | `setup-chrome` Action 추가 여부 |
| git push 실패 | `permissions: contents: write` 설정 |
| 토큰 만료 | Secret 값 갱신 |
| 타임아웃 | `--max-turns` 및 `timeout-minutes` 설정 |

---

| 이전 | 다음 |
|------|------|
| [Step 5: 고급 패턴](./05-advanced-patterns.md) | [비용 가이드](./cost-guide.md) |
