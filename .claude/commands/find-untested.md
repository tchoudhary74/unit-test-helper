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
ARGUMENTS = "$ARGUMENTS"

# Check for --coverage flag (run real Jest coverage)
If ARGUMENTS contains "--coverage":
  MODE = "coverage"
  Remove "--coverage" from ARGUMENTS
Else:
  MODE = "quick"

# Default path
If ARGUMENTS is empty:
  SCAN_PATH = "src/"
Else:
  SCAN_PATH = ARGUMENTS
```

---

## Step 2: Find Source Files

**Action:** Use Glob to find source files.

```
Patterns:
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

Exclude:
  - node_modules/
  - *.test.* and *.spec.* (test files)
  - __tests__/ directories
  - __mocks__/ directories
```

Store results as `SOURCE_FILES`.

---

## Step 3: Apply Exclusions

Skip files that typically don't need direct tests:

| Pattern | Reason |
|---------|--------|
| `index.ts` / `index.tsx` | Barrel exports (re-exports only) |
| `*.d.ts` | Type definitions |
| `*.types.ts` | Type-only files |
| `*.styles.ts` | Style definitions |
| `*.constants.ts` | Pure constants |
| `*.config.ts` | Configuration files |
| `vite.config.*` | Build config |
| `jest.config.*` | Test config |

Store filtered list as `TESTABLE_FILES`.

---

## Step 4: Check for Test Files (Quick Mode)

**If MODE = "quick":**

For each file in `TESTABLE_FILES`, check if a test file exists:

```
Source: src/components/Button.tsx

Check for (in order):
1. src/components/Button.test.tsx
2. src/components/Button.test.ts
3. src/components/Button.spec.tsx
4. src/components/Button.spec.ts
5. src/components/__tests__/Button.test.tsx
6. src/components/__tests__/Button.test.ts
```

**Action:** Use Glob to check each pattern.

Categorize results:
- `WITH_TESTS` - source files that have a test file
- `WITHOUT_TESTS` - source files missing a test file

**Skip to Step 6 (Output)**

---

## Step 5: Run Jest Coverage (Coverage Mode)

**If MODE = "coverage":**

**Action:** Run Jest with fresh coverage (don't use old coverage folder).

### Detect Script Type (see /run-tests for full logic)

| Script Pattern | Example | Command |
|----------------|---------|---------|
| Simple | `"jest"` | `npm test -- --coverage --watchAll=false` |
| Path-based | `"jest src/"` | `npm test -- --coverage --watchAll=false` |
| react-scripts | `"react-scripts test"` | `npm test -- --coverage --watchAll=false` |
| Complex | `"lint && jest"` | `npx jest --coverage --watchAll=false` |

```bash
# Run fresh coverage (don't read from old coverage/ folder)
npm test -- --coverage --watchAll=false

# Parse the console output directly
```

Extract from Jest output:
- File paths
- % Statements
- % Branches
- % Functions
- % Lines

Categorize:
- `COVERED` - files with >0% coverage
- `UNCOVERED` - files with 0% coverage
- `LOW_COVERAGE` - files with <50% line coverage

---

## Step 6: Output Results

### Quick Mode Output

```
Untested Files Report
───────────────────────────────────────
Scanned: src/
Source files: 45
With test files: 32
Missing test files: 13
───────────────────────────────────────

Missing Test Files:

Components (5):
  • src/components/Modal.tsx
  • src/components/Tooltip.tsx
  • src/components/Dropdown.tsx

Hooks (3):
  • src/hooks/useDebounce.ts
  • src/hooks/useLocalStorage.ts

Utils (2):
  • src/utils/validators.ts
  • src/utils/formatters.ts

Services (3):
  • src/services/analytics.ts
  • src/services/storage.ts
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
  Statements: 72.5%
  Branches: 65.3%
  Functions: 80.1%
  Lines: 71.8%
───────────────────────────────────────

Uncovered Files (0% coverage):
  • src/components/Modal.tsx
  • src/hooks/useDebounce.ts
  • src/utils/validators.ts

Low Coverage (<50% lines):
  • src/components/Form.tsx (32%)
  • src/services/api.ts (45%)
───────────────────────────────────────

To write tests: /write-tests [file]
```

---

## File Categorization

Group files by type based on path/name:

| Pattern | Category |
|---------|----------|
| `components/` or `.tsx` with JSX | Components |
| `hooks/` or `use*.ts` | Hooks |
| `utils/` or `helpers/` | Utils |
| `services/` or `api/` | Services |
| Other | Other |

---

## Quick Reference

```
/find-untested                      # Quick: check if test files exist
/find-untested src/components       # Quick: specific directory
/find-untested --coverage           # Accurate: run Jest coverage
```

---

## Notes

- **Quick mode** is fast but only checks if test files exist (not quality)
- **Coverage mode** runs all tests (slower but accurate)
- Coverage mode always runs fresh - ignores old `coverage/` folder
- Use quick mode for daily checks, coverage mode for CI/reviews
