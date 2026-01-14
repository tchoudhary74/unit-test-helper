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
If $ARGUMENTS contains "--check":
  MODE = "validate"  # Check only, no changes
  Remove "--check" from $ARGUMENTS
Else:
  MODE = "fix"

If $ARGUMENTS is empty:
  → Error: "Please provide a test file path"
  → Example: "/fix-tests src/components/Button.test.tsx"

If $ARGUMENTS does NOT contain .test. or .spec.:
  → Warning: "This doesn't look like a test file"
```

---

## Step 2: Find and Read Test File

Use Glob to find:
1. Exact path: `$ARGUMENTS`
2. In src/: `src/**/$ARGUMENTS`
3. Anywhere: `**/$ARGUMENTS`

Read file content for analysis.

---

## Step 3: Analyze Violations

Check test file against these rules:

| Rule | Check For | Severity |
|------|-----------|----------|
| Has describe() | `describe(` present | Required |
| Has it() or test() | `it(` or `test(` present | Required |
| Uses "should" naming | `it('should` pattern | Warning |
| Has assertions | `expect(` present | Required |
| No .only() | Must NOT have `.only(` | Required |
| No .skip() | Must NOT have `.skip(` | Required |

**Detect test type:**
- `render(` + `screen.` → React Component
- `renderHook(` → React Hook
- `jest.mock(` + http/api → API Service
- Otherwise → Utility Function

---

## Step 4: Apply Fixes (Skip if MODE = "validate")

### Fix: Rename it() to use "should"

```typescript
// Before
it('renders', () => { ... });
it('handles click', () => { ... });

// After
it('should render without crashing', () => { ... });
it('should handle click event', () => { ... });
```

### Fix: Add describe() grouping

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

### Fix: Add AAA spacing (Arrange-Act-Assert)

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

### Fix: Remove .only() and .skip()

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

Use Edit tool to apply fixes incrementally - one issue at a time.

---

## Step 6: Verify Tests Pass (Skip if MODE = "validate")

Run the fixed tests:

```bash
npm test -- --testPathPattern="[filename]" --watchAll=false
```

If tests fail after fixes:
- Review the changes
- Revert problematic fix
- Report which fix caused the issue

---

## Output

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
