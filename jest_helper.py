# ============================================================
# JEST HELPER MCP SERVER
#
# This MCP gives Claude tools to:
# - Read and understand your existing test patterns
# - Run tests and see results
# - Write/fix tests matching YOUR style
# ============================================================

import os
import subprocess
import json
import re
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# ------------------------------------------------------------
# INITIALIZE MCP SERVER
# ------------------------------------------------------------
mcp = FastMCP("jest-helper")

# ------------------------------------------------------------
# CONFIGURATION
#
# The project path is passed via environment variable.
# This allows the same MCP to work with any project.
# ------------------------------------------------------------
def get_project_root() -> str:
    """Get the project root from environment variable or current directory."""
    return os.environ.get("PROJECT_ROOT", os.getcwd())


# ============================================================
# SECTION 1: READING TOOLS
# These tools help Claude understand your codebase
# ============================================================

@mcp.tool()
def find_test_files(directory: str = "") -> str:
    """
    Find all test files in the project.

    Args:
        directory: Subdirectory to search in (relative to project root).
                   Leave empty to search entire project.

    Returns:
        List of test file paths, one per line.
    """
    project_root = get_project_root()
    search_path = Path(project_root) / directory if directory else Path(project_root)

    if not search_path.exists():
        return f"Error: Directory not found: {search_path}"

    # Find files matching common test patterns
    test_patterns = [
        "**/*.test.ts",
        "**/*.test.tsx",
        "**/*.test.js",
        "**/*.test.jsx",
        "**/*.spec.ts",
        "**/*.spec.tsx",
        "**/*.spec.js",
        "**/*.spec.jsx",
    ]

    test_files = []
    for pattern in test_patterns:
        test_files.extend(search_path.glob(pattern))

    # Filter out node_modules
    test_files = [f for f in test_files if "node_modules" not in str(f)]

    # Return relative paths for readability
    relative_paths = [str(f.relative_to(project_root)) for f in sorted(test_files)]

    if not relative_paths:
        return "No test files found."

    return f"Found {len(relative_paths)} test files:\n" + "\n".join(relative_paths)


@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read a file from the project.

    Args:
        file_path: Path to the file (relative to project root or absolute)

    Returns:
        The file contents.
    """
    project_root = get_project_root()

    # Handle both relative and absolute paths
    if os.path.isabs(file_path):
        full_path = Path(file_path)
    else:
        full_path = Path(project_root) / file_path

    if not full_path.exists():
        return f"Error: File not found: {full_path}"

    if not full_path.is_file():
        return f"Error: Not a file: {full_path}"

    try:
        content = full_path.read_text(encoding="utf-8")
        return content
    except Exception as e:
        return f"Error reading file: {e}"


@mcp.tool()
def find_source_for_test(test_file_path: str) -> str:
    """
    Find the source file that a test file is testing.

    Args:
        test_file_path: Path to the test file

    Returns:
        The likely source file path, or candidates if multiple found.
    """
    project_root = get_project_root()
    test_path = Path(project_root) / test_file_path

    # Remove test suffix to find source file
    # Button.test.tsx -> Button.tsx
    # Button.spec.tsx -> Button.tsx
    source_name = re.sub(r'\.(test|spec)\.(tsx?|jsx?)$', '', test_path.name)

    # Add back extension
    possible_extensions = ['.tsx', '.ts', '.jsx', '.js']
    candidates = []

    for ext in possible_extensions:
        # Check same directory
        same_dir = test_path.parent / f"{source_name}{ext}"
        if same_dir.exists():
            candidates.append(str(same_dir.relative_to(project_root)))

        # Check parent directory (for __tests__ folders)
        parent_dir = test_path.parent.parent / f"{source_name}{ext}"
        if parent_dir.exists():
            candidates.append(str(parent_dir.relative_to(project_root)))

    if not candidates:
        return f"Could not find source file for {test_file_path}. Expected something like {source_name}.tsx"

    if len(candidates) == 1:
        return f"Source file: {candidates[0]}"

    return "Multiple candidates found:\n" + "\n".join(candidates)


@mcp.tool()
def analyze_test_patterns(sample_count: int = 3) -> str:
    """
    Analyze existing tests to understand the testing patterns used.

    This reads a sample of test files and identifies:
    - Import patterns
    - Describe/it/test usage
    - Mocking patterns
    - Assertion patterns

    Args:
        sample_count: Number of test files to sample (default 3)

    Returns:
        Analysis of the testing patterns found.
    """
    project_root = get_project_root()

    # Find test files
    test_patterns = ["**/*.test.tsx", "**/*.test.ts", "**/*.test.jsx", "**/*.test.js"]
    test_files = []
    for pattern in test_patterns:
        test_files.extend(Path(project_root).glob(pattern))

    test_files = [f for f in test_files if "node_modules" not in str(f)]

    if not test_files:
        return "No test files found to analyze."

    # Sample files
    sample = test_files[:sample_count]

    analysis = {
        "files_analyzed": [],
        "import_patterns": set(),
        "test_structure": set(),
        "mocking_patterns": set(),
        "common_utilities": set(),
    }

    for test_file in sample:
        content = test_file.read_text(encoding="utf-8")
        relative_path = str(test_file.relative_to(project_root))
        analysis["files_analyzed"].append(relative_path)

        # Detect import patterns
        if "from '@testing-library/react'" in content or 'from "@testing-library/react"' in content:
            analysis["import_patterns"].add("@testing-library/react")
        if "render," in content or "render }" in content:
            analysis["common_utilities"].add("render")
        if "screen" in content:
            analysis["common_utilities"].add("screen")
        if "fireEvent" in content:
            analysis["common_utilities"].add("fireEvent")
        if "userEvent" in content:
            analysis["common_utilities"].add("userEvent")
        if "waitFor" in content:
            analysis["common_utilities"].add("waitFor")

        # Detect test structure
        if "describe(" in content and "it(" in content:
            analysis["test_structure"].add("describe + it")
        if "describe(" in content and "test(" in content:
            analysis["test_structure"].add("describe + test")
        if re.search(r'^test\(', content, re.MULTILINE):
            analysis["test_structure"].add("standalone test()")

        # Detect mocking patterns
        if "jest.mock(" in content:
            analysis["mocking_patterns"].add("jest.mock()")
        if "jest.fn()" in content:
            analysis["mocking_patterns"].add("jest.fn()")
        if "jest.spyOn(" in content:
            analysis["mocking_patterns"].add("jest.spyOn()")
        if "mockImplementation" in content:
            analysis["mocking_patterns"].add("mockImplementation")

    # Format output
    output = ["## Test Pattern Analysis", ""]
    output.append(f"**Files Analyzed:** {len(analysis['files_analyzed'])}")
    for f in analysis["files_analyzed"]:
        output.append(f"  - {f}")
    output.append("")

    output.append("**Test Structure Patterns:**")
    for pattern in analysis["test_structure"]:
        output.append(f"  - {pattern}")
    output.append("")

    output.append("**Testing Library Utilities Used:**")
    for util in analysis["common_utilities"]:
        output.append(f"  - {util}")
    output.append("")

    output.append("**Mocking Patterns:**")
    for mock in analysis["mocking_patterns"]:
        output.append(f"  - {mock}")

    return "\n".join(output)


# ============================================================
# SECTION 2: RUNNING TOOLS
# These tools execute Jest and return results
# ============================================================

@mcp.tool()
def run_tests(
    test_path: str = "",
    test_name_pattern: str = "",
    coverage: bool = False,
    watch: bool = False
) -> str:
    """
    Run Jest tests.

    Args:
        test_path: Specific test file or directory to run (optional)
        test_name_pattern: Only run tests matching this pattern (optional)
        coverage: Include coverage report (default False)
        watch: Run in watch mode (default False, usually False for MCP)

    Returns:
        Test results including passes, failures, and error messages.
    """
    project_root = get_project_root()

    # Build the Jest command
    cmd = ["npm", "test", "--"]

    if test_path:
        cmd.append(test_path)

    if test_name_pattern:
        cmd.extend(["-t", test_name_pattern])

    if coverage:
        cmd.append("--coverage")

    if not watch:
        cmd.append("--watchAll=false")

    # Add verbose output for better error messages
    cmd.append("--verbose")

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )

        output = result.stdout + "\n" + result.stderr

        # Add summary at the top
        if result.returncode == 0:
            return "✅ All tests passed!\n\n" + output
        else:
            return "❌ Some tests failed!\n\n" + output

    except subprocess.TimeoutExpired:
        return "Error: Tests timed out after 2 minutes"
    except Exception as e:
        return f"Error running tests: {e}"


@mcp.tool()
def run_single_test(test_file: str, test_name: str = "") -> str:
    """
    Run a single test file with detailed output.

    Args:
        test_file: Path to the test file
        test_name: Specific test name to run (optional)

    Returns:
        Detailed test results.
    """
    return run_tests(test_path=test_file, test_name_pattern=test_name)


# ============================================================
# SECTION 3: WRITING TOOLS
# These tools let Claude write and update tests
# ============================================================

@mcp.tool()
def write_test_file(file_path: str, content: str) -> str:
    """
    Write a test file.

    Args:
        file_path: Path where to write the test (relative to project root)
        content: The test file content

    Returns:
        Success or error message.
    """
    project_root = get_project_root()
    full_path = Path(project_root) / file_path

    # Safety check: only allow test files
    if not any(pattern in file_path for pattern in ['.test.', '.spec.']):
        return "Error: Can only write test files (.test.* or .spec.*)"

    # Safety check: don't write outside project
    try:
        full_path.resolve().relative_to(Path(project_root).resolve())
    except ValueError:
        return "Error: Cannot write outside project directory"

    # Create parent directories if needed
    full_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        full_path.write_text(content, encoding="utf-8")
        return f"✅ Successfully wrote test file: {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"


@mcp.tool()
def update_test_section(
    file_path: str,
    old_content: str,
    new_content: str
) -> str:
    """
    Update a specific section of a test file.

    Args:
        file_path: Path to the test file
        old_content: The exact content to replace
        new_content: The new content

    Returns:
        Success or error message.
    """
    project_root = get_project_root()
    full_path = Path(project_root) / file_path

    if not full_path.exists():
        return f"Error: File not found: {file_path}"

    try:
        content = full_path.read_text(encoding="utf-8")

        if old_content not in content:
            return "Error: Could not find the content to replace. Make sure it matches exactly."

        updated_content = content.replace(old_content, new_content, 1)
        full_path.write_text(updated_content, encoding="utf-8")

        return f"✅ Successfully updated: {file_path}"
    except Exception as e:
        return f"Error updating file: {e}"


# ============================================================
# SECTION 4: UTILITY TOOLS
# ============================================================

@mcp.tool()
def get_jest_config() -> str:
    """
    Get the Jest configuration for the project.

    Returns:
        Jest configuration details.
    """
    project_root = get_project_root()

    config_files = [
        "jest.config.js",
        "jest.config.ts",
        "jest.config.json",
        "jest.config.mjs",
    ]

    for config_file in config_files:
        config_path = Path(project_root) / config_file
        if config_path.exists():
            content = config_path.read_text(encoding="utf-8")
            return f"Found {config_file}:\n\n{content}"

    # Check package.json for jest config
    package_json_path = Path(project_root) / "package.json"
    if package_json_path.exists():
        try:
            package_data = json.loads(package_json_path.read_text())
            if "jest" in package_data:
                return "Jest config in package.json:\n\n" + json.dumps(package_data["jest"], indent=2)
        except json.JSONDecodeError:
            pass

    return "No Jest configuration file found. Using default Jest config."


@mcp.tool()
def list_project_structure(directory: str = "src", max_depth: int = 3) -> str:
    """
    List the project structure to understand the codebase layout.

    Args:
        directory: Starting directory (default "src")
        max_depth: Maximum depth to traverse (default 3)

    Returns:
        Tree-like structure of the project.
    """
    project_root = get_project_root()
    start_path = Path(project_root) / directory

    if not start_path.exists():
        return f"Directory not found: {directory}"

    def build_tree(path: Path, prefix: str = "", depth: int = 0) -> list:
        if depth >= max_depth:
            return []

        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
        lines = []

        for i, item in enumerate(items):
            if item.name in ["node_modules", ".git", "__pycache__", ".venv"]:
                continue

            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            lines.append(f"{prefix}{current_prefix}{item.name}")

            if item.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(build_tree(item, next_prefix, depth + 1))

        return lines

    tree_lines = [directory + "/"] + build_tree(start_path)
    return "\n".join(tree_lines)


# ============================================================
# RUN THE SERVER
# ============================================================
if __name__ == "__main__":
    mcp.run(transport='stdio')
