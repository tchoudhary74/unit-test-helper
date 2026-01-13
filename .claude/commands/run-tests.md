---
description: Run Jest tests with automatic project detection
argument-hint: [file] [--coverage] [--watch]
allowed-tools: Bash(npm test:*), Bash(npx jest:*)
---

# Run Tests Command

Execute Jest tests with automatic project detection.

**Arguments:** `$ARGUMENTS`

---

## Step 1: Parse Arguments

Analyze `$ARGUMENTS` and extract components:

### Argument Types

| Pattern | Type | Example |
|---------|------|---------|
| Empty | Run all tests | `/run-tests` |
| `*.test.ts`, `*.test.tsx`, `*.test.js`, `*.test.jsx` | Test file | `Button.test.tsx` |
| `*.spec.ts`, `*.spec.tsx`, `*.spec.js`, `*.spec.jsx` | Spec file | `utils.spec.js` |
| `--coverage` | Coverage flag | `--coverage` |
| `--watch` | Watch mode flag | `--watch` |
| Other text | Test pattern | `"should render"` |

### Parsing Logic

```
ARGUMENTS = "$ARGUMENTS"

# Extract flags
HAS_COVERAGE = contains "--coverage"
HAS_WATCH = contains "--watch"

# Remove flags to get remaining args
REMAINING = remove "--coverage" and "--watch" from ARGUMENTS

# Determine type
If REMAINING is empty:
  TYPE = "all"
Else if REMAINING matches *.test.* or *.spec.*:
  TYPE = "file"
  FILE_PATH = REMAINING
Else:
  TYPE = "pattern"
  PATTERN = REMAINING
```

---

## Step 2: Find Project Root

Find `package.json` to determine project root.

**Action:** Use Glob tool to search for `package.json`:

```
Search order:
1. Current directory: ./package.json
2. Parent directories: ../package.json, ../../package.json
3. Or use: **/package.json (exclude node_modules)
```

If `package.json` not found:
- Display error: "No package.json found. Are you in a JavaScript/TypeScript project?"
- Stop execution

Store the directory containing `package.json` as `PROJECT_ROOT`.

---

## Step 3: Verify npm Project

**Action:** Use Glob tool to check for `package-lock.json` in PROJECT_ROOT.

If found: Confirms npm is the package manager
If not found: Proceed with npm (default)

**Note:** This command is optimized for npm. For yarn/pnpm projects, minor adjustments may be needed.

---

## Step 4: Detect TypeScript Project

Check for TypeScript configuration in `PROJECT_ROOT`.

**Action:** Use Glob tool to check for:
- `tsconfig.json`
- `tsconfig.test.json`
- `jest.config.ts`

If any found: `PROJECT_TYPE = "typescript"`
Else: `PROJECT_TYPE = "javascript"`

---

## Step 5: Read & Analyze package.json

**Action:** Use Read tool to read `PROJECT_ROOT/package.json`.

Extract:
```json
{
  "scripts": {
    "test": "<test_command>"  // Check if exists
  },
  "dependencies": { ... },
  "devDependencies": { ... }
}
```

### Determine Test Command

```
If scripts.test exists:
  USE_SCRIPT = true
  Analyze the script pattern (see below)

Else if "jest" in dependencies or devDependencies:
  USE_SCRIPT = false
  USE_DIRECT_JEST = true

Else:
  ERROR: "No test script found and Jest is not installed."
  SUGGESTION: "Add a test script to package.json or install Jest: npm install -D jest"
  Stop execution
```

### Analyze Test Script Pattern

**Important:** The test script format affects how we pass file arguments.

| Script Pattern | Example | `SCRIPT_TYPE` | File Passing Strategy |
|----------------|---------|---------------|----------------------|
| Simple jest | `"test": "jest"` | `simple` | Pass file directly after `--` |
| Jest with path | `"test": "jest src/"` | `path_based` | Use `--testPathPattern` |
| Jest with config | `"test": "jest --config=..."` | `simple` | Pass file directly after `--` |
| react-scripts | `"test": "react-scripts test"` | `cra` | Use `--testPathPattern` |
| vitest | `"test": "vitest"` | `vitest` | Pass file directly |
| Custom/other | `"test": "npm run lint && jest"` | `complex` | Use direct `npx jest` |

**Detection Logic:**
```
TEST_SCRIPT = scripts.test value

If TEST_SCRIPT contains "vitest":
  SCRIPT_TYPE = "vitest"

Else if TEST_SCRIPT contains "react-scripts test":
  SCRIPT_TYPE = "cra"

Else if TEST_SCRIPT matches "jest" followed by a path (e.g., "jest src/", "jest ./tests"):
  SCRIPT_TYPE = "path_based"

Else if TEST_SCRIPT is just "jest" or "jest --config..." (no directory path):
  SCRIPT_TYPE = "simple"

Else:
  SCRIPT_TYPE = "complex"
```

Store `SCRIPT_TYPE` for use in command construction.

---

## Step 6: Validate Test File (if TYPE = "file")

If a specific file was provided:

**Action:** Use Glob tool to verify the file exists.

If file not found:
- Search for similar files: `**/[filename]*`
- Display error: "Test file not found: [path]"
- If similar files found: "Did you mean: [suggestions]"
- Stop execution

---

## Step 7: Construct Command

### Base Command

| Scenario | Command |
|----------|---------|
| With test script | `npm test --` |
| Without script (Direct Jest) | `npx jest` |

### Add Flags

```
FLAGS = ""

# Watch mode handling
If HAS_WATCH:
  FLAGS += "--watch"
Else:
  FLAGS += "--watchAll=false"

# Always add verbose
FLAGS += "--verbose"

# Coverage if requested
If HAS_COVERAGE:
  FLAGS += "--coverage"
```

### Add Target (Based on SCRIPT_TYPE)

**This is critical for running specific files correctly.**

```
If TYPE = "all":
  TARGET = ""  # No target, run all tests

Else if TYPE = "file":
  # Choose strategy based on SCRIPT_TYPE

  If SCRIPT_TYPE = "simple":
    # Can pass file directly
    TARGET = FILE_PATH

  Else if SCRIPT_TYPE = "path_based" OR SCRIPT_TYPE = "cra":
    # Must use --testPathPattern to filter
    TARGET = "--testPathPattern=\"FILE_NAME\""
    # Extract just filename: Button.test.tsx from src/components/Button.test.tsx

  Else if SCRIPT_TYPE = "vitest":
    TARGET = FILE_PATH

  Else if SCRIPT_TYPE = "complex":
    # Bypass script entirely, use direct jest
    USE_SCRIPT = false
    USE_DIRECT_JEST = true
    TARGET = FILE_PATH

Else if TYPE = "pattern":
  TARGET = "-t \"PATTERN\""
```

### Final Command Construction

```
If USE_DIRECT_JEST:
  # Bypass npm script, call jest directly
  COMMAND = "npx jest " + TARGET + " " + FLAGS

Else:
  # Use npm test script
  COMMAND = "npm test -- " + TARGET + " " + FLAGS
```

### Examples by Script Type

```bash
# SCRIPT_TYPE = "simple" (test: "jest")
npm test -- src/components/Button.test.tsx --watchAll=false --verbose

# SCRIPT_TYPE = "path_based" (test: "jest src/")  ← Most common!
npm test -- --testPathPattern="Button.test.tsx" --watchAll=false --verbose

# SCRIPT_TYPE = "cra" (test: "react-scripts test")
npm test -- --testPathPattern="Button.test" --watchAll=false --verbose

# SCRIPT_TYPE = "complex" (test: "lint && jest") - bypass script
npx jest src/components/Button.test.tsx --watchAll=false --verbose

# Run all tests
npm test -- --watchAll=false --verbose

# Run by test name pattern
npm test -- -t "should render" --watchAll=false --verbose

# With coverage
npm test -- --testPathPattern="Button.test.tsx" --coverage --watchAll=false --verbose
```

### Why This Matters

```
Problem:
  package.json: "test": "jest src/"
  User runs: /run-tests Button.test.tsx

  Wrong: npm test -- Button.test.tsx
         → Jest gets: jest src/ Button.test.tsx (doesn't filter!)

  Correct: npm test -- --testPathPattern="Button.test.tsx"
           → Jest filters to only Button.test.tsx
```

---

## Step 8: Execute Tests

**Action:** Use Bash tool to run the constructed command.

Set working directory to `PROJECT_ROOT`.

```bash
cd PROJECT_ROOT && COMMAND
```

---

## Step 9: Format Output

Parse the Jest output and display a clean summary.

### Success Output

```
Running tests...
Project: [PROJECT_TYPE]
Command: [COMMAND]

───────────────────────────────────────
Test Results
───────────────────────────────────────
Suites:  X passed, X total
Tests:   X passed, X total
Time:    X.XXs

Status: PASSED
───────────────────────────────────────
```

### Failure Output

```
Running tests...
Project: [PROJECT_TYPE]
Command: [COMMAND]

───────────────────────────────────────
Test Results
───────────────────────────────────────
Suites:  X passed, X failed, X total
Tests:   X passed, X failed, X total
Time:    X.XXs

Status: FAILED
───────────────────────────────────────

Failed Tests:

1. [Describe Block] > [Test Name]
   File: [file:line]

   Expected: [expected]
   Received: [received]

2. [Describe Block] > [Test Name]
   File: [file:line]

   [Error message]
───────────────────────────────────────
```

---

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot find module` | Missing dependency | Run `npm install` |
| `SyntaxError: Unexpected token` | Missing TypeScript config | Ensure `ts-jest` is installed: `npm i -D ts-jest` |
| `No tests found` | Wrong path or pattern | Verify file exists or check pattern spelling |
| `Jest: command not found` | Jest not installed | Run `npm i -D jest` |
| `Test timeout` | Async issue | Check for missing `await` or unresolved promises |
| `Runs all tests instead of one` | Path-based script | Use `--testPathPattern` (see Step 7) |

### TypeScript-Specific Errors

If `PROJECT_TYPE = "typescript"` and tests fail:

| Error | Solution |
|-------|----------|
| `Cannot use import statement` | Add `transform` config for ts-jest |
| `Type errors in tests` | Check tsconfig.json includes test files |
| `Module not found (@/)` | Configure `moduleNameMapper` in jest.config |

---

## Quick Reference

```
/run-tests                           # Run all tests
/run-tests Button.test.tsx           # Run specific file
/run-tests "should render"           # Run tests matching pattern
/run-tests --coverage                # Run with coverage
/run-tests --watch                   # Run in watch mode
/run-tests Button.test.tsx --coverage  # Combine file + coverage
```
