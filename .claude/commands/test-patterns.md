# Test Patterns Reference Command

Show testing patterns for: $ARGUMENTS

Available patterns: `mocking`, `async`, `hooks`, `events`, `queries`, `assertions`, `setup`, `errors`, or `all`

---

## Mocking Patterns

### Module Mocking
```typescript
// Mock entire module
jest.mock('./api');

// Mock with implementation
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'Test' })
}));

// Mock default export
jest.mock('./Component', () => ({
  __esModule: true,
  default: () => <div>Mocked</div>
}));
```

### Function Mocking
```typescript
const mockFn = jest.fn();
const mockFn = jest.fn().mockReturnValue('result');
const mockFn = jest.fn().mockResolvedValue({ data: 'test' });
const mockFn = jest.fn().mockRejectedValue(new Error('Failed'));

// Different returns per call
const mockFn = jest.fn()
  .mockReturnValueOnce('first')
  .mockReturnValueOnce('second')
  .mockReturnValue('default');
```

### Spies
```typescript
const spy = jest.spyOn(object, 'method');
jest.spyOn(console, 'error').mockImplementation(() => {});
```

### Timers
```typescript
beforeEach(() => jest.useFakeTimers());
afterEach(() => jest.useRealTimers());

jest.advanceTimersByTime(1000);
jest.runAllTimers();
```

---

## Async Patterns

### waitFor
```typescript
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});
```

### findBy (built-in waiting)
```typescript
const element = await screen.findByText('Result');
expect(element).toBeInTheDocument();
```

### waitForElementToBeRemoved
```typescript
await waitForElementToBeRemoved(() => screen.queryByText('Loading'));
```

### act wrapper
```typescript
await act(async () => {
  result.current.doAsyncAction();
});
```

---

## Hook Testing Patterns

### Basic Hook Test
```typescript
import { renderHook, act } from '@testing-library/react';

const { result } = renderHook(() => useMyHook());
expect(result.current.value).toBe(initial);

act(() => {
  result.current.setValue('new');
});
expect(result.current.value).toBe('new');
```

### Hook with Props
```typescript
const { result, rerender } = renderHook(
  ({ id }) => useUser(id),
  { initialProps: { id: 1 } }
);

rerender({ id: 2 });
```

### Hook with Provider
```typescript
const wrapper = ({ children }) => (
  <Provider store={store}>{children}</Provider>
);

const { result } = renderHook(() => useMyHook(), { wrapper });
```

---

## User Event Patterns

### Setup (always do this)
```typescript
const user = userEvent.setup();
```

### Common Interactions
```typescript
await user.click(button);
await user.type(input, 'text');
await user.clear(input);
await user.selectOptions(select, 'option');
await user.keyboard('{Enter}');
await user.tab();
await user.hover(element);
await user.unhover(element);
```

### Full Example
```typescript
it('should submit form', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<Form onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText('Email'), 'test@example.com');
  await user.type(screen.getByLabelText('Password'), 'password123');
  await user.click(screen.getByRole('button', { name: 'Submit' }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123'
  });
});
```

---

## Query Priority (Best → Worst)

```typescript
// 1. Accessible to everyone
screen.getByRole('button', { name: 'Submit' })
screen.getByRole('heading', { level: 1 })

// 2. Form labels
screen.getByLabelText('Email')

// 3. Placeholder (when no label)
screen.getByPlaceholderText('Enter email')

// 4. Text content
screen.getByText('Welcome')

// 5. Alt text (images)
screen.getByAltText('User avatar')

// 6. Test ID (last resort only!)
screen.getByTestId('submit-btn')
```

### Query Variants
```typescript
getBy...    // Throws if not found
queryBy...  // Returns null if not found
findBy...   // Async, waits for element
getAllBy... // Returns array
```

---

## Assertion Patterns

### DOM Assertions
```typescript
expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toHaveTextContent('text');
expect(element).toHaveValue('value');
expect(element).toHaveAttribute('href', '/path');
expect(element).toHaveClass('active');
expect(element).toBeDisabled();
expect(element).toBeChecked();
```

### Function Call Assertions
```typescript
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledTimes(2);
expect(fn).toHaveBeenCalledWith('arg1', 'arg2');
expect(fn).toHaveBeenLastCalledWith('arg');
```

### Async Assertions
```typescript
await expect(asyncFn()).resolves.toBe('result');
await expect(asyncFn()).rejects.toThrow('error');
```

### Negation
```typescript
expect(element).not.toBeInTheDocument();
expect(fn).not.toHaveBeenCalled();
```

---

## Setup & Teardown

```typescript
describe('Component', () => {
  // Once before all tests
  beforeAll(() => {
    server.listen();
  });

  // Once after all tests
  afterAll(() => {
    server.close();
  });

  // Before each test
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // After each test
  afterEach(() => {
    cleanup();
  });
});
```

---

## Error Handling Patterns

### Test Component Errors
```typescript
const originalError = console.error;
beforeAll(() => {
  console.error = jest.fn();
});
afterAll(() => {
  console.error = originalError;
});

it('should handle error', () => {
  render(
    <ErrorBoundary>
      <ComponentThatThrows />
    </ErrorBoundary>
  );
  expect(screen.getByText('Error occurred')).toBeInTheDocument();
});
```

### Test Async Errors
```typescript
it('should handle API error', async () => {
  mockApi.mockRejectedValue(new Error('Network error'));

  render(<Component />);

  await waitFor(() => {
    expect(screen.getByText('Error: Network error')).toBeInTheDocument();
  });
});
```

### Test Thrown Errors
```typescript
it('should throw for invalid input', () => {
  expect(() => validateInput(null)).toThrow('Input required');
});
```

---

## Debug Helpers

```typescript
screen.debug();                    // Print entire DOM
screen.debug(element);             // Print specific element
screen.logTestingPlaygroundURL();  // Get playground link
```
