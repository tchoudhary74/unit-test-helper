---
description: Run Jest tests with automatic project detection
argument-hint: [file] [--coverage] [--watch]
allowed-tools: Bash(npm test:*), Bash(npx jest:*)
---

# Run Tests Command

**Arguments:** `$ARGUMENTS`

## Step 1: Parse Arguments

```
Extract from $ARGUMENTS:
- HAS_COVERAGE = contains "--coverage"
- HAS_WATCH = contains "--watch"
- REMAINING = args without flags

Type detection:
- Empty → TYPE = "all"
- Matches *.test.* or *.spec.* → TYPE = "file"
- Other text → TYPE = "pattern"
```

## Step 2: Project Detection

Use Glob/Read to find:
1. `package.json` → Extract `scripts.test` and dependencies
2. `tsconfig.json` → IS_TYPESCRIPT = true/false

If no test script and jest not in dependencies → Error and stop.

## Step 3: Script Type & Command Strategy

| scripts.test value | Type | How to run single file |
|--------------------|------|------------------------|
| `"jest"` | simple | `npm test -- [file]` |
| `"jest --config=..."` | simple | `npm test -- [file]` |
| `"jest src/"` | path_based | `npm test -- --testPathPattern="[filename]"` |
| `"react-scripts test"` | cra | `npm test -- --testPathPattern="[filename]"` |
| `"vitest"` | vitest | `npm test -- [file]` |
| Contains `&&` or `||` | complex | `npx jest [file]` directly |

**Critical:** Path-based scripts (`jest src/`) ignore file arguments and run ALL tests. Must use `--testPathPattern` to filter.

## Step 4: Build Command

```
FLAGS = HAS_WATCH ? "--watch" : "--watchAll=false"
FLAGS += " --verbose"
If HAS_COVERAGE: FLAGS += " --coverage"

If TYPE = "file" and SCRIPT_TYPE in [path_based, cra]:
  TARGET = --testPathPattern="[filename only]"
Else if TYPE = "pattern":
  TARGET = -t "[pattern]"
Else:
  TARGET = [file or empty]

COMMAND = SCRIPT_TYPE == "complex"
  ? "npx jest TARGET FLAGS"
  : "npm test -- TARGET FLAGS"
```

## Step 5: Execute & Format Output

Run with Bash. Format results:

```
Test Results
───────────────────────────────────────
Suites:  X passed, X failed, X total
Tests:   X passed, X failed, X total
Time:    X.XXs
Status:  PASSED | FAILED

[If FAILED, list each failed test with error message]
───────────────────────────────────────
```

## Quick Reference

```
/run-tests                    # All tests
/run-tests Button.test.tsx    # Single file
/run-tests "should render"    # By pattern
/run-tests --coverage         # With coverage
/run-tests --watch            # Watch mode
```
