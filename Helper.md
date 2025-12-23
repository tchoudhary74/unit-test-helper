🧪 Jest Helper MCP (Claude) — Standardizing Unit Tests at Scale

Why I Built This

Our biggest problem with tests isn’t Jest itself — it’s inconsistency.
	•	Every developer writes tests differently
	•	Reviews waste time on style instead of intent
	•	Fixing or adding tests is slow because “what’s the right pattern?” isn’t obvious

This MCP solves that by giving Claude controlled access to our repo so it can:
	•	understand how we already write tests
	•	write new tests that match our style
	•	enforce consistency automatically

The goal is simple:
tests should look like they were written by one disciplined team, not ten individuals.

⸻

What This MCP Actually Does

This is a FastMCP server called jest-helper that runs inside a repo and exposes a focused set of tools Claude can use.

At a high level, it supports five things:
	1.	Read & understand existing tests
	2.	Analyze test patterns used in the repo
	3.	Run Jest tests safely
	4.	Write or update test files
	5.	Validate tests against team rules

Everything is scoped to the project root and guarded by strict safety checks.

⸻

Safety & Guardrails (By Design)

This MCP is intentionally restrictive:
	•	✅ Can only read files inside the repo
	•	✅ Can only write *.test.* or *.spec.* files
	•	✅ File reads capped at 1MB
	•	✅ Large outputs are truncated automatically
	•	❌ No access outside PROJECT_ROOT

This makes it safe to use locally, in devspaces, or later in CI-style automation.

⸻

Configuration Model

If .jest-helper.json exists → it’s used
If not → sensible defaults apply

The config controls:
	•	test structure rules (describe/it, naming, AAA)
	•	templates (React, hooks, utilities, API tests)
	•	validation rules (required vs warning vs forbidden)

There’s also a helper tool to generate a starter config and commit it so the entire team shares the same standards.

⸻

Core Tooling (What Claude Can Do)

🧠 Understand the Codebase
	•	Find all test files
	•	Read test or source files safely
	•	Infer which source file a test maps to
	•	Analyze real test patterns (imports, mocks, assertions, naming)

This is how Claude learns our style instead of guessing.

⸻

🏃 Run Tests
	•	Run all tests, a single file, or a single test name
	•	Optional coverage
	•	Clean, readable output with pass/fail summaries

Good for tight feedback loops while fixing or writing tests.

⸻

✍️ Write & Update Tests
	•	Create new test files using approved templates
	•	Update specific sections of an existing test (surgical changes, clean diffs)

No free-form file editing. Everything stays controlled.

⸻

✅ Enforce Consistency
	•	Get the official team test style guide
	•	Generate canonical test templates
	•	Validate a test file against regex-based rules
	•	Analyze a test and tell you exactly how to rewrite it to standard

This is the part that turns “guidelines” into something enforceable.

⸻

Recommended Developer Flow

When adding a new test
	1.	Read the style guide
	2.	Use the correct template
	3.	Write the test
	4.	Validate it
	5.	Run it

When fixing an existing test
	1.	Run the failing test
	2.	Ask for rewrite guidance if needed
	3.	Update only the broken section
	4.	Validate and re-run

⸻

Why This Works Well
	•	It’s opinionated but configurable
	•	It learns from our repo, not generic examples
	•	It removes style debates from code reviews
	•	It scales across teams without relying on tribal knowledge

This MCP turns Claude into a test-aware team member, not just a code generator.
