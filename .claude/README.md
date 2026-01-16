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

As part of our recent hackathon, we explored how we can use Claude in a more effective and consistent way across our projects.

What we noticed is that most of the time, Claude is used as a generic assistant. It’s powerful, but the quality of the output depends heavily on how you ask the question. Different prompts lead to different answers — and sometimes the answer is right, sometimes it’s close, and over time that can lead to inconsistency.

So we tried something different.

We focused on turning Claude from a generic assistant into a repeatable teammate that follows our standards, using Claude Custom Commands.

At a simple level, Claude Custom Commands are reusable, standardized prompts that live directly in the project. They’re defined once as a one-time setup, and from that point on, anyone on the team can run the exact same workflow and get consistent results.

But the real value isn’t just reuse — it’s removing prompt skill from the equation.

Developers no longer need to know how to phrase the perfect question or remember all the project context. The command already knows, because we’ve given it a clear and detailed understanding of what it needs to do and how it should do it.

The end result is faster onboarding, more consistent code and tests, and less dependency on who knows what or how a question is asked.

⸻

Use Case 1: Writing Unit Tests

The first command we focused on was writing unit tests, because it’s something we do repeatedly across UI projects.

For this, we created a Custom Command backed by a simple markdown file. That file clearly defines our testing patterns — how test files should be structured, how mocks should look, and how describe and test blocks are organized.

When the command runs, Claude doesn’t just generate a test from scratch. It first:
	•	reads the source file,
	•	identifies whether it’s a component, hook, utility, or API,
	•	and looks at one or two existing test files in the repo to match our conventions.

Based on that, it generates a test that already follows our patterns and fits naturally into the codebase.

The goal here isn’t just speed — it’s consistency. The tests look like something a team member would write, not something generated and then rewritten.

⸻

Use Case 2: Onboarding a Developer

The second command — and arguably the most impactful one — is onboarding.

This command is designed for a very common scenario: someone new to a project trying to run a UI application locally.

When the onboarding command runs, it first understands the project structure. Since we started with UI applications, it looks for the main module, finds the package.json, and understands how the app is built and run using NPM.

From there, it:
	•	installs dependencies,
	•	runs an audit to check for vulnerabilities or outdated packages,
	•	applies fixes where possible,
	•	and then walks the developer through exactly how to run the application locally.

While many projects already have a README, this command turns onboarding into a guided workflow instead of a manual, trial-and-error process.

Instead of guessing or searching through documentation, the developer is guided step by step based on the actual state of the repo.

