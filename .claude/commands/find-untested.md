# Find Untested Files Command

Find source files that don't have corresponding test files in: $ARGUMENTS

If no path specified, scan `src/` directory.

## Process

### Step 1: Find All Source Files
```bash
find ${ARGUMENTS:-src} -name "*.ts" -o -name "*.tsx" | grep -v node_modules | grep -v ".test." | grep -v ".spec." | grep -v "__tests__"
```

### Step 2: Check for Corresponding Tests

For each source file, look for test file in these locations:
- Same directory: `Component.tsx` → `Component.test.tsx`
- `__tests__` subfolder: `Component.tsx` → `__tests__/Component.test.tsx`
- Parent `__tests__`: `components/Button.tsx` → `components/__tests__/Button.test.tsx`

### Step 3: Categorize Results

**Test file patterns to match:**
- `[filename].test.ts`
- `[filename].test.tsx`
- `[filename].spec.ts`
- `[filename].spec.tsx`

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║  UNTESTED FILES REPORT                                          ║
╠════════════════════════════════════════════════════════════════╣
║  Scanned: src/                                                  ║
║  Source files: 45                                               ║
║  With tests: 32                                                 ║
║  Without tests: 13                                              ║
║  Coverage: 71%                                                  ║
╚════════════════════════════════════════════════════════════════╝

┌─ Files Missing Tests ──────────────────────────────────────────┐
│                                                                │
│ Components (5 files):                                          │
│   • src/components/Modal.tsx                                   │
│   • src/components/Tooltip.tsx                                 │
│   • src/components/Dropdown.tsx                                │
│   • src/components/Avatar.tsx                                  │
│   • src/components/Badge.tsx                                   │
│                                                                │
│ Hooks (3 files):                                               │
│   • src/hooks/useDebounce.ts                                   │
│   • src/hooks/useLocalStorage.ts                               │
│   • src/hooks/useMediaQuery.ts                                 │
│                                                                │
│ Utils (2 files):                                               │
│   • src/utils/validators.ts                                    │
│   • src/utils/formatters.ts                                    │
│                                                                │
│ Services (3 files):                                            │
│   • src/services/analytics.ts                                  │
│   • src/services/storage.ts                                    │
│   • src/services/notifications.ts                              │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌─ Priority Recommendations ─────────────────────────────────────┐
│                                                                │
│ High Priority (complex/critical):                              │
│   1. src/hooks/useLocalStorage.ts - state management          │
│   2. src/utils/validators.ts - data validation                │
│   3. src/services/analytics.ts - tracking logic               │
│                                                                │
│ Medium Priority:                                               │
│   4. src/components/Modal.tsx - user interaction              │
│   5. src/components/Dropdown.tsx - user interaction           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Exclusions

Skip these by default (typically don't need direct tests):
- `index.ts` / `index.tsx` (barrel exports)
- `*.d.ts` (type definitions)
- `*.types.ts` (type-only files)
- `*.styles.ts` (style definitions)
- `*.constants.ts` (pure constants)
- Files in `__mocks__/` directories

## Actions

After identifying untested files, use:
- `/write-tests src/components/Modal.tsx` to create tests
- `/analyze-tests` to understand existing patterns first

## Integration with CI

Suggest adding to CI pipeline:
```yaml
# .github/workflows/test.yml
- name: Check test coverage
  run: |
    npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
```
