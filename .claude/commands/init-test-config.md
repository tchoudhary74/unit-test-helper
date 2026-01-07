# Initialize Test Config Command

Initialize Jest helper configuration for this project.

$ARGUMENTS can be: `default`, `strict`, `minimal`, or empty (uses default)

## What This Does

Creates a `.jest-helper.json` file in the project root that defines:
- Team test style guide
- Validation rules
- Custom conventions

## Configuration Profiles

### Default Profile
Balanced rules suitable for most teams:
- `describe + it` structure required
- "should" naming encouraged (warning)
- Edge case testing encouraged (warning)
- No `.only()` or `.skip()` allowed

### Strict Profile  
Enforced standards for larger teams:
- All default rules as required (not warnings)
- AAA comments required
- Minimum assertions per test
- Coverage thresholds

### Minimal Profile
Light-touch for small projects:
- Only basic structure required
- Most rules as warnings
- Flexible naming

## Generated Config

```json
{
  "style_guide": {
    "test_structure": "describe + it",
    "it_naming": "should + verb",
    "describe_naming": "component/function name",
    "arrangement": "AAA (Arrange-Act-Assert) structure",
    "imports_order": ["react", "testing-library", "components", "utils", "mocks"],
    "assertions_per_test": "1-3 related assertions",
    "edge_cases_required": ["null/undefined", "empty values", "error states"],
    "custom_rules": []
  },
  "validation_rules": [
    {
      "id": "has_describe",
      "description": "Test must use describe() blocks",
      "pattern": "describe\\s*\\("
    },
    {
      "id": "has_it_or_test", 
      "description": "Test must use it() or test()",
      "pattern": "(it|test)\\s*\\("
    },
    {
      "id": "it_uses_should",
      "description": "it() should start with 'should'",
      "pattern": "it\\s*\\(\\s*['\"]should",
      "warning": true
    },
    {
      "id": "has_assertions",
      "description": "Test must have assertions",
      "pattern": "expect\\s*\\("
    },
    {
      "id": "no_only",
      "description": "No .only() in tests",
      "pattern": "\\.only\\s*\\(",
      "must_not_match": true
    },
    {
      "id": "no_skip",
      "description": "No .skip() in tests", 
      "pattern": "\\.skip\\s*\\(",
      "must_not_match": true
    },
    {
      "id": "has_edge_cases",
      "description": "Should test edge cases",
      "pattern": "(null|undefined|empty|error)",
      "warning": true
    }
  ]
}
```

## After Initialization

1. **Review the config** - adjust rules to match team preferences
2. **Commit to repo** - so all developers share the same standards
3. **Use with commands**:
   - `/write-tests` will follow these conventions
   - `/validate-tests` will check against these rules
   - `/fix-tests` will apply these standards

## Customization Examples

### Add Custom Rule
```json
{
  "validation_rules": [
    {
      "id": "uses_user_event",
      "description": "Must use userEvent over fireEvent",
      "pattern": "userEvent\\.setup\\(",
      "warning": true
    }
  ]
}
```

### Make Warning Required
Change `"warning": true` to remove it (making rule required):
```json
{
  "id": "it_uses_should",
  "description": "it() must start with 'should'",
  "pattern": "it\\s*\\(\\s*['\"]should"
}
```

### Add Team-Specific Guidelines
```json
{
  "style_guide": {
    "custom_rules": [
      "Always mock API calls in service tests",
      "Use data-testid only as last resort",
      "Prefer screen queries over container queries",
      "Group tests by behavior, not implementation"
    ]
  }
}
```

## File Location

The config file will be created at:
```
[project-root]/.jest-helper.json
```

Make sure to add it to version control.
