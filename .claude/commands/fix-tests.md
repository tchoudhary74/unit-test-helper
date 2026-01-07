# Fix Tests Command

Fix and refactor tests to match team standards for: $ARGUMENTS

## Analysis Steps

1. **Read the test file** specified in arguments
2. **Identify violations** against these rules:

| Rule | Check | Severity |
|------|-------|----------|
| Has `describe()` | Must have `describe\s*\(` | ❌ Required |
| Has `it()` or `test()` | Must have `(it\|test)\s*\(` | ❌ Required |
| `it()` uses "should" | Should match `it\s*\(\s*['"]should` | ⚠️ Warning |
| Has assertions | Must have `expect\s*\(` | ❌ Required |
| No `.only()`/`.skip()` | Must NOT have `\.(only\|skip)\s*\(` | ❌ Required |
| Tests edge cases | Should have null/undefined/empty/error tests | ⚠️ Warning |

3. **Detect test type** from content:
   - `render(` + `screen.` → React component
   - `renderHook(` → React hook
   - `jest.mock(` + api/fetch/http → API service
   - Otherwise → Utility function

## Common Fixes

### Fix 1: Rename `it()` to use "should"
```typescript
// ❌ Before
it('renders', () => { ... });
it('handles click', () => { ... });

// ✅ After  
it('should render without crashing', () => { ... });
it('should call handler when clicked', () => { ... });
```

### Fix 2: Add `describe()` grouping
```typescript
// ❌ Before
it('should render', () => { ... });
it('should click', () => { ... });
it('should handle null', () => { ... });

// ✅ After
describe('ComponentName', () => {
  describe('rendering', () => {
    it('should render without crashing', () => { ... });
  });

  describe('interactions', () => {
    it('should call handler when clicked', () => { ... });
  });

  describe('edge cases', () => {
    it('should handle null gracefully', () => { ... });
  });
});
```

### Fix 3: Add AAA spacing
```typescript
// ❌ Before (cramped)
it('should update', () => {
  const { result } = renderHook(() => useCounter());
  act(() => { result.current.increment(); });
  expect(result.current.count).toBe(1);
});

// ✅ After (clear sections)
it('should update count when increment called', () => {
  const { result } = renderHook(() => useCounter());

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

### Fix 4: Remove `.only()` and `.skip()`
```typescript
// ❌ Before
describe.only('Component', () => { ... });
it.skip('should work', () => { ... });

// ✅ After
describe('Component', () => { ... });
it('should work', () => { ... });
```

### Fix 5: Add missing edge case tests
```typescript
// Add these if missing:
describe('edge cases', () => {
  it('should handle null input', () => {
    expect(functionName(null)).toBe(defaultValue);
  });

  it('should handle undefined input', () => {
    expect(functionName(undefined)).toBe(defaultValue);
  });

  it('should handle empty string', () => {
    expect(functionName('')).toBe(defaultValue);
  });
});
```

## Output Format

After fixing, report:
```
✅ Fixed: [filename]

Changes made:
• Renamed X it() blocks to use "should" prefix
• Added describe() grouping for rendering/interactions/edge cases  
• Removed N .only() calls
• Added M edge case tests
• Applied AAA spacing

Validation:
✅ PASS  Has describe() blocks
✅ PASS  Has it() or test()
✅ PASS  it() uses "should" naming
✅ PASS  Has assertions
✅ PASS  No .only() or .skip()
```

## After Fixing

Run the tests to ensure nothing broke:
```bash
npm test -- [test-file-path] --watchAll=false --verbose
```
