---
name: news-digest-generator
description: Generate a daily tech news digest from multiple sources
triggers:
  - generate news digest
  - daily digest
  - news summary
---

# News Digest Generator

## Steps

### 1. Check for Duplicates
Run the duplicate checker to load previously covered headlines:
```bash
python3 .claude/skills/news-digest-generator/scripts/check_duplicates.py output/
```
This outputs a list of known headlines to avoid.

### 2. Visit News Sources
Navigate to each configured news source and extract content:
- **Hacker News** (https://news.ycombinator.com): Top 15 stories with points and comment counts
- **TechCrunch** (https://techcrunch.com): Top 10 featured articles with authors

For each source:
1. Navigate using chrome-devtools
2. Take a page snapshot to extract structured content
3. Take a screenshot for archival (save to `output/screenshots/`)

### 3. Extract Headlines
From each source, extract:
- Headline text
- URL
- Source name
- Metadata (points, comments, author, publish time)

Filter out any headlines that match the duplicate list from Step 1.

### 4. Generate Summary
For each story:
- Write a 1-2 sentence summary based on the headline and any available context
- Assign a category (AI, Web, Security, Startups, DevTools, Science, Other)
- Rate relevance (High / Medium / Low)

### 5. Analyze Trends
Identify 3-5 themes that appear across multiple stories:
- Name each trend
- List the related stories
- Write a brief analysis paragraph

### 6. Compose Digest
Read the template from `assets/template.md` and fill in all sections:
- Header with date and source count
- Source summary table
- Top stories by category
- Trend analysis
- Footer

### 7. Save Output
Write the completed digest to:
```
output/YYYY-MM-DD-digest.md
```

Verify the file was written correctly by reading it back.
