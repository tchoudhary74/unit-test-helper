---
description: Fix and refactor tests to match team standards
argument-hint: [test-file] [--check]
allowed-tools: Bash(npm test:*), Bash(npx jest:*)
---

# Fix Tests Command

Fix and refactor tests to match team standards.

**Arguments:** `$ARGUMENTS`

---

## Step 1: Parse Arguments

```
ARGUMENTS = "$ARGUMENTS"

# Check for --check flag (validate only, no fixes)
If ARGUMENTS contains "--check":
  MODE = "validate"
  Remove "--check" from ARGUMENTS
Else:
  MODE = "fix"

# Validate remaining arguments
If ARGUMENTS is empty:
  ERROR: "Please provide a test file path"
  EXAMPLE: "/fix-tests src/components/Button.test.tsx"
  Stop execution

If ARGUMENTS does NOT contain .test. or .spec.:
  WARNING: "This doesn't look like a test file"
  Stop execution
```

---

## Step 2: Find and Read Test File

**Action:** Use Glob to find the test file, then Read to get its content.

```
Search patterns:
1. Exact path: $ARGUMENTS
2. In src/: src/**/$ARGUMENTS
3. Anywhere: **/$ARGUMENTS
```

If not found:
- Display error: "Test file not found: [path]"
- Stop execution

Store file path as `TEST_FILE_PATH` and content for analysis.

---

## Step 3: Analyze Violations

Check the test file against these rules:

| Rule | How to Check | Severity |
|------|--------------|----------|
| Has `describe()` | Look for `describe(` | Required |
| Has `it()` or `test()` | Look for `it(` or `test(` | Required |
| `it()` uses "should" | Check if `it('should` pattern | Warning |
| Has assertions | Look for `expect(` | Required |
| No `.only()` | Must NOT have `.only(` | Required |
| No `.skip()` | Must NOT have `.skip(` | Required |

**Detect test type:**
- `render(` + `screen.` → React Component
- `renderHook(` → React Hook
- `jest.mock(` + http/api/fetch → API Service
- Otherwise → Utility Function

---

## Step 4: Apply Fixes (Skip if MODE = "validate")

**If MODE = "validate":** Skip to Step 6 (Output Summary)

**If MODE = "fix":** Apply relevant fixes based on violations found:

### Fix: Rename `it()` to use "should"

```typescript
// Before
it('renders', () => { ... });
it('handles click', () => { ... });

// After
it('should render without crashing', () => { ... });
it('should handle click event', () => { ... });
```

### Fix: Add `describe()` grouping

```typescript
// Before
it('should render', () => { ... });
it('should click', () => { ... });

// After
describe('ComponentName', () => {
  describe('rendering', () => {
    it('should render without crashing', () => { ... });
  });

  describe('interactions', () => {
    it('should handle click event', () => { ... });
  });
});
```

### Fix: Add AAA spacing

```typescript
// Before (cramped)
it('should update', () => {
  const { result } = renderHook(() => useCounter());
  act(() => { result.current.increment(); });
  expect(result.current.count).toBe(1);
});

// After (clear sections)
it('should update count when increment called', () => {
  const { result } = renderHook(() => useCounter());

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

### Fix: Remove `.only()` and `.skip()`

```typescript
// Before
describe.only('Component', () => { ... });
it.skip('should work', () => { ... });

// After
describe('Component', () => { ... });
it('should work', () => { ... });
```

---

## Step 5: Write Updated File (Skip if MODE = "validate")

**If MODE = "validate":** Skip to Step 6

**If MODE = "fix":**
- Use Edit tool to apply the fixes to `TEST_FILE_PATH`
- Apply changes incrementally - fix one issue at a time to maintain stability

---

## Step 6: Verify Tests Pass (Skip if MODE = "validate")

**If MODE = "validate":** Skip test execution, just show validation results in Output Summary.

**If MODE = "fix":** Run the fixed tests to ensure nothing broke.

Check `package.json` scripts.test:
- If `"jest src/"` (path-based): Use `--testPathPattern`
- If `"jest"` (simple): Pass file directly

```bash
# Path-based script (most common)
npm test -- --testPathPattern="[filename]" --watchAll=false

# Simple script
npm test -- [file-path] --watchAll=false
```

If tests fail after fixes:
- Review the changes
- Revert problematic fix
- Report which fix caused the issue

---

## Output Summary

### If MODE = "fix"

```
Fixed: [filename]
───────────────────────────────────────
Changes Made:
  • Renamed X it() blocks to use "should"
  • Added describe() grouping
  • Removed N .only()/.skip() calls
  • Applied AAA spacing

Validation:
  ✓ Has describe() blocks
  ✓ Has it() or test()
  ✓ Uses "should" naming
  ✓ Has assertions
  ✓ No .only() or .skip()

Tests: PASSED
───────────────────────────────────────
```

### If MODE = "validate" (--check flag)

```
Validated: [filename]
───────────────────────────────────────
Results:
  ✓ Has describe() blocks
  ✓ Has it() or test()
  ✗ Missing "should" naming (3 violations)
  ✓ Has assertions
  ✗ Found .only() (line 23)

Status: 2 issues found
───────────────────────────────────────
Run without --check to auto-fix these issues.
```

---

## Quick Reference

```
/fix-tests Button.test.tsx              # Fix test file
/fix-tests Button.test.tsx --check      # Validate only (no changes)
/fix-tests src/hooks/useAuth.test.ts    # Fix with full path
```
