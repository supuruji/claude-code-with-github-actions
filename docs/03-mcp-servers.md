# Step 3: MCP 서버 연결

세 번째 실습에서는 MCP(Model Context Protocol) 서버를 활용하여 Claude Code의 능력을 확장하는 방법을 배웁니다. 웹페이지 가져오기, 브라우저 자동화, 단계적 사고 등 다양한 도구를 연결합니다.

---

## 목차

1. [MCP 개념 이해하기](#1-mcp-개념-이해하기)
2. [사용 가능한 MCP 서버](#2-사용-가능한-mcp-서버)
3. [MCP Config JSON 형식](#3-mcp-config-json-형식)
4. [GitHub Actions에서 Chrome 설정](#4-github-actions에서-chrome-설정)
5. [MCP 도구 네이밍 규칙](#5-mcp-도구-네이밍-규칙)
6. [디버깅 팁](#6-디버깅-팁)
7. [실습 과제](#7-실습-과제)

---

## 1. MCP 개념 이해하기

### MCP란?

**Model Context Protocol (MCP)**은 AI 모델에 외부 도구를 연결하는 표준 프로토콜입니다. MCP 서버를 연결하면 Claude가 다음과 같은 추가 능력을 갖게 됩니다:

- 웹페이지 내용 가져오기
- 브라우저 자동화 (스크린샷, 클릭, 입력)
- 데이터베이스 조회
- 외부 API 호출
- 복잡한 문제의 단계적 사고

### MCP 동작 방식

```
GitHub Actions Runner
├── Claude Code CLI
│   ├── MCP Server 1 (fetch)         ← 웹페이지 가져오기
│   ├── MCP Server 2 (chrome)        ← 브라우저 제어
│   └── MCP Server 3 (thinking)      ← 단계적 사고
│
└── Claude가 필요에 따라 MCP 도구를 호출
```

Claude는 프롬프트의 맥락에 따라 적절한 MCP 도구를 자동으로 선택하여 사용합니다.

---

## 2. 사용 가능한 MCP 서버

### sequential-thinking

복잡한 문제를 단계별로 분해하여 사고하는 서버입니다.

| 항목 | 내용 |
|------|------|
| **패키지** | `@anthropic-ai/mcp-sequential-thinking` |
| **용도** | 복잡한 분석, 다단계 의사결정, 논리적 추론 |
| **도구** | `mcp__sequential-thinking__sequentialThinking` |

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-sequential-thinking"]
    }
  }
}
```

### fetch

웹페이지 내용을 가져오는 서버입니다.

| 항목 | 내용 |
|------|------|
| **패키지** | `@anthropic-ai/mcp-fetch` |
| **용도** | 웹페이지 크롤링, API 응답 가져오기, RSS 피드 읽기 |
| **도구** | `mcp__fetch__fetch` |

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-fetch"]
    }
  }
}
```

### chrome-devtools (Puppeteer 기반)

Headless Chrome 브라우저를 제어하는 서버입니다.

| 항목 | 내용 |
|------|------|
| **패키지** | `@anthropic-ai/mcp-chrome-devtools` (또는 Puppeteer 기반 서버) |
| **용도** | 스크린샷 촬영, 웹 자동화, 폼 입력, 클릭 |
| **주요 도구** | `navigate`, `screenshot`, `click`, `type` 등 |

```json
{
  "mcpServers": {
    "chrome": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-puppeteer"],
      "env": {
        "PUPPETEER_LAUNCH_OPTIONS": "{\"headless\": true, \"args\": [\"--no-sandbox\", \"--disable-setuid-sandbox\"]}"
      }
    }
  }
}
```

---

## 3. MCP Config JSON 형식

### 설정 파일 위치

MCP 서버 설정은 `.claude/mcp.json` 파일 또는 Claude Code CLI의 `--mcp-config` 옵션으로 지정합니다.

### 기본 형식

```json
{
  "mcpServers": {
    "<서버-이름>": {
      "command": "<실행-명령어>",
      "args": ["<인자1>", "<인자2>"],
      "env": {
        "<환경변수>": "<값>"
      }
    }
  }
}
```

### 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| `command` | O | MCP 서버 실행 명령어 (예: `npx`, `node`, `python`) |
| `args` | O | 명령어에 전달할 인자 배열 |
| `env` | X | 서버에 전달할 환경 변수 |

### 여러 서버 동시 사용

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-fetch"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-sequential-thinking"]
    }
  }
}
```

### 워크플로우에서 MCP Config 사용

```yaml
- name: Run Claude with MCP
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  run: |
    # 방법 1: --mcp-config 옵션
    claude -p "웹페이지를 분석해줘" \
      --mcp-config .claude/mcp.json \
      --output-format text \
      --dangerously-skip-permissions

    # 방법 2: 프로젝트 루트에 .claude/mcp.json이 있으면 자동 로드
    claude -p "웹페이지를 분석해줘" \
      --output-format text \
      --dangerously-skip-permissions
```

---

## 4. GitHub Actions에서 Chrome 설정

Headless Chrome을 GitHub Actions에서 사용하려면 추가 설정이 필요합니다.

### Chrome 설치

```yaml
steps:
  - name: Install Chrome
    uses: browser-actions/setup-chrome@latest
    with:
      chrome-version: stable

  - name: Verify Chrome
    run: chrome --version
```

### Puppeteer MCP와 함께 사용

```yaml
- name: Run Claude with Chrome MCP
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    PUPPETEER_EXECUTABLE_PATH: /usr/bin/google-chrome-stable
  run: |
    claude -p "https://example.com 페이지의 스크린샷을 찍고 내용을 분석해줘" \
      --mcp-config .claude/mcp.json \
      --output-format text \
      --dangerously-skip-permissions
```

### MCP Config에서 Chrome 경로 지정

```json
{
  "mcpServers": {
    "chrome": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-puppeteer"],
      "env": {
        "PUPPETEER_LAUNCH_OPTIONS": "{\"headless\": true, \"executablePath\": \"/usr/bin/google-chrome-stable\", \"args\": [\"--no-sandbox\", \"--disable-setuid-sandbox\", \"--disable-gpu\", \"--disable-dev-shm-usage\"]}"
      }
    }
  }
}
```

### Chrome 실행 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--headless` | GUI 없이 실행 |
| `--no-sandbox` | 샌드박스 비활성화 (CI 환경에서 필요) |
| `--disable-setuid-sandbox` | setuid 샌드박스 비활성화 |
| `--disable-gpu` | GPU 가속 비활성화 (서버 환경) |
| `--disable-dev-shm-usage` | /dev/shm 사용 비활성화 (메모리 이슈 방지) |

---

## 5. MCP 도구 네이밍 규칙

Claude가 MCP 도구를 호출할 때 사용하는 이름 규칙입니다.

### 형식

```
mcp__<서버이름>__<도구이름>
```

### 예시

| MCP 서버 | 도구 | 전체 이름 |
|----------|------|-----------|
| fetch | fetch | `mcp__fetch__fetch` |
| sequential-thinking | sequentialThinking | `mcp__sequential-thinking__sequentialThinking` |
| chrome | navigate | `mcp__chrome__navigate` |
| chrome | screenshot | `mcp__chrome__screenshot` |
| chrome | click | `mcp__chrome__click` |

### 프롬프트에서 도구 지정

Claude가 특정 MCP 도구를 사용하도록 프롬프트에서 명시할 수 있습니다:

```yaml
run: |
  claude -p "mcp__fetch__fetch 도구를 사용해서 \
    https://news.ycombinator.com 의 내용을 가져와서 \
    상위 5개 뉴스를 요약해줘" \
    --mcp-config .claude/mcp.json \
    --output-format text \
    --dangerously-skip-permissions
```

---

## 6. 디버깅 팁

### MCP 서버 시작 실패 시

```yaml
# 서버가 정상 설치되는지 먼저 확인
- name: Test MCP server
  run: |
    npx -y @anthropic-ai/mcp-fetch --help || echo "fetch server check done"
    npx -y @anthropic-ai/mcp-sequential-thinking --help || echo "thinking server check done"
```

### 로그 레벨 높이기

```yaml
- name: Run Claude with debug
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    CLAUDE_CODE_DEBUG: "true"
  run: |
    claude -p "..." \
      --mcp-config .claude/mcp.json \
      --output-format text \
      --dangerously-skip-permissions \
      --verbose
```

### 일반적인 문제와 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| MCP 서버 연결 실패 | npx 패키지 설치 실패 | `npm install -g <패키지>` 로 먼저 설치 |
| Chrome 실행 불가 | Chrome 미설치 | `setup-chrome` Action 추가 |
| 타임아웃 | MCP 서버 응답 지연 | `--max-turns` 옵션으로 제한 |
| 도구를 찾을 수 없음 | mcp.json 경로 오류 | 파일 경로 및 JSON 형식 확인 |

---

## 7. 실습 과제

### 과제 1: fetch MCP로 웹페이지 요약

fetch MCP 서버를 연결하여 웹페이지를 가져오고 요약하는 워크플로우를 만들어 보세요.

#### 1단계: MCP 설정 파일 생성

`.claude/mcp.json`:
```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-fetch"]
    }
  }
}
```

#### 2단계: 워크플로우 작성

```yaml
name: "Web Summary with MCP"

on:
  workflow_dispatch:
    inputs:
      url:
        description: '요약할 웹페이지 URL'
        required: true
        default: 'https://news.ycombinator.com'

jobs:
  summarize:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Summarize webpage
        env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
        run: |
          claude -p "fetch 도구를 사용해서 ${{ github.event.inputs.url }}의 \
            내용을 가져오고, 핵심 내용을 한국어로 요약해서 \
            summaries/$(date -u +%Y-%m-%d).md 파일로 저장해줘" \
            --mcp-config .claude/mcp.json \
            --output-format text \
            --dangerously-skip-permissions

      - name: Commit summary
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "auto: web summary"
          git push
```

### 과제 2: sequential-thinking으로 코드 분석

복잡한 코드 분석에 sequential-thinking MCP를 활용해 보세요.

```yaml
- name: Analyze with thinking
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  run: |
    claude -p "sequential-thinking 도구를 활용해서 \
      이 프로젝트의 아키텍처를 단계별로 분석하고 \
      개선 제안을 작성해줘" \
      --mcp-config .claude/mcp.json \
      --output-format text \
      --dangerously-skip-permissions
```

### 과제 3: 여러 MCP 서버 조합

fetch와 sequential-thinking을 동시에 사용하여 웹 콘텐츠를 분석하는 워크플로우를 만들어 보세요.

---

## 다음 단계

MCP 서버 연결에 성공했다면, 다음 단계에서는 **Skills와 Agents를 활용하여 재사용 가능한 자동화 패턴**을 만드는 방법을 배웁니다.

---

| 이전 | 다음 |
|------|------|
| [Step 2: 스케줄 자동화](./02-scheduled-automation.md) | [Step 4: Skills & Agents](./04-skills-and-agents.md) |
