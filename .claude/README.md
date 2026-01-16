# Jest Helper Commands for Claude Code

A set of custom commands that help Claude write, analyze, and maintain Jest tests following team conventions.

## Installation

Copy the `.claude/commands/` folder to your project root:

```bash
cp -r .claude/commands/ your-project/.claude/commands/
```

Then restart Claude Code to load the commands.

## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/write-tests` | Write new tests for a file/component | `/write-tests src/components/Button.tsx` |
| `/fix-tests` | Fix existing tests to match standards | `/fix-tests src/components/Button.test.tsx` |
| `/run-tests` | Run Jest tests | `/run-tests src/components/` |
| `/validate-tests` | Check test style compliance | `/validate-tests src/` |
| `/analyze-tests` | Analyze testing patterns in codebase | `/analyze-tests` |
| `/find-untested` | Find source files without tests | `/find-untested src/` |
| `/init-test-config` | Create team config file | `/init-test-config strict` |
| `/test-patterns` | Quick reference for test patterns | `/test-patterns mocking` |

## Configuration

Optionally create `.jest-helper.json` in your project root to customize team standards:

```json
{
  "style_guide": {
    "test_structure": "describe + it",
    "it_naming": "should + verb"
  },
  "validation_rules": [
    {
      "id": "custom_rule",
      "description": "Must use userEvent",
      "pattern": "userEvent\\.setup"
    }
  ]
}
```

## Workflow Examples

### Write tests for a new component
```
/analyze-tests                           # Understand existing patterns
/write-tests src/components/Modal.tsx    # Write tests
/run-tests src/components/Modal.test.tsx # Verify they pass
/validate-tests src/components/Modal.test.tsx # Check style
```

### Fix an existing test file
```
/validate-tests src/hooks/useAuth.test.ts  # See what's wrong
/fix-tests src/hooks/useAuth.test.ts       # Fix issues
/run-tests src/hooks/useAuth.test.ts       # Verify still passes
```

### Improve test coverage
```
/find-untested src/                        # Find gaps
/write-tests src/utils/validators.ts       # Add missing tests
```

## Enforced Standards

By default, these standards are enforced:

**Required:**
- Tests use `describe()` blocks
- Tests use `it()` or `test()`
- Tests have `expect()` assertions
- No `.only()` or `.skip()` left in code

**Encouraged (warnings):**
- `it()` names start with "should"
- Edge cases are tested (null, undefined, empty)
- Uses Testing Library best practices

## Files

```
.claude/commands/
├── write-tests.md      # Write new tests
├── fix-tests.md        # Fix/refactor tests
├── run-tests.md        # Execute tests
├── validate-tests.md   # Check compliance
├── analyze-tests.md    # Analyze patterns
├── find-untested.md    # Find coverage gaps
├── init-test-config.md # Create config
└── test-patterns.md    # Quick reference
```

## Customization

Edit any `.md` file in `.claude/commands/` to adjust the instructions for your team's specific needs.

