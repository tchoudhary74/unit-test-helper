---
description: Find source files without corresponding test files
argument-hint: [path] [--coverage]
allowed-tools: Bash(npm test:*)
---

# Find Untested Files Command

Find source files that don't have corresponding test files.

**Arguments:** `$ARGUMENTS`

**IMPORTANT:** Use Glob and Read tools directly. Do NOT generate Python/Bash scripts.

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

**Use Glob tool** with patterns:
- `[SCAN_PATH]/**/*.ts`
- `[SCAN_PATH]/**/*.tsx`
- `[SCAN_PATH]/**/*.js`
- `[SCAN_PATH]/**/*.jsx`

Exclude from results:
- Files in `node_modules/`
- Files matching `*.test.*` or `*.spec.*`
- Files in `__tests__/` or `__mocks__/`

Store as `SOURCE_FILES`.

---

## Step 3: Filter Testable Files

From `SOURCE_FILES`, exclude files that don't need tests:

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

For each file in `TESTABLE_FILES`, **use Glob tool** to check if test exists:

```
Example: src/components/Button.tsx

Use Glob to check (stop at first match):
  1. src/components/Button.test.tsx
  2. src/components/Button.test.ts
  3. src/components/Button.spec.tsx
  4. src/components/Button.spec.ts
  5. src/components/__tests__/Button.test.tsx
  6. src/components/__tests__/Button.test.ts
```

**Do this in memory** - categorize each file as:
- `WITH_TESTS` - Glob found a matching test file
- `WITHOUT_TESTS` - Glob found no matching test file

**Skip to Step 6 (Output)**

---

## Step 5: Coverage Mode (--coverage flag)

**If MODE = "coverage":**

**Use Bash tool** to run Jest coverage (fresh run, ignore old coverage/ folder):

```bash
npm test -- --coverage --watchAll=false
```

Parse the Jest console output directly to extract:
- File paths
- % Statements, Branches, Functions, Lines

Categorize from output:
- `UNCOVERED` - files with 0% coverage
- `LOW_COVERAGE` - files with <50% line coverage
- `COVERED` - files with >50% coverage

---

## Step 6: Categorize by Type

Group `WITHOUT_TESTS` or `UNCOVERED` files by type:

| Pattern | Category |
|---------|----------|
| Path contains `components/` | Components |
| Path contains `hooks/` or filename `use*.ts` | Hooks |
| Path contains `utils/` or `helpers/` | Utils |
| Path contains `services/` or `api/` | Services |
| Other | Other |

---

## Step 7: Output Results

### Quick Mode Output

```
Untested Files Report
───────────────────────────────────────
Scanned: [SCAN_PATH]
Source files: [count of TESTABLE_FILES]
With test files: [count of WITH_TESTS]
Missing test files: [count of WITHOUT_TESTS]
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

- **Quick mode** checks if test files exist (fast, file-based)
- **Coverage mode** runs Jest for actual coverage data (slower, accurate)
- Coverage mode always runs fresh - ignores stale `coverage/` folder
- Use quick mode for daily checks, coverage mode for CI/reviews

---

## Quick Reference

```
/find-untested                      # Quick: check if test files exist
/find-untested src/components       # Quick: specific directory
/find-untested --coverage           # Accurate: run Jest coverage
```
