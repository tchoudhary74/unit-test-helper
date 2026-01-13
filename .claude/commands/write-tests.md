---
description: Write comprehensive Jest tests for a source file
argument-hint: [source-file-path]
allowed-tools: Bash(npm test:*), Bash(npx jest:*)
---

# Write Tests Command

Write comprehensive Jest tests for a source file.

**Arguments:** `$ARGUMENTS`

---

## Step 1: Parse Arguments

Analyze `$ARGUMENTS` to extract the source file path.

### Expected Input

| Input | Example |
|-------|---------|
| File path | `src/components/Button.tsx` |
| File name only | `Button.tsx` |
| Relative path | `./utils/format.ts` |

### Validation

```
If $ARGUMENTS is empty:
  ERROR: "Please provide a source file path"
  EXAMPLE: "/write-tests src/components/Button.tsx"
  Stop execution

If $ARGUMENTS contains test/spec in filename:
  WARNING: "This appears to be a test file, not a source file"
  SUGGESTION: "Did you mean to use /fix-tests instead?"
  Stop execution
```

---

## Step 2: Find Source File

**Action:** Use Glob tool to locate the source file.

```
Search patterns (in order):
1. Exact path: $ARGUMENTS
2. In src/: src/**/$ARGUMENTS
3. Anywhere: **/$ARGUMENTS
```

If not found:
- Display error: "Source file not found: [path]"
- Search for similar: `**/*[partial-name]*`
- If similar found: "Did you mean: [suggestions]"
- Stop execution

Store result as `SOURCE_FILE_PATH`.

---

## Step 3: Read Source File

**Action:** Use Read tool to read `SOURCE_FILE_PATH`.

Store the content for analysis in Step 6.

---

## Step 4: Check Existing Tests

Determine the expected test file location:

```
SOURCE: src/components/Button.tsx
TEST OPTIONS:
  1. src/components/Button.test.tsx (same directory)
  2. src/components/__tests__/Button.test.tsx (__tests__ folder)
  3. src/components/Button.spec.tsx (.spec variant)
```

**Action:** Use Glob tool to check if test file already exists.

If test file exists:
- Display: "Test file already exists: [path]"
- Ask: "Overwrite existing tests or add to them?"
- Options: Overwrite | Append | Cancel

---

## Step 5: Detect Project Configuration

### Language Detection

**Action:** Use Glob to check for TypeScript config:

| File Found | Language |
|------------|----------|
| `tsconfig.json` | TypeScript |
| `jsconfig.json` | JavaScript |
| Neither | Check source file extension |

```
.ts, .tsx → TypeScript (use .test.tsx)
.js, .jsx → JavaScript (use .test.jsx)
```

Store as `PROJECT_LANG` and `TEST_EXTENSION`.

### Test Convention Detection

**Action:** Use Glob to find 1-2 existing test files:
```
Pattern: **/*.test.{ts,tsx,js,jsx}
Exclude: node_modules
Limit: 2 most recent
```

If found, use Read tool to extract:
- Import style (ES6 vs require)
- Describe/it vs test() style
- beforeEach/afterEach usage
- Naming conventions

Store as `TEAM_CONVENTIONS`.

---

## Step 6: Analyze Source File & Select Template

Analyze the source file content to determine the type:

### Detection Logic

```
SOURCE FILE ANALYSIS:

1. React Component?
   ├── Has: import React OR import { ... } from 'react'
   ├── Has: JSX syntax (return <...> or return (...<))
   ├── Has: export default/named function or const
   └── Result: Use REACT_COMPONENT_TEMPLATE

2. React Hook?
   ├── Has: function name starts with "use" (useAuth, useState custom)
   ├── Has: calls useState, useEffect, useCallback, etc.
   ├── Has: returns object or array
   └── Result: Use REACT_HOOK_TEMPLATE

3. API Service?
   ├── Has: import axios OR import fetch OR http client
   ├── Has: async/await with HTTP methods (get, post, put, delete)
   ├── Has: API endpoints or URLs
   └── Result: Use API_SERVICE_TEMPLATE

4. Utility Function?
   ├── Default: pure functions, helpers, formatters
   └── Result: Use UTILITY_FUNCTION_TEMPLATE
```

Store selected template as `TEMPLATE_TYPE`.

---

## Step 7: Generate Tests

### Import Order (apply to all templates)

```typescript
// 1. React/framework (if applicable)
import React from 'react';

// 2. Testing libraries
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
// OR for hooks:
import { renderHook, act } from '@testing-library/react';

// 3. Component/module being tested
import { ComponentName } from './ComponentName';

// 4. Mocks (after imports)
jest.mock('./api');
```

**JavaScript Note:** For JS projects, remove type annotations and use `.js`/`.jsx` extensions.

---

### Template: React Component

**Use when:** Source has React import + JSX return

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

### Template: React Hook

**Use when:** Function name starts with `use`, returns state/methods

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

### Template: Utility Function

**Use when:** Pure functions, formatters, helpers, validators

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

### Template: API Service

**Use when:** Contains axios/fetch, async HTTP calls

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

## Step 8: Write Test File

Determine test file path:

```
SOURCE: src/components/Button.tsx

TEST PATH (based on team convention or default):
  Default: src/components/Button.test.tsx
  Or: src/components/__tests__/Button.test.tsx
```

**Action:** Use Write tool to create the test file.

---

## Step 9: Verify Tests (Optional)

**Action:** Run the tests to ensure they pass.

### Analyze Test Script (from package.json)

Check `scripts.test` to determine how to run a specific file:

| Script Pattern | Example | Command to Use |
|----------------|---------|----------------|
| Simple jest | `"jest"` | `npm test -- [file-path]` |
| Jest with path | `"jest src/"` | `npm test -- --testPathPattern="[filename]"` |
| react-scripts | `"react-scripts test"` | `npm test -- --testPathPattern="[filename]"` |

### Run Verification

```bash
# If script is simple ("jest" or "jest --config=...")
npm test -- src/components/Button.test.tsx --watchAll=false

# If script has path ("jest src/") - use testPathPattern
npm test -- --testPathPattern="Button.test.tsx" --watchAll=false

# If script is complex - bypass and use npx
npx jest src/components/Button.test.tsx --watchAll=false
```

### Handle Results

If tests pass:
- Display success message
- Show test count

If tests fail:
- Show failure details
- Common fixes:
  - Missing mock: Add `jest.mock('./module')`
  - Async error: Add `await` or use `waitFor`
  - DOM query fail: Check element roles/text

---

## Output Summary

```
Test File Created
─────────────────────────────────────
Source:    src/components/Button.tsx
Test:      src/components/Button.test.tsx
Type:      React Component
Language:  TypeScript

Tests Generated:
  • rendering (2 tests)
  • interactions (1 test)
  • edge cases (1 test)

Next Steps:
  1. Review generated tests
  2. Update placeholder values (defaultProps, expectedValue, etc.)
  3. Run: /run-tests Button.test.tsx
─────────────────────────────────────
```

---

## Quick Reference

```
/write-tests Button.tsx                    # Write tests for component
/write-tests src/hooks/useAuth.ts          # Write tests for hook
/write-tests utils/format.js               # Write tests for utility
/write-tests services/api.ts               # Write tests for API service
```
