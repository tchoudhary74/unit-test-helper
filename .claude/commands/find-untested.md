---
description: Find source files without corresponding test files
argument-hint: [path] [--coverage]
allowed-tools: Bash(npm test:*)
---

# Find Untested Files Command

Find source files that don't have corresponding test files.

**Arguments:** `$ARGUMENTS`

---

## CRITICAL RULES

**YOU MUST:**
- Use the Glob tool directly for all file searches
- Process and categorize files in your response (not via scripts)
- Only use Bash for `npm test -- --coverage` command

**YOU MUST NOT:**
- Generate bash scripts (.sh files)
- Generate Python scripts (.py files)
- Use bash loops, arrays, or conditionals
- Create temporary files
- Use `find`, `while read`, `for`, `declare -a`, or similar bash constructs

---

## Step 1: Parse Arguments

```
MODE = $ARGUMENTS contains "--coverage" ? "coverage" : "quick"
SCAN_PATH = remaining args or "src/"
```

---

## Step 2: Find All Source Files

Call the **Glob tool** with pattern: `[SCAN_PATH]/**/*.{ts,tsx,js,jsx}`

From results, mentally filter out:
- `*.test.*` and `*.spec.*` files
- `__tests__/` and `__mocks__/` directories
- `index.ts`, `*.d.ts`, `*.types.ts`, `*.styles.ts`, `*.constants.ts`, `*.config.ts`

---

## Step 3A: Quick Mode (Default)

For each remaining source file, call the **Glob tool** to check if test exists.

Example for `src/components/Button.tsx`:
- Glob: `src/components/Button.test.{ts,tsx}`
- Glob: `src/components/Button.spec.{ts,tsx}`
- Glob: `src/components/__tests__/Button.test.{ts,tsx}`

If any match found → file has tests
If no match → add to "Missing Tests" list

---

## Step 3B: Coverage Mode (--coverage flag)

Run with **Bash tool**:
```bash
npm test -- --coverage --watchAll=false
```

Parse the Jest output table directly from the response. Identify:
- Files with 0% coverage → "Uncovered"
- Files with <50% coverage → "Low Coverage"

---

## Step 4: Output Results

Group missing/uncovered files by category:
- `components/` in path → Components
- `hooks/` in path or `use*.ts` → Hooks
- `utils/` or `helpers/` in path → Utils
- `services/` or `api/` in path → Services

### Quick Mode Output
```
Untested Files Report
───────────────────────────────────────
Scanned: [path]
Source files: [X]
With test files: [X]
Missing test files: [X]
───────────────────────────────────────

Missing Test Files:

Components ([X]):
  • src/components/Modal.tsx
  • src/components/Tooltip.tsx

Hooks ([X]):
  • src/hooks/useDebounce.ts
───────────────────────────────────────

To write tests: /write-tests [file]
```

### Coverage Mode Output
```
Coverage Report
───────────────────────────────────────
Overall: [X]% Statements, [X]% Branches, [X]% Lines

Uncovered (0%):
  • src/components/Modal.tsx

Low Coverage (<50%):
  • src/components/Form.tsx (32%)
───────────────────────────────────────
```

---

## Quick Reference

```
/find-untested                 # Quick mode
/find-untested src/components  # Specific directory
/find-untested --coverage      # Run Jest coverage
```
