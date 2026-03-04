# Step 4: Skills & Agents

네 번째 실습에서는 Claude Code의 Skills와 Agents를 활용하여 재사용 가능한 자동화 모듈을 만드는 방법을 배웁니다.

---

## 목차

1. [Skills 개념](#1-skills-개념)
2. [Skill 만들기](#2-skill-만들기)
3. [Agents 개념](#3-agents-개념)
4. [Agent 만들기](#4-agent-만들기)
5. [Skills + Agents 조합 패턴](#5-skills--agents-조합-패턴)
6. [실습 과제](#6-실습-과제)

---

## 1. Skills 개념

### Skill이란?

**Skill**은 Claude Code에게 특정 작업 방법을 가르치는 지침서입니다. `.claude/skills/` 폴더에 `SKILL.md` 파일로 정의하면, Claude가 관련 작업을 수행할 때 자동으로 해당 Skill을 참조합니다.

### 폴더 구조

```
.claude/
└── skills/
    └── <skill-name>/
        ├── SKILL.md          # 핵심: Skill 정의 파일
        ├── assets/           # 참고 이미지, 샘플 파일 등
        ├── references/       # 참조 문서
        └── scripts/          # 관련 스크립트
```

### Skill이 로드되는 시점

Claude는 프롬프트의 맥락에 따라 관련 Skill을 **자동으로 로드**합니다. 예를 들어 "블로그 글을 써줘"라는 프롬프트가 들어오면, `blog-writer` Skill이 있다면 자동으로 참조합니다.

---

## 2. Skill 만들기

### SKILL.md 기본 형식

```markdown
---
name: "blog-writer"
description: "기술 블로그 포스트를 작성하는 Skill"
---

# 블로그 작성 Skill

## 작성 규칙
- 한국어로 작성
- 마크다운 형식 사용
- 제목은 독자의 관심을 끄는 형태로
- 코드 예제 포함 필수
- 500-1000자 분량

## 구조
1. 제목 (H1)
2. 도입부 - 왜 이 주제가 중요한지
3. 본문 - 핵심 내용 (코드 예제 포함)
4. 마무리 - 요약 및 다음 단계

## 파일 저장 규칙
- 경로: `posts/YYYY-MM-DD-<slug>.md`
- slug: 영문 소문자, 하이픈 구분

## 예시

### 좋은 예
- 제목: "GitHub Actions로 CI/CD 자동화하기 - 초보자 가이드"
- 파일: `posts/2025-01-15-github-actions-cicd-guide.md`

### 나쁜 예
- 제목: "CI/CD" (너무 짧음)
- 파일: `posts/post1.md` (날짜, slug 없음)
```

### SKILL.md Frontmatter 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | O | Skill의 고유 이름 |
| `description` | O | Skill의 설명 (Claude가 로드 여부 판단에 사용) |

### 실전 예시: 코드 리뷰 Skill

`.claude/skills/code-reviewer/SKILL.md`:

```markdown
---
name: "code-reviewer"
description: "코드 리뷰를 수행하는 Skill"
---

# 코드 리뷰 Skill

## 리뷰 관점
1. **보안**: SQL injection, XSS, 인증/인가 문제
2. **성능**: N+1 쿼리, 불필요한 연산, 메모리 누수
3. **가독성**: 네이밍, 함수 길이, 주석
4. **테스트**: 테스트 커버리지, 엣지 케이스

## 출력 형식
각 이슈마다:
- 심각도: Critical / Warning / Info
- 파일: 해당 파일 경로
- 라인: 해당 라인 번호
- 설명: 문제 설명
- 제안: 수정 방법

## 리뷰 결과 저장
- 경로: `reviews/YYYY-MM-DD-<PR번호>.md`
```

### assets, references, scripts 활용

```
.claude/skills/data-analyzer/
├── SKILL.md
├── assets/
│   └── chart-template.html      # 차트 템플릿
├── references/
│   └── data-format-spec.md      # 데이터 형식 명세
└── scripts/
    └── validate-output.sh       # 출력 검증 스크립트
```

SKILL.md에서 이 파일들을 참조할 수 있습니다:

```markdown
## 차트 생성 시
- `assets/chart-template.html`을 기반으로 차트 생성
- 출력 후 `scripts/validate-output.sh`로 검증
```

---

## 3. Agents 개념

### Agent란?

**Agent**는 특정 역할을 수행하는 Claude의 분신입니다. 메인 Claude가 복잡한 작업을 수행할 때, Agent에게 하위 작업을 **위임(delegate)**할 수 있습니다.

### Agent 파일 위치

```
.claude/
└── agents/
    └── <agent-name>.md
```

### Agent 위임 방식

메인 Claude가 Agent를 호출하면, 해당 Agent가 독립적인 컨텍스트에서 작업을 수행하고 결과를 반환합니다.

```
메인 Claude
├── "이 PR을 리뷰해줘"
│   └── → code-reviewer Agent에게 위임
│       └── Agent가 리뷰 수행 후 결과 반환
│
└── "리뷰 결과를 요약해줘"
    └── → 메인 Claude가 요약
```

---

## 4. Agent 만들기

### Agent Frontmatter 형식

```markdown
---
name: "code-reviewer"
description: "코드 변경사항을 리뷰하는 에이전트"
tools:
  - Read
  - Glob
  - Grep
  - Bash
model: sonnet
skills:
  - code-reviewer
---

# 코드 리뷰 에이전트

당신은 코드 리뷰 전문가입니다.

## 작업 절차
1. 변경된 파일 목록 확인
2. 각 파일의 변경 내용 분석
3. code-reviewer Skill의 관점에 따라 리뷰
4. 리뷰 결과 작성

## 출력
리뷰 결과를 마크다운으로 작성합니다.
```

### Frontmatter 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | O | Agent의 고유 이름 |
| `description` | O | Agent의 역할 설명 |
| `tools` | X | 사용 가능한 도구 목록 |
| `model` | X | 사용할 모델 (`sonnet`, `haiku` 등) |
| `skills` | X | 참조할 Skill 목록 |

### 모델 선택 가이드

| 모델 | 특징 | 적합한 용도 |
|------|------|------------|
| `sonnet` | 균형 잡힌 성능과 속도 | 일반적인 코드 작업, 분석 |
| `haiku` | 빠르고 저렴함 | 단순 분류, 형식 변환, 요약 |
| `opus` | 최고 성능 | 복잡한 추론, 고품질 콘텐츠 |

### 실전 예시: 번역 Agent

`.claude/agents/translator.md`:

```markdown
---
name: "translator"
description: "기술 문서를 한국어로 번역하는 에이전트"
tools:
  - Read
  - Write
  - Glob
model: haiku
---

# 번역 에이전트

당신은 기술 문서 번역 전문가입니다.

## 규칙
- 기술 용어는 영어 원문 유지 (예: API, GitHub, commit)
- 자연스러운 한국어 표현 사용
- 코드 블록 내용은 번역하지 않음
- 링크는 원본 유지

## 작업 절차
1. 원본 파일 읽기
2. 번역 수행
3. 번역 결과 저장 (같은 경로, `-ko` 접미사)
```

### 실전 예시: Issue 분류 Agent

`.claude/agents/issue-classifier.md`:

```markdown
---
name: "issue-classifier"
description: "GitHub Issue를 분류하는 에이전트"
tools:
  - Bash
model: haiku
---

# Issue 분류 에이전트

## 분류 기준
- **bug**: 기존 기능의 오류
- **feature**: 새로운 기능 요청
- **docs**: 문서 관련
- **question**: 질문
- **enhancement**: 기존 기능 개선

## 출력 형식
JSON 형식으로 출력:
```json
{
  "category": "bug",
  "priority": "high",
  "summary": "로그인 페이지에서 OAuth 리다이렉트 실패"
}
```
```

---

## 5. Skills + Agents 조합 패턴

### 패턴 1: Agent가 Skill을 참조

Agent의 frontmatter에서 `skills` 필드로 Skill을 지정하면, Agent가 해당 Skill의 지침을 따릅니다.

```
.claude/
├── skills/
│   └── code-review-rules/
│       └── SKILL.md          # 리뷰 규칙 정의
└── agents/
    └── reviewer.md           # skills: [code-review-rules]
```

### 패턴 2: 멀티 Agent 파이프라인

여러 Agent가 순차적으로 작업하는 패턴입니다.

```yaml
- name: Multi-agent pipeline
  env:
    CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
  run: |
    claude -p "다음 작업을 순서대로 수행해줘:
      1. issue-classifier Agent로 최신 Issue를 분류
      2. 분류 결과에 따라 적절한 라벨 추가
      3. translator Agent로 Issue 요약을 한국어로 번역
      4. 결과를 reports/ 폴더에 저장" \
      --output-format text \
      --dangerously-skip-permissions
```

### 패턴 3: Skill로 품질 보장

Agent의 출력 품질을 Skill로 통제하는 패턴입니다.

```
# Skill: 출력 품질 기준 정의
.claude/skills/quality-standards/SKILL.md
→ 문서 형식, 어조, 필수 포함 항목 등 정의

# Agent: Skill을 참조하여 작업 수행
.claude/agents/content-writer.md
→ skills: [quality-standards]
→ Skill의 기준에 맞춰 콘텐츠 생성
```

---

## 6. 실습 과제

### 과제 1: 블로그 작성 Skill 만들기

`.claude/skills/blog-writer/SKILL.md` 파일을 생성하고, 자신만의 블로그 작성 규칙을 정의해 보세요.

포함할 내용:
- 작성 언어 및 어조
- 마크다운 구조
- 파일 명명 규칙
- 필수 포함 요소 (코드 예제, 이미지 등)

### 과제 2: 코드 리뷰 Agent 만들기

`.claude/agents/code-reviewer.md` 파일을 생성하고, 코드 리뷰 Agent를 정의해 보세요.

고려할 점:
- 어떤 도구가 필요한가? (Read, Grep, Bash 등)
- 어떤 모델이 적합한가? (복잡도에 따라 선택)
- 어떤 Skill을 참조할 것인가?

### 과제 3: Skill + Agent 조합으로 워크플로우 만들기

위에서 만든 Skill과 Agent를 활용하는 GitHub Actions 워크플로우를 만들어 보세요.

```yaml
name: "Blog Writer with Agent"

on:
  workflow_dispatch:
    inputs:
      topic:
        description: '블로그 주제'
        required: true

jobs:
  write-blog:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g @anthropic-ai/claude-code

      - name: Write blog post
        env:
          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
        run: |
          claude -p "blog-writer Skill을 참고해서 \
            '${{ github.event.inputs.topic }}' 주제로 \
            블로그 포스트를 작성해줘" \
            --output-format text \
            --dangerously-skip-permissions

      - name: Commit
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "auto: new blog post"
          git push
```

---

## 다음 단계

Skills와 Agents를 이해했다면, 다음 단계에서는 **고급 자동화 패턴**을 배웁니다. Multi-job 워크플로우, PR 자동 리뷰, 비용 최적화 등을 다룹니다.

---

| 이전 | 다음 |
|------|------|
| [Step 3: MCP 서버](./03-mcp-servers.md) | [Step 5: 고급 패턴](./05-advanced-patterns.md) |
