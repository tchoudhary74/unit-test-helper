---
description: Discover testing patterns and conventions in codebase
argument-hint: [path]
---

# Analyze Test Patterns Command

Discover testing patterns and conventions used in this codebase.

**Arguments:** `$ARGUMENTS` (optional path, defaults to entire project)

---

## Step 1: Find Test Files

**Action:** Use Glob to find test files in the project.

```
Pattern: **/*.test.{ts,tsx,js,jsx}
Also:    **/*.spec.{ts,tsx,js,jsx}
Exclude: node_modules
```

If no test files found:
- Display: "No test files found in this project"
- Stop execution

Store count as `TOTAL_TEST_FILES`.

---

## Step 2: Sample Recent Tests

Select 2-3 test files for analysis (recent files represent current standards).

**Action:** Use Glob results sorted by modification time, take first 3.

If `$ARGUMENTS` specifies a path, analyze files in that path only.

---

## Step 3: Read and Analyze Patterns

**Action:** Use Read tool to examine each sampled file.

Extract these patterns:

### Structure
| Pattern | Look For |
|---------|----------|
| Test blocks | `describe(` vs `test(` only |
| Assertions | `it(` vs `test(` |
| Setup/teardown | `beforeEach`, `afterEach`, `beforeAll` |
| Nesting | Nested `describe()` blocks |

### Naming
| Pattern | Look For |
|---------|----------|
| Test naming | `it('should...` vs `it('...` |
| Describe naming | Component name vs description |

### Imports
| Pattern | Look For |
|---------|----------|
| Testing library | `@testing-library/react` vs `enzyme` |
| User events | `userEvent` vs `fireEvent` |
| Import order | React → testing-lib → component → mocks |

### Mocking
| Pattern | Look For |
|---------|----------|
| Module mocks | `jest.mock()` |
| Function mocks | `jest.fn()` |
| Spy | `jest.spyOn()` |
| Async mocks | `mockResolvedValue`, `mockRejectedValue` |

---

## Step 4: Check Configuration Files

**Action:** Use Glob to check for these files:

| File | Purpose |
|------|---------|
| `jest.config.js` or `jest.config.ts` | Jest configuration |
| `setupTests.ts` or `setupTests.js` | Global test setup |
| `.jest-helper.json` | Team-specific rules |
| `src/test-utils/` | Custom test utilities |

---

## Output Summary

```
Test Patterns Analysis
───────────────────────────────────────
Files Found: [N] test files
Sampled: [2-3 files]

Structure:
  • Uses: describe() + it()
  • Setup: beforeEach (cleanup)
  • Nesting: Yes (rendering, interactions, edge cases)

Naming:
  • it() style: "should + verb"
  • describe(): Component/function name

Libraries:
  • Testing: @testing-library/react
  • Events: userEvent
  • Imports: react → testing-lib → component

Mocking:
  • jest.mock() for modules
  • jest.fn() for callbacks
  • mockResolvedValue for async

Config:
  • jest.config.ts: Found
  • setupTests.ts: Found
───────────────────────────────────────

Use these patterns when writing new tests.
```

---

## Quick Reference

```
/analyze-tests                    # Analyze entire project
/analyze-tests src/components     # Analyze specific directory
```
