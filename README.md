<!-- badges area -->
<!-- [![GitHub Stars](https://img.shields.io/github/stars/joonlab/claude-code-with-github-actions?style=flat-square)](https://github.com/joonlab/claude-code-with-github-actions) -->
<!-- [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE) -->
<!-- [![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](#) -->
<!-- [![Claude Code](https://img.shields.io/badge/Claude%20Code-Anthropic-blueviolet?style=flat-square)](#) -->

# Claude Code with GitHub Actions

**미니 PC, 맥미니 없이 무료로 GitHub Actions를 통해 Claude Code 스케줄러를 만드는 템플릿**

> Build a serverless Claude Code scheduler using GitHub Actions — no Mini PC, Mac Mini, or VPS required.

---

## 📌 목차 / Table of Contents

- [Why This Project?](#-why-this-project)
- [Quick Start (5분)](#-quick-start-5분--5-minutes)
- [Workshop Steps](#-workshop-steps)
- [Use Case Examples](#-use-case-examples)
- [Architecture](#-architecture)
- [Cost Comparison](#-cost-comparison)
- [Documentation](#-documentation)
- [Based On](#-based-on)
- [License](#-license)

---

## 💡 Why This Project?

### 문제 / The Problem

AI 에이전트를 24/7 자동으로 돌리려면 항상 켜져 있는 서버가 필요합니다.

| 기존 방법 | 단점 |
|-----------|------|
| 미니 PC / 맥미니 | 초기 비용 50만원+, 전기세, 관리 부담 |
| VPS (AWS, GCP 등) | 월 1~5만원, 설정 복잡, 과금 리스크 |
| 클라우드 인스턴스 | 종량제 과금, 예상치 못한 비용 폭탄 가능 |
| OpenClaw | 설정 편의성은 높지만, 별도 플랫폼 의존 |

### 해결책 / The Solution

**GitHub Actions (무료 2,000분/월) + Claude Code = 서버리스 AI 자동화**

- 서버 구매/임대 불필요 — GitHub가 인프라를 제공합니다
- cron 스케줄로 원하는 시간에 자동 실행
- 코드와 워크플로우가 하나의 리포에 — 버전 관리 자동
- 월 2,000분 무료 (public repo는 무제한)
- Claude Code CLI를 GitHub Actions runner 위에서 직접 실행

### OpenClaw 대비 장점

| 비교 항목 | 이 프로젝트 | OpenClaw |
|-----------|------------|----------|
| 인프라 비용 | 무료 (GitHub Actions) | 무료 tier 있음 |
| 커스터마이징 | 워크플로우 YAML 직접 제어 | 플랫폼 제공 UI |
| 의존성 | GitHub만 필요 | 별도 플랫폼 계정 필요 |
| 투명성 | 오픈소스, 모든 코드 확인 가능 | 플랫폼 내부 로직 비공개 |
| 학습 가치 | GitHub Actions + CI/CD 학습 | 플랫폼 사용법 학습 |

---

## 🚀 Quick Start (5분) / 5 Minutes

### Prerequisites

- GitHub 계정
- Claude Max 구독 (OAuth 토큰 사용) 또는 Anthropic API Key

### Steps

**1. Fork this repository**

```
GitHub 웹에서 [Fork] 버튼 클릭
```

**2. Claude Code OAuth 토큰을 Secret으로 등록**

```
Settings → Secrets and variables → Actions → New repository secret

Name:  CLAUDE_CODE_OAUTH_TOKEN
Value: (Claude Code CLI에서 발급받은 OAuth 토큰)
```

> OAuth 토큰 발급: Claude Code CLI 실행 → `/login` → 토큰 복사
> API Key 대안: `ANTHROPIC_API_KEY` secret으로도 사용 가능

**3. 워크플로우 실행**

```
Actions 탭 → "Step 1 - Hello Claude" 선택 → Run workflow
```

완료! 첫 번째 Claude Code 자동화가 실행됩니다.

---

## 📋 Workshop Steps

단계별로 난이도를 높여가며 학습할 수 있도록 구성되어 있습니다.

| Step | 제목 | 설명 | 난이도 | 핵심 학습 |
|------|------|------|--------|-----------|
| **Step 1** | Hello Claude | GitHub Actions에서 Claude Code 첫 실행 | ★☆☆☆ | 워크플로우 기본 구조, Secret 설정 |
| **Step 2** | Scheduled Automation | cron으로 자동 실행 + git commit/push | ★★☆☆ | cron 표현식, git 자동화 패턴 |
| **Step 3** | MCP Servers | Chrome DevTools로 웹 브라우징 자동화 | ★★★☆ | MCP 개념, Chrome 설정, 스크린샷 |
| **Step 4** | Full Pipeline | Skills + Subagents 풀셋 파이프라인 | ★★★★ | Skills, Agents, 위임 패턴 |

각 Step의 상세 가이드는 [`docs/`](./docs/) 폴더에 있습니다.

---

## 🎯 Use Case Examples

### 1. Daily News Digest (일일 뉴스 요약)

```yaml
# 매일 오전 9시, 관심 분야 뉴스를 요약해서 Issue로 생성
schedule:
  - cron: '0 0 * * *'  # UTC 00:00 = KST 09:00
```

- Claude Code가 RSS 피드 또는 웹 검색 결과를 분석
- 핵심 뉴스 5개를 요약하여 GitHub Issue로 자동 생성
- 라벨 자동 분류 (tech, business, AI 등)

### 2. Repo Health Checker (리포 건강 체크)

```yaml
# 매주 월요일, 리포 상태를 점검하고 리포트 생성
schedule:
  - cron: '0 1 * * 1'  # 매주 월요일 UTC 01:00
```

- 오래된 Issue/PR 목록 정리
- 의존성 업데이트 필요 여부 확인
- README 및 문서 최신 상태 점검
- 결과를 마크다운 리포트로 커밋

### 3. Learning Content Generator (학습 콘텐츠 생성기)

```yaml
# 매일 저녁, 설정한 주제로 학습 자료 생성
schedule:
  - cron: '0 10 * * *'  # UTC 10:00 = KST 19:00
```

- 설정 파일에 학습 주제와 난이도 지정
- Claude Code가 퀴즈, 요약, 실습 문제 생성
- `docs/` 폴더에 날짜별로 자동 커밋

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Repository                    │
│                                                          │
│  .github/workflows/        .claude/                      │
│  ├── step1-hello.yml       ├── agents/   (Subagents)     │
│  ├── step2-scheduled.yml   └── skills/   (Skills)        │
│  ├── step3-with-mcp.yml                                  │
│  └── step4-full-pipeline.yml   output/  (generated)      │
└──────────────┬───────────────────────────────────────────┘
               │
               │  cron / workflow_dispatch / @claude
               ▼
┌──────────────────────────────────────────────────────────┐
│              GitHub Actions Runner (ubuntu-latest)         │
│                                                           │
│  1. Checkout repo                                         │
│  2. Setup Chrome (headless)                               │
│  3. Create MCP config                                     │
│  4. Run Claude Code CLI                                   │
│  5. Git commit & push results                             │
└──────────┬────────────────────┬──────────────────────────┘
           │                    │
           │ Claude Code CLI    │ MCP Protocol
           ▼                    ▼
┌──────────────────┐  ┌─────────────────────────────────┐
│  Anthropic API   │  │       MCP Servers                │
│                  │  │  ├── sequential-thinking          │
│  Claude Sonnet   │  │  ├── fetch (web pages)            │
│  + Skills        │  │  └── chrome-devtools (browser)    │
│  + Subagents     │  │      ├── Screenshots              │
│                  │  │      ├── Click / Navigate          │
└──────────────────┘  │      └── Extract text              │
                      └─────────────────────────────────┘
```

**흐름 요약:**

1. **Trigger** — cron 스케줄, 수동 실행, 또는 @claude 멘션으로 시작
2. **Setup** — Runner에서 Chrome 설치 + MCP 서버 설정
3. **Execute** — Claude Code가 MCP 도구로 웹 탐색, Skills/Agents로 콘텐츠 생성
4. **Output** — 생성된 파일 + 스크린샷을 리포에 커밋하거나 Issue/PR로 생성

---

## 💰 Cost Comparison

| 항목 | This Project | Mini PC | VPS (Lightsail) | OpenClaw |
|------|:------------:|:-------:|:---------------:|:--------:|
| **초기 비용** | 0원 | 50만원+ | 0원 | 0원 |
| **월 운영비** | 0원 (무료 tier) | 전기세 ~1만원 | $5~20/월 | 무료 tier |
| **설정 난이도** | 낮음 (Fork & Secret) | 높음 (OS, 네트워크) | 중간 (SSH, 설정) | 낮음 |
| **커스터마이징** | 높음 (YAML 직접 편집) | 최고 (풀 제어) | 높음 | 중간 |
| **실행 한도** | 2,000분/월 (무료) | 무제한 | 무제한 | tier별 상이 |
| **유지보수** | 불필요 (GitHub 관리) | 직접 관리 | 직접 관리 | 불필요 |
| **적합 대상** | 간헐적 자동화 | 상시 실행 필요 | 유연한 제어 필요 | 빠른 시작 |

> **참고**: GitHub Actions 무료 tier는 public repo의 경우 무제한, private repo는 월 2,000분입니다.
> Claude API 비용은 별도이며, 사용량에 따라 과금됩니다.

---

## 📚 Documentation

| 문서 | 설명 |
|------|------|
| [00. Prerequisites](./docs/00-prerequisites.md) | 사전 준비 (토큰 발급, Secret 설정) |
| [01. Hello Claude](./docs/01-hello-claude.md) | Step 1: 첫 실행 가이드 |
| [02. Scheduled Automation](./docs/02-scheduled-automation.md) | Step 2: cron 스케줄 자동화 |
| [03. MCP Servers](./docs/03-mcp-servers.md) | Step 3: Chrome DevTools + MCP |
| [04. Skills & Agents](./docs/04-skills-and-agents.md) | Step 4: Skills, Subagents 활용 |
| [05. Advanced Patterns](./docs/05-advanced-patterns.md) | 고급 패턴 (PR 리뷰, 이슈 분류) |
| [Troubleshooting](./docs/troubleshooting.md) | 자주 발생하는 문제 해결 |
| [Cost Guide](./docs/cost-guide.md) | 비용 가이드 및 최적화 |

---

## 🔗 Based On

이 프로젝트는 [**joonlab/claude-code-github-actions**](https://github.com/joonlab/claude-code-github-actions)를 기반으로 합니다.

원본 리포에서 GitHub Actions와 Claude Code를 연동하는 핵심 패턴을 가져왔으며,
워크숍 형태로 재구성하여 단계별 학습이 가능하도록 만들었습니다.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 JoonLab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <sub>Built with Claude Code + GitHub Actions</sub>
</p>
