# Write Tests Command

Write comprehensive Jest tests for: $ARGUMENTS

## Before Writing Any Tests

1. **Analyze existing test patterns** in this codebase:
   - Find 3-5 recent test files: `find . -name "*.test.ts" -o -name "*.test.tsx" | grep -v node_modules | head -5`
   - Read them to understand the team's conventions
   - Note: import order, describe/it structure, naming patterns, mocking approaches

2. **Check for team config** at `.jest-helper.json` in project root - if present, follow its rules

3. **Find the source file** being tested to understand what needs testing

## Test Writing Standards

### Structure
- Use `describe()` blocks to group related tests
- Use `it()` with "should + verb" naming: `it('should render with default props', ...)`
- Follow AAA pattern with visual spacing: Arrange → Act → Assert

### Required Coverage
- Happy path (normal usage)
- Edge cases: null, undefined, empty values
- Error states and error handling
- User interactions (for components)

### Import Order
```typescript
// 1. React/framework
import React from 'react';
// 2. Testing libraries
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
// 3. Components/modules being tested
import { ComponentName } from './ComponentName';
// 4. Utilities and helpers
// 5. Mocks (at top, after imports)
jest.mock('./api');
```

## Template Selection

**React Component** (has render, screen):
```typescript
describe('ComponentName', () => {
  const defaultProps = {};

  describe('rendering', () => {
    it('should render without crashing', () => {
      render(<ComponentName {...defaultProps} />);
      expect(screen.getByRole('...')).toBeInTheDocument();
    });
  });

  describe('interactions', () => {
    it('should handle click events', async () => {
      const user = userEvent.setup();
      const mockHandler = jest.fn();
      render(<ComponentName onClick={mockHandler} />);

      await user.click(screen.getByRole('button'));

      expect(mockHandler).toHaveBeenCalledTimes(1);
    });
  });

  describe('edge cases', () => {
    it('should handle empty props gracefully', () => {
      render(<ComponentName />);
      expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    });
  });
});
```

**React Hook** (has renderHook):
```typescript
describe('useHookName', () => {
  describe('initialization', () => {
    it('should return initial state', () => {
      const { result } = renderHook(() => useHookName());
      expect(result.current.value).toBe(initialValue);
    });
  });

  describe('actions', () => {
    it('should update state when action is called', () => {
      const { result } = renderHook(() => useHookName());

      act(() => {
        result.current.doAction();
      });

      expect(result.current.value).toBe(expectedValue);
    });
  });
});
```

**Utility Function**:
```typescript
describe('functionName', () => {
  describe('valid inputs', () => {
    it('should return expected result for valid input', () => {
      const result = functionName(validInput);
      expect(result).toBe(expectedOutput);
    });
  });

  describe('edge cases', () => {
    it('should handle null input', () => {
      expect(functionName(null)).toBe(defaultValue);
    });

    it('should handle undefined input', () => {
      expect(functionName(undefined)).toBe(defaultValue);
    });
  });

  describe('error cases', () => {
    it('should throw for invalid input', () => {
      expect(() => functionName(invalidInput)).toThrow();
    });
  });
});
```

**API Service** (has mocked HTTP):
```typescript
jest.mock('./httpClient');

describe('apiFunction', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('successful requests', () => {
    it('should return data on success', async () => {
      httpClient.get.mockResolvedValue({ data: 'test' });

      const result = await apiFunction();

      expect(result).toEqual({ data: 'test' });
      expect(httpClient.get).toHaveBeenCalledWith('/endpoint');
    });
  });

  describe('error handling', () => {
    it('should handle network errors', async () => {
      httpClient.get.mockRejectedValue(new Error('Network error'));

      await expect(apiFunction()).rejects.toThrow('Network error');
    });
  });
});
```

## After Writing

1. **Run the tests**: `npm test -- path/to/file.test.tsx --watchAll=false`
2. **Validate style** - ensure no `.only()` or `.skip()` left in code
3. **Check coverage** of edge cases

## File Naming
- Place test file next to source: `Button.tsx` → `Button.test.tsx`
- Or in `__tests__` folder: `__tests__/Button.test.tsx`
