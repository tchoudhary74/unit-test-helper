# Validate Test Style Command

Validate test file(s) against team standards: $ARGUMENTS

## Validation Rules

Apply these checks to each test file:

### Required Rules (Must Pass)

| ID | Rule | Pattern | Check |
|----|------|---------|-------|
| R1 | Has describe() | `describe\s*\(` | Must match |
| R2 | Has it() or test() | `(it\|test)\s*\(` | Must match |
| R3 | Has assertions | `expect\s*\(` | Must match |
| R4 | No .only() | `\.only\s*\(` | Must NOT match |
| R5 | No .skip() | `\.skip\s*\(` | Must NOT match |

### Warning Rules (Should Pass)

| ID | Rule | Pattern | Check |
|----|------|---------|-------|
| W1 | it() uses "should" | `it\s*\(\s*['"]should` | Should match |
| W2 | Tests edge cases | `(null\|undefined\|empty\|error)` | Should match |
| W3 | Uses Testing Library | `@testing-library` | Should match |
| W4 | Has beforeEach cleanup | `beforeEach` | Should match |

## Validation Process

1. **Read the test file(s)** specified in arguments
2. **Apply each rule** using regex pattern matching
3. **Collect results** for all rules
4. **Report findings** with pass/fail/warning status

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║  TEST STYLE VALIDATION                                          ║
╠════════════════════════════════════════════════════════════════╣
║  File: src/components/Button.test.tsx                          ║
╚════════════════════════════════════════════════════════════════╝

┌─ Required Rules ───────────────────────────────────────────────┐
│ ✅ PASS   R1: Has describe() blocks                            │
│ ✅ PASS   R2: Has it() or test() blocks                        │
│ ✅ PASS   R3: Has expect() assertions                          │
│ ✅ PASS   R4: No .only() calls                                 │
│ ✅ PASS   R5: No .skip() calls                                 │
└────────────────────────────────────────────────────────────────┘

┌─ Warning Rules ────────────────────────────────────────────────┐
│ ✅ PASS   W1: it() uses "should" naming                        │
│ ⚠️  WARN   W2: Should test edge cases (null/undefined/empty)   │
│ ✅ PASS   W3: Uses Testing Library                             │
│ ✅ PASS   W4: Has beforeEach for cleanup                       │
└────────────────────────────────────────────────────────────────┘

┌─ Summary ──────────────────────────────────────────────────────┐
│ Required: 5/5 passed                                           │
│ Warnings: 3/4 passed, 1 warning                                │
│                                                                │
│ ✅ File meets required standards                               │
│ ⚠️  Consider adding edge case tests                            │
└────────────────────────────────────────────────────────────────┘
```

## Batch Validation

If `$ARGUMENTS` is a directory or glob pattern, validate all matching files:

```
Validating 12 test files...

✅ src/components/Button.test.tsx         (5/5 required, 4/4 warnings)
✅ src/components/Input.test.tsx          (5/5 required, 3/4 warnings)  
❌ src/hooks/useAuth.test.ts              (4/5 required - has .only())
⚠️  src/utils/format.test.ts              (5/5 required, 2/4 warnings)

Summary:
├── Passed:   2 files
├── Warnings: 1 file  
└── Failed:   1 file

Failed files need attention:
• src/hooks/useAuth.test.ts - Remove .only() call on line 23
```

## Custom Rules

Check for `.jest-helper.json` in project root for additional team-specific rules:

```json
{
  "validation_rules": [
    {
      "id": "custom_1",
      "description": "Must use userEvent over fireEvent",
      "pattern": "userEvent",
      "warning": true
    }
  ]
}
```

## Quick Fixes

If validation fails, suggest fixes:

| Failure | Fix |
|---------|-----|
| Missing describe() | Wrap tests in `describe('ComponentName', () => { ... })` |
| Missing "should" | Rename `it('renders', ...)` → `it('should render', ...)` |
| Has .only() | Remove `.only` from test |
| Has .skip() | Remove `.skip` or delete unused test |
| No edge cases | Add tests for null/undefined/empty inputs |
