# Analyze Test Patterns Command

Analyze testing patterns and conventions in: $ARGUMENTS

If no path specified, analyze the entire project.

## Analysis Process

### Step 1: Find Test Files
```bash
find . -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" -o -name "*.spec.tsx" | grep -v node_modules
```

### Step 2: Sample Recent Tests
Get the 5 most recently modified test files (represent current standards):
```bash
ls -t $(find . -name "*.test.tsx" -o -name "*.test.ts" | grep -v node_modules) 2>/dev/null | head -5
```

### Step 3: Extract Patterns

For each sampled file, identify:

**Structure Patterns**
- [ ] Uses `describe()` blocks?
- [ ] Uses `it()` or `test()`?
- [ ] Uses `beforeEach`/`afterEach`?
- [ ] Has nested describe blocks?

**Naming Patterns**
- [ ] `it()` starts with "should"?
- [ ] `describe()` uses component/function name?
- [ ] Consistent capitalization?

**Import Patterns**
- [ ] Import order (React → testing-lib → components → utils)
- [ ] Testing library used (@testing-library/react?)
- [ ] User event library (userEvent vs fireEvent)

**Mocking Patterns**
- [ ] `jest.mock()` for modules
- [ ] `jest.fn()` for functions
- [ ] `jest.spyOn()` for methods
- [ ] `mockResolvedValue`/`mockRejectedValue` for async

**Assertion Patterns**
- [ ] DOM: `toBeInTheDocument()`, `toHaveTextContent()`
- [ ] Calls: `toHaveBeenCalled()`, `toHaveBeenCalledWith()`
- [ ] Values: `toBe()`, `toEqual()`, `toMatchObject()`
- [ ] Async: `resolves`, `rejects`

**Code Organization**
- [ ] AAA pattern with spacing?
- [ ] Comments for Arrange/Act/Assert?
- [ ] Default props pattern?
- [ ] Test utilities/helpers?

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║  TEST PATTERN ANALYSIS                                          ║
╠════════════════════════════════════════════════════════════════╣
║  Files Analyzed: N                                              ║
║  Path: [analyzed path]                                          ║
╚════════════════════════════════════════════════════════════════╝

┌─ Files Sampled ────────────────────────────────────────────────┐
│ • src/components/Button.test.tsx                               │
│ • src/hooks/useAuth.test.ts                                    │
│ • src/utils/format.test.ts                                     │
└────────────────────────────────────────────────────────────────┘

┌─ Structure ────────────────────────────────────────────────────┐
│ Pattern        : describe + it                                 │
│ beforeEach     : ✓ Used                                        │
│ afterEach      : ✗ Not used                                    │
│ Nested describe: ✓ Used (rendering, interactions, edge cases) │
└────────────────────────────────────────────────────────────────┘

┌─ Naming Conventions ───────────────────────────────────────────┐
│ it() naming    : "should + verb" (e.g., "should render...")   │
│ describe()     : Component/function name                       │
│ Examples:                                                      │
│   • describe('Button', ...)                                    │
│   • it('should render with default props', ...)                │
│   • it('should call onClick when clicked', ...)                │
└────────────────────────────────────────────────────────────────┘

┌─ Libraries & Imports ──────────────────────────────────────────┐
│ Testing Library: @testing-library/react                        │
│ User Events    : userEvent (not fireEvent)                     │
│ Utilities      : render, screen, waitFor, act                  │
│ Import Order   : react → testing-lib → components → mocks      │
└────────────────────────────────────────────────────────────────┘

┌─ Mocking Patterns ─────────────────────────────────────────────┐
│ • jest.mock() for module mocking                               │
│ • jest.fn() for function mocks                                 │
│ • mockResolvedValue() for async success                        │
│ • mockRejectedValue() for async errors                         │
└────────────────────────────────────────────────────────────────┘

┌─ Assertion Style ──────────────────────────────────────────────┐
│ DOM      : toBeInTheDocument(), toHaveTextContent()            │
│ Calls    : toHaveBeenCalledWith(), toHaveBeenCalledTimes()     │
│ Values   : toBe(), toEqual()                                   │
└────────────────────────────────────────────────────────────────┘

## Recommendations

Follow these patterns exactly when writing new tests in this codebase.
```

## Also Check For

- `.jest-helper.json` config file in project root
- `jest.config.js` or `jest.config.ts` for Jest configuration
- `setupTests.ts` for global test setup
- Custom test utilities in `src/test-utils/` or similar
