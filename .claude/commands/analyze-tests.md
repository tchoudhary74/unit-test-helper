---
description: Discover testing patterns and conventions in codebase
argument-hint: [path]
---

# Analyze Test Patterns Command

Discover testing patterns and conventions used in this codebase.

**Arguments:** `$ARGUMENTS` (optional path, defaults to entire project)

---

## Step 1: Find Test Files

Use Glob to find test files:

```
Pattern: **/*.test.{ts,tsx,js,jsx}
Also:    **/*.spec.{ts,tsx,js,jsx}
Exclude: node_modules
```

If no test files found → Display "No test files found" and stop.

Store count as `TOTAL_TEST_FILES`.

---

## Step 2: Sample Recent Tests

Select 2-3 test files for analysis (recent files represent current standards).

Use Glob results sorted by modification time, take first 3.

If `$ARGUMENTS` specifies a path, analyze files in that path only.

---

## Step 3: Read and Analyze Patterns

Read each sampled file and extract:

### Structure Patterns
| Pattern | Look For |
|---------|----------|
| Test blocks | `describe(` vs `test(` only |
| Assertions | `it(` vs `test(` |
| Setup/teardown | `beforeEach`, `afterEach`, `beforeAll` |
| Nesting | Nested `describe()` blocks |

### Naming Patterns
| Pattern | Look For |
|---------|----------|
| Test naming | `it('should...` vs `it('...` |
| Describe naming | Component name vs description |

### Import Patterns
| Pattern | Look For |
|---------|----------|
| Testing library | `@testing-library/react` vs `enzyme` |
| User events | `userEvent` vs `fireEvent` |
| Import order | React → testing-lib → component → mocks |

### Mocking Patterns
| Pattern | Look For |
|---------|----------|
| Module mocks | `jest.mock()` |
| Function mocks | `jest.fn()` |
| Spy | `jest.spyOn()` |
| Async mocks | `mockResolvedValue`, `mockRejectedValue` |

---

## Step 4: Check Configuration Files

Use Glob to check for:

| File | Purpose |
|------|---------|
| `jest.config.js` or `jest.config.ts` | Jest configuration |
| `setupTests.ts` or `setupTests.js` | Global test setup |
| `src/test-utils/` | Custom test utilities |

---

## Output

```
Test Patterns Analysis
───────────────────────────────────────
Files Found: [N] test files
Sampled: [list of 2-3 files analyzed]

Structure:
  • Uses: describe() + it()
  • Setup: beforeEach (cleanup)
  • Nesting: Yes/No

Naming:
  • it() style: "should + verb" | other
  • describe(): Component/function name

Libraries:
  • Testing: @testing-library/react | enzyme | other
  • Events: userEvent | fireEvent
  • Imports: [detected order]

Mocking:
  • jest.mock() for modules: Yes/No
  • jest.fn() for callbacks: Yes/No
  • mockResolvedValue for async: Yes/No

Config Files:
  • jest.config: Found/Not found
  • setupTests: Found/Not found
  • test-utils/: Found/Not found
───────────────────────────────────────

Use these patterns when writing new tests.
```

---

## Quick Reference

```
/analyze-tests                    # Analyze entire project
/analyze-tests src/components     # Analyze specific directory
```
