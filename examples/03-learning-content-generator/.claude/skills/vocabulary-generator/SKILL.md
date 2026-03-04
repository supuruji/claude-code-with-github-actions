---
name: vocabulary-generator
description: Generate structured vocabulary learning content with definitions, examples, and practice exercises
triggers:
  - generate vocabulary
  - vocabulary content
  - learning materials
---

# Vocabulary Generator

## Steps

### 1. Duplicate Check
Run the duplicate checker to get previously used words:
```bash
python3 .claude/skills/vocabulary-generator/scripts/check_duplicates.py output/
```
Store the output list and ensure no selected words overlap.

### 2. Word Selection
Read the vocabulary guide:
```
.claude/skills/vocabulary-generator/references/vocabulary-guide.md
```

Select the target number of words following these criteria:
- Matches the specified difficulty level
- Not in the duplicate list
- Mix of parts of speech (aim for ~40% nouns, ~30% verbs, ~20% adjectives, ~10% adverbs)
- Practical usage in professional, academic, or everyday contexts

### 3. Definitions
For each word, prepare:
- Primary definition (most common usage)
- Secondary definition (if applicable)
- Part of speech
- IPA pronunciation
- Word origin/etymology (brief)

### 4. Example Sentences
Write 2-3 example sentences per word:
- One in a professional/business context
- One in an academic/formal context
- One in an everyday/casual context

Each sentence should make the word's meaning clear from context.

### 5. Practice Questions
Create three types of exercises:

**Multiple Choice** (5 questions):
- Stem: sentence or definition
- 4 options (1 correct, 3 distractors)
- Distractors should be same part of speech and similar difficulty

**Fill-in-the-Blank** (5 questions):
- Sentence with the target word removed
- Word bank provided
- Context clues should guide the answer

**Matching** (5 questions):
- Column A: words
- Column B: definitions (shuffled)
- Clear, unambiguous matches

### 6. Learning Tips
For each word, include one of the following:
- Mnemonic device
- Word root breakdown
- Related words / word family
- Common mistake to avoid
- Collocation pattern

### 7. Save File
Read the template:
```
.claude/skills/vocabulary-generator/assets/template.md
```

Fill in all sections and save to:
```
output/YYYY-MM-DD-HH-vocabulary.md
```

Verify the file was written correctly by reading it back.
