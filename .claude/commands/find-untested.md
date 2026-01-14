---
description: Find source files without corresponding test files
argument-hint: [path] [--coverage]
allowed-tools: Bash(npm test:*)
---

# Find Untested Files Command

Find source files that don't have corresponding test files.

**Arguments:** `$ARGUMENTS`

---

## Step 1: Parse Arguments

```
If $ARGUMENTS contains "--coverage":
  MODE = "coverage"  # Run real Jest coverage
  Remove "--coverage" from $ARGUMENTS
Else:
  MODE = "quick"     # Just check if test files exist

SCAN_PATH = $ARGUMENTS is empty ? "src/" : $ARGUMENTS
```

---

## Step 2: Find Source Files

Use Glob to find source files:

```
Patterns: **/*.ts, **/*.tsx, **/*.js, **/*.jsx
Exclude: node_modules, *.test.*, *.spec.*, __tests__/, __mocks__/
```

---

## Step 3: Apply Exclusions

Skip files that typically don't need direct tests:

| Pattern | Reason |
|---------|--------|
| `index.ts` / `index.tsx` | Barrel exports |
| `*.d.ts` | Type definitions |
| `*.types.ts` | Type-only files |
| `*.styles.ts` | Style definitions |
| `*.constants.ts` | Pure constants |
| `*.config.ts` | Configuration |

Store filtered list as `TESTABLE_FILES`.

---

## Step 4: Quick Mode (Default)

**If MODE = "quick":**

For each file in `TESTABLE_FILES`, check if test file exists:

```
Source: src/components/Button.tsx

Check for (in order):
1. src/components/Button.test.tsx
2. src/components/Button.test.ts
3. src/components/Button.spec.tsx
4. src/components/__tests__/Button.test.tsx
```

Use Glob to verify each pattern.

Categorize:
- `WITH_TESTS` - has a test file
- `WITHOUT_TESTS` - missing test file

**Skip to Output**

---

## Step 5: Coverage Mode (--coverage flag)

**If MODE = "coverage":**

Run Jest with fresh coverage (always run fresh, don't use old coverage/ folder):

```bash
npm test -- --coverage --watchAll=false
```

**Note:** If `scripts.test` is path-based (`jest src/`), the command still works for coverage.

Parse Jest console output to extract:
- File paths
- % Statements, Branches, Functions, Lines

Categorize:
- `COVERED` - files with >0% coverage
- `UNCOVERED` - files with 0% coverage
- `LOW_COVERAGE` - files with <50% line coverage

---

## Step 6: Categorize by Type

Group files by type for organized output:

| Pattern | Category |
|---------|----------|
| `components/` or `.tsx` with JSX | Components |
| `hooks/` or `use*.ts` | Hooks |
| `utils/` or `helpers/` | Utils |
| `services/` or `api/` | Services |
| Other | Other |

---

## Output

### Quick Mode Output

```
Untested Files Report
───────────────────────────────────────
Scanned: [path]
Source files: [total]
With test files: [count]
Missing test files: [count]
───────────────────────────────────────

Missing Test Files:

Components ([count]):
  • src/components/Modal.tsx
  • src/components/Tooltip.tsx

Hooks ([count]):
  • src/hooks/useDebounce.ts

Utils ([count]):
  • src/utils/validators.ts

Services ([count]):
  • src/services/analytics.ts
───────────────────────────────────────

To write tests: /write-tests [file]
For real coverage: /find-untested --coverage
```

### Coverage Mode Output

```
Coverage Report (Fresh Run)
───────────────────────────────────────
Command: npm test -- --coverage

Overall:
  Statements: XX.X%
  Branches: XX.X%
  Functions: XX.X%
  Lines: XX.X%
───────────────────────────────────────

Uncovered Files (0% coverage):
  • src/components/Modal.tsx
  • src/hooks/useDebounce.ts

Low Coverage (<50% lines):
  • src/components/Form.tsx (32%)
  • src/services/api.ts (45%)
───────────────────────────────────────

To write tests: /write-tests [file]
```

---

## Notes

- **Quick mode** is fast but only checks if test files exist (not quality)
- **Coverage mode** runs all tests (slower but accurate)
- Coverage mode always runs fresh - ignores old `coverage/` folder
- Use quick mode for daily checks, coverage mode for CI/reviews

---

## Quick Reference

```
/find-untested                      # Quick: check if test files exist
/find-untested src/components       # Quick: specific directory
/find-untested --coverage           # Accurate: run Jest coverage
```
