# 사전 준비 가이드

이 저장소의 실습을 시작하기 전에 아래 항목들을 준비해야 합니다.

---

## 목차

1. [GitHub 계정 및 Actions 활성화](#1-github-계정-및-actions-활성화)
2. [Claude 인증 준비](#2-claude-인증-준비)
3. [CLAUDE_CODE_OAUTH_TOKEN 발급](#3-claude_code_oauth_token-발급)
4. [GitHub Repository Secrets 설정](#4-github-repository-secrets-설정)
5. [저장소 Fork 또는 Template 사용](#5-저장소-fork-또는-template-사용)
6. [비용 안내](#6-비용-안내)

---

## 1. GitHub 계정 및 Actions 활성화

### GitHub 계정 확인

GitHub 계정이 없다면 [github.com](https://github.com)에서 무료 계정을 생성합니다.

### Actions 활성화 확인

1. GitHub 저장소로 이동
2. 상단 **Actions** 탭 클릭
3. "I understand my workflows, go ahead and enable them" 버튼이 보이면 클릭하여 활성화

> **참고**: Fork한 저장소에서는 Actions가 기본 비활성화 상태입니다. 반드시 수동으로 활성화해야 합니다.

### Actions 활성화 상태 확인

```
Settings → Actions → General → Actions permissions
```

"Allow all actions and reusable workflows"가 선택되어 있는지 확인합니다.

---

## 2. Claude 인증 준비

GitHub Actions에서 Claude Code를 실행하려면 인증 토큰이 필요합니다. 두 가지 방법 중 하나를 선택하세요.

### 방법 A: Claude Max 구독 (권장)

- [Claude Max](https://claude.ai) 구독이 있으면 **OAuth 토큰**을 발급받아 사용
- 구독료 외 추가 비용 없음
- 환경 변수: `CLAUDE_CODE_OAUTH_TOKEN`

### 방법 B: Anthropic API Key

- [Anthropic Console](https://console.anthropic.com)에서 API key 발급
- 사용량에 따라 토큰당 과금
- 환경 변수: `ANTHROPIC_API_KEY`

---

## 3. CLAUDE_CODE_OAUTH_TOKEN 발급

### 방법 A: Claude Code CLI에서 OAuth 토큰 복사

Claude Code CLI가 설치되어 있어야 합니다.

```bash
# Claude Code CLI 설치 (아직 없다면)
npm install -g @anthropic-ai/claude-code

# Claude Code 실행 후 로그인
claude
```

로그인 후 토큰을 확인하는 방법:

```bash
# macOS
cat ~/.claude/.credentials.json | jq -r '.oauthToken'

# 또는 Claude Code 내부에서 Settings 확인
claude config list
```

> **참고**: OAuth 토큰은 주기적으로 갱신됩니다. 만료 시 다시 로그인하여 새 토큰을 발급받아야 합니다.

### 방법 B: Anthropic API Key 사용

1. [Anthropic Console](https://console.anthropic.com) 접속
2. **API Keys** 메뉴 클릭
3. **Create Key** 클릭
4. 키 이름 입력 (예: `github-actions`)
5. 생성된 키를 안전한 곳에 복사

```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **주의**: API key는 생성 시에만 확인할 수 있습니다. 분실 시 새로 생성해야 합니다.

---

## 4. GitHub Repository Secrets 설정

발급받은 토큰을 GitHub Repository Secret으로 등록합니다.

### 설정 방법

1. GitHub 저장소 페이지에서 **Settings** 탭 클릭
2. 좌측 메뉴에서 **Secrets and variables** 클릭
3. **Actions** 클릭
4. **New repository secret** 버튼 클릭

### OAuth 토큰 사용 시

| 항목 | 값 |
|------|-----|
| **Name** | `CLAUDE_CODE_OAUTH_TOKEN` |
| **Value** | 발급받은 OAuth 토큰 |

### API Key 사용 시

| 항목 | 값 |
|------|-----|
| **Name** | `ANTHROPIC_API_KEY` |
| **Value** | `sk-ant-api03-xxxx...` |

### 설정 확인

Secret이 정상 등록되면 목록에 이름과 "Updated ..." 날짜가 표시됩니다. **값은 한 번 저장하면 다시 확인할 수 없으며**, 수정만 가능합니다.

### CLI로 설정하기 (선택)

GitHub CLI를 사용하면 터미널에서도 설정할 수 있습니다:

```bash
# OAuth 토큰 설정
gh secret set CLAUDE_CODE_OAUTH_TOKEN --body "your-oauth-token-here"

# 또는 API Key 설정
gh secret set ANTHROPIC_API_KEY --body "sk-ant-api03-xxxx..."
```

---

## 5. 저장소 Fork 또는 Template 사용

### Fork 방법 (권장)

1. 이 저장소 페이지 우측 상단의 **Fork** 버튼 클릭
2. 본인 계정으로 Fork
3. Fork한 저장소에서 **Actions** 탭 → 활성화
4. **Settings → Secrets** → 토큰 등록

```bash
# Fork 후 로컬에 클론
gh repo fork <원본-repo-URL> --clone
cd claude-code-with-github-actions
```

### Template 사용 방법

저장소가 Template으로 설정되어 있다면:

1. **Use this template** 버튼 클릭
2. 새 저장소 이름 입력
3. **Create repository** 클릭

```bash
# Template으로 생성한 저장소 클론
gh repo clone <your-username>/claude-code-with-github-actions
```

---

## 6. 비용 안내

### Claude 사용 비용

| 인증 방식 | 비용 구조 | 월 예상 비용 |
|-----------|----------|-------------|
| Claude Max (OAuth) | 구독료만 발생 | 구독료 (고정) |
| Anthropic API Key | 토큰당 과금 | 사용량에 따라 변동 |

### API Key 과금 기준 (참고)

| 모델 | Input (1M 토큰) | Output (1M 토큰) |
|------|-----------------|------------------|
| Claude Sonnet | $3 | $15 |
| Claude Haiku | $0.25 | $1.25 |

> **참고**: 최신 가격은 [Anthropic 가격 페이지](https://www.anthropic.com/pricing)에서 확인하세요.

### GitHub Actions 비용

| 저장소 유형 | 무료 한도 |
|------------|----------|
| Public repo | 2,000분/월 |
| Private repo (Free plan) | 500분/월 |
| Private repo (Pro plan) | 3,000분/월 |

> **팁**: 실습 중에는 Public repo를 사용하면 Actions 비용 걱정 없이 진행할 수 있습니다.

---

## 체크리스트

시작 전 아래 항목을 모두 확인하세요:

- [ ] GitHub 계정 보유
- [ ] GitHub Actions 활성화 완료
- [ ] Claude 인증 토큰 발급 완료 (OAuth 또는 API Key)
- [ ] Repository Secret 등록 완료
- [ ] 저장소 Fork 또는 Template 생성 완료

모든 준비가 끝났다면 첫 번째 실습으로 이동합니다.

---

| 이전 | 다음 |
|------|------|
| [README](../README.md) | [Step 1: Hello Claude](./01-hello-claude.md) |
