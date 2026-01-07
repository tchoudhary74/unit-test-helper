# Run Tests Command

Run Jest tests for: $ARGUMENTS

## Interpret Arguments

| Input | Command |
|-------|---------|
| (empty) | Run all tests |
| `path/to/file.test.tsx` | Run specific file |
| `ComponentName` | Run tests matching name pattern |
| `--coverage` | Run with coverage report |
| `path --coverage` | Run file with coverage |

## Commands

### Run All Tests
```bash
npm test -- --watchAll=false --verbose
```

### Run Specific File
```bash
npm test -- $ARGUMENTS --watchAll=false --verbose
```

### Run Tests Matching Pattern
```bash
npm test -- -t "$ARGUMENTS" --watchAll=false --verbose
```

### Run with Coverage
```bash
npm test -- --coverage --watchAll=false --verbose
```

### Run Specific File with Coverage
```bash
npm test -- $ARGUMENTS --coverage --watchAll=false --verbose
```

## Output Interpretation

### Success Output
```
✅ All tests passed!

Test Suites: X passed, X total
Tests:       X passed, X total
Snapshots:   X passed, X total
Time:        X.XXs
```

### Failure Output
```
❌ Some tests failed!

FAIL src/components/Button.test.tsx
  ● ComponentName › should render

    Expected: "Hello"
    Received: "World"

      12 |     render(<Button />);
      13 |
    > 14 |     expect(screen.getByText('Hello')).toBeInTheDocument();
         |                                       ^
```

## Common Issues

### Test Timeout
If tests hang, check for:
- Missing `await` on async operations
- Unresolved promises
- Missing mock implementations

### Module Not Found
If imports fail:
- Check `moduleNameMapper` in jest.config
- Verify `@/` path aliases are configured
- Ensure dependencies are installed

### Act Warnings
If you see "not wrapped in act(...)":
- Wrap state updates: `await act(async () => { ... })`
- Use `waitFor` for async assertions
- Use `userEvent.setup()` before interactions

## Debugging

### Run Single Test
```bash
npm test -- -t "should render" --watchAll=false
```

### Run with Debug Output
```bash
DEBUG_PRINT_LIMIT=100000 npm test -- $ARGUMENTS --watchAll=false
```

### Update Snapshots
```bash
npm test -- -u --watchAll=false
```
