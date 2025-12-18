The Jest MCP Server - What I Built

📚 Architecture Philosophy

┌─────────────────────────────────────────────────────────────────┐
│ Claude (The Brain) │
│ │
│ "I need to write a test for Button.tsx" │
│ │
│ 1. analyze_test_patterns() → Learn your team's style │
│ 2. read_file("Button.tsx") → Understand the component │
│ 3. find_test_files() → Find similar tests │
│ 4. read_file("...test.tsx")→ Study existing patterns │
│ 5. write_test_file() → Write test in YOUR style │
│ 6. run_tests() → Verify it works │
│ 7. update_test_section() → Fix if needed │
│ │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ Jest MCP Server (The Tools) │
│ │
│ READ TOOLS RUN TOOLS WRITE TOOLS │
│ ───────────── ────────── ─────────── │
│ • find_test_files • run_tests • write_test_file │
│ • read_file • run_single_test • update_test_section │
│ • find_source_for_test │
│ • analyze_test_patterns │
│ • get_jest_config │
│ • list_project_structure │
│ │
└─────────────────────────────────────────────────────────────────┘

---

Tools Summary

| Tool                   | What It Does            | Why It Matters                   |
| ---------------------- | ----------------------- | -------------------------------- |
| find_test_files        | Lists all test files    | Claude knows what tests exist    |
| read_file              | Reads any file          | Claude studies your code & tests |
| find_source_for_test   | Maps test → source      | Knows what file a test covers    |
| analyze_test_patterns  | Studies your style      | Learns describe/it/test patterns |
| run_tests              | Runs Jest               | Sees pass/fail results           |
| run_single_test        | Runs one test file      | Quick feedback loop              |
| write_test_file        | Creates/overwrites test | Only allows .test.\* files       |
| update_test_section    | Edits part of a test    | Surgical fixes                   |
| get_jest_config        | Reads Jest config       | Understands your setup           |
| list_project_structure | Shows folder structure  | Navigates your codebase          |

---

Key Safety Features

# Can only write test files

if not any(pattern in file_path for pattern in ['.test.', '.spec.']):
return "Error: Can only write test files"

# Can't write outside project

full_path.resolve().relative_to(Path(project_root).resolve())

---

Let's test it with the MCP Inspector:

⏺ Bash(uv run python jest_helper.py 2>&1 & timeout: 10s
sleep 2…)
⎿  Server syntax OK - ready for testing

⏺ Server works! Now let's connect it to Claude Code.

---

Connecting Jest MCP to Claude Code CLI

The key difference: we need to pass your project path to the MCP so it knows where your React project is.

Run this command (replace the project path with your actual React project):

claude mcp add jest-helper \
 -e PROJECT_ROOT=/path/to/your/react/project \
 -- /Users/tharunchoudhary/.local/bin/uv \
 --directory /Users/tharunchoudhary/Desktop/pythonPR/MCP/jest-helper \
 run jest_helper.py

📚 Breaking This Down:

claude mcp add jest-helper # Name of the MCP server
-e PROJECT_ROOT=/path/to/project # 👈 YOUR React project path!
-- # Separator
/Users/.../uv # Command to run
--directory /Users/.../jest-helper # Where the MCP code is
run jest_helper.py # The MCP server file

claude mcp add github \
 -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here \
 -e GITHUB_API_URL=https://github.yourcompany.com/api/v3 \
 -- npx -y @modelcontextprotocol/server-github

There's already an official GitHub MCP (@modelcontextprotocol/server-github) that's well-maintained and comprehensive. You just run it with npx - no coding needed.

So my question is:

Do you want me to:

A) Help you set up the official one (recommended)

- Battle-tested, maintained by MCP team
- Just needs your token and one command
- Works with Enterprise GitHub too

B) Build a custom GitHub MCP from scratch

- Good if you want specific features only
- Learning experience (like we did with weather/jest)
- More control over what tools are exposed

C) Build a lightweight custom one for your specific workflow

- Only the tools you actually use (e.g., just PRs and issues)
- Simpler, easier to get security approval for
- Can be tailored to your enterprise setup
