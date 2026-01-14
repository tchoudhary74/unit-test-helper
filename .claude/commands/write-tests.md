---
description: Write comprehensive Jest tests for a source file
argument-hint: [source-file-path]
allowed-tools: Bash(npm test:*), Bash(npx jest:*)
---

# Write Tests Command

Write comprehensive Jest tests for a source file.

**Arguments:** `$ARGUMENTS`

---

## Step 1: Validate Input

```
If $ARGUMENTS is empty:
  → Error: "Please provide a source file path"
  → Example: "/write-tests src/components/Button.tsx"

If $ARGUMENTS contains .test. or .spec.:
  → Error: "This appears to be a test file. Use /fix-tests instead"
```

---

## Step 2: Find Source File

Use Glob to locate the file:
1. Exact path: `$ARGUMENTS`
2. In src/: `src/**/$ARGUMENTS`
3. Anywhere: `**/$ARGUMENTS`

If not found → Show error with similar file suggestions.

---

## Step 3: Read & Analyze Source File

Read the source file and determine type:

| Look For | Type | Template to Use |
|----------|------|-----------------|
| React import + JSX return | React Component | COMPONENT |
| Function name starts with `use` + calls hooks | React Hook | HOOK |
| axios/fetch import + async HTTP methods | API Service | API |
| Pure functions, helpers, formatters | Utility | UTILITY |

---

## Step 4: Detect Project Configuration

1. **Language:** Check for `tsconfig.json`
   - Found → TypeScript (use `.test.tsx`)
   - Not found → JavaScript (use `.test.jsx`)

2. **Team Conventions:** Read 1-2 existing test files to match:
   - Import style
   - describe/it vs test() pattern
   - Naming conventions
   - beforeEach/afterEach usage

---

## Step 5: Check for Existing Tests

Determine test file location:
```
Source: src/components/Button.tsx
Check:
  1. src/components/Button.test.tsx
  2. src/components/__tests__/Button.test.tsx
```

If exists → Ask: Overwrite | Append | Cancel

---

## Step 6: Generate Tests Using Template

### React Component Template

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  const defaultProps = {
    // Add required props here
  };

  describe('rendering', () => {
    it('should render without crashing', () => {
      render(<ComponentName {...defaultProps} />);

      expect(screen.getByRole('...')).toBeInTheDocument();
    });

    it('should display correct content', () => {
      render(<ComponentName {...defaultProps} />);

      expect(screen.getByText('...')).toBeInTheDocument();
    });
  });

  describe('interactions', () => {
    it('should handle click events', async () => {
      const user = userEvent.setup();
      const mockHandler = jest.fn();
      render(<ComponentName {...defaultProps} onClick={mockHandler} />);

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

---

### React Hook Template

```typescript
import { renderHook, act } from '@testing-library/react';
import { useHookName } from './useHookName';

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

  describe('with parameters', () => {
    it('should accept initial value', () => {
      const { result } = renderHook(() => useHookName({ initial: 'test' }));

      expect(result.current.value).toBe('test');
    });
  });
});
```

---

### Utility Function Template

```typescript
import { functionName } from './functionName';

describe('functionName', () => {
  describe('valid inputs', () => {
    it('should return expected result for valid input', () => {
      const result = functionName(validInput);

      expect(result).toBe(expectedOutput);
    });

    it('should handle multiple valid cases', () => {
      expect(functionName(input1)).toBe(output1);
      expect(functionName(input2)).toBe(output2);
    });
  });

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

  describe('error cases', () => {
    it('should throw for invalid input', () => {
      expect(() => functionName(invalidInput)).toThrow();
    });
  });
});
```

---

### API Service Template

```typescript
import { apiFunction } from './apiService';
import { httpClient } from './httpClient';

jest.mock('./httpClient');

const mockedHttpClient = httpClient as jest.Mocked<typeof httpClient>;

describe('apiFunction', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('successful requests', () => {
    it('should return data on success', async () => {
      const mockData = { id: 1, name: 'Test' };
      mockedHttpClient.get.mockResolvedValue({ data: mockData });

      const result = await apiFunction();

      expect(result).toEqual(mockData);
      expect(mockedHttpClient.get).toHaveBeenCalledWith('/endpoint');
    });
  });

  describe('request parameters', () => {
    it('should pass correct parameters', async () => {
      mockedHttpClient.post.mockResolvedValue({ data: {} });

      await apiFunction({ id: 123 });

      expect(mockedHttpClient.post).toHaveBeenCalledWith('/endpoint', { id: 123 });
    });
  });

  describe('error handling', () => {
    it('should handle network errors', async () => {
      mockedHttpClient.get.mockRejectedValue(new Error('Network error'));

      await expect(apiFunction()).rejects.toThrow('Network error');
    });

    it('should handle 404 errors', async () => {
      mockedHttpClient.get.mockRejectedValue({ response: { status: 404 } });

      await expect(apiFunction()).rejects.toMatchObject({
        response: { status: 404 }
      });
    });
  });
});
```

---

## Step 7: Write Test File

Write to: `[source-directory]/[name].test.[tsx|jsx]`

Or if team uses `__tests__/`: `[source-directory]/__tests__/[name].test.[tsx|jsx]`

---

## Step 8: Verify Tests Pass

Run the generated tests:

```bash
npm test -- --testPathPattern="[filename]" --watchAll=false
```

If tests fail:
- Missing mock → Add `jest.mock('./module')`
- Async error → Add `await` or use `waitFor`
- DOM query fail → Check element roles/text

---

## Output

```
Test File Created
───────────────────────────────────────
Source:   [source file path]
Test:     [test file path]
Type:     [Component|Hook|Utility|API]
Language: [TypeScript|JavaScript]

Tests Generated:
  • rendering (2 tests)
  • interactions (1 test)
  • edge cases (1 test)

Next Steps:
  1. Review generated tests
  2. Update placeholder values
  3. Run: /run-tests [test-file]
───────────────────────────────────────
```

---

## Quick Reference

```
/write-tests Button.tsx                # Component
/write-tests src/hooks/useAuth.ts      # Hook
/write-tests utils/format.js           # Utility
/write-tests services/api.ts           # API service
```
