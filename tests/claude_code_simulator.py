"""Simulate the Claude Code CLI with the NotebookLM plugin installed.

This script is used for manual testing of the plugin interface.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

PLUGIN_DIR = Path.home() / ".claude" / "plugins" / "installed" / "notebooklm"
SCRIPTS_DIR = PLUGIN_DIR / "skills" / "notebooklm" / "scripts"


class Colors:
    """ANSI color codes for terminal output."""

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


logger = logging.getLogger("claude_code_simulator")
MIN_SUBCOMMAND_PARTS = 2


def _configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _emit(message: str = "") -> None:
    logger.info(message)


def _handle_notebook_auth(parts: list[str]) -> None:
    if len(parts) < MIN_SUBCOMMAND_PARTS:
        _emit(
            f"{Colors.RED}Usage: /notebook-auth <status|setup|reset>{Colors.RESET}",
        )
        return

    subcmd = parts[1]
    result = execute_command("auth", [subcmd])
    format_response(result)


def _handle_notebook(parts: list[str]) -> None:
    if len(parts) < MIN_SUBCOMMAND_PARTS:
        _emit(
            f"{Colors.RED}Usage: /notebook <add|list|activate|ask> [args]{Colors.RESET}",
        )
        return

    subcmd = parts[1]
    args = parts[2].split() if len(parts) > MIN_SUBCOMMAND_PARTS else []

    result = execute_command(subcmd, args)
    format_response(result)


def _handle_command(user_input: str) -> bool:
    parts = user_input.split(maxsplit=2)
    command = parts[0].lower()

    if command == "/exit":
        _emit(f"{Colors.YELLOW}Goodbye!{Colors.RESET}")
        return False

    if command == "/help":
        show_help()
        return True

    if command == "/notebook-auth":
        _handle_notebook_auth(parts)
        return True

    if command == "/notebook":
        _handle_notebook(parts)
        return True

    _emit(f"{Colors.RED}Unknown command: {command}{Colors.RESET}")
    _emit(f"Type {Colors.BLUE}/help{Colors.RESET} for available commands")
    return True


def print_header() -> None:
    """Print the Claude Code header."""
    _emit(f"{Colors.BOLD}{Colors.BLUE}")
    _emit("╔════════════════════════════════════════════════════════════╗")
    _emit("║              Claude Code CLI v2.0.12                        ║")
    _emit("║         NotebookLM Plugin Demo (SIMULATED)                  ║")
    _emit("╚════════════════════════════════════════════════════════════╝")
    _emit(f"{Colors.RESET}")


def execute_command(cmd: str, args: list[str]) -> dict:
    """Execute a plugin command."""
    script_path = SCRIPTS_DIR / "run.py"

    try:
        result = subprocess.run(  # noqa: S603
            [sys.executable, str(script_path), cmd, *args],
            capture_output=True,
            check=False,  # CLI script returns JSON on stdout.
            text=True,
            timeout=10,
        )
        return json.loads(result.stdout)
    except (json.JSONDecodeError, subprocess.TimeoutExpired, OSError) as exc:
        return {"success": False, "error": str(exc)}


def _format_notebook_list(data: dict) -> None:
    _emit(f"{Colors.BOLD}Notebooks in library:{Colors.RESET}")
    for notebook in data["notebooks"]:
        active = "●" if notebook.get("active") else "○"
        topics = ", ".join(notebook.get("topics", []))
        _emit(f"  {active} {notebook['name']}")
        _emit(f"    ID: {notebook['id'][:16]}...")
        _emit(f"    Topics: {topics}")
        _emit()


def _format_answer(data: dict) -> None:
    _emit(f"{Colors.BOLD}Question:{Colors.RESET}")
    _emit(f"  {data['question']}")
    _emit()
    _emit(f"{Colors.BOLD}Answer from {data['notebook']['name']}:{Colors.RESET}")
    _emit(f"{data['answer']}")
    _emit()

    citations = data.get("citations") or []
    if citations:
        _emit(f"{Colors.BOLD}Citations:{Colors.RESET}")
        for cite in citations:
            _emit(f"  • {cite['source']}")
        _emit()

    follow_ups = data.get("follow_up_questions") or []
    if follow_ups:
        _emit(f"{Colors.YELLOW}Suggested follow-ups:{Colors.RESET}")
        for question in follow_ups:
            _emit(f"  ? {question}")


def _format_auth(data: dict) -> None:
    if data["authenticated"]:
        _emit(f"{Colors.GREEN}● Authenticated{Colors.RESET}")
        if data.get("email"):
            _emit(f"  Email: {data['email']}")
        return
    _emit(f"{Colors.YELLOW}○ Not authenticated{Colors.RESET}")
    _emit(f"  {data.get('message', '')}")


def _format_single_notebook(data: dict) -> None:
    notebook = data["notebook"]
    _emit(f"{Colors.BOLD}{notebook['name']}{Colors.RESET}")
    _emit(f"  ID: {notebook['id']}")
    _emit(f"  Description: {notebook.get('description', 'N/A')}")
    _emit(f"  Topics: {', '.join(notebook.get('topics', []))}")
    _emit(f"  Sources: {notebook.get('sources_count', 'N/A')}")


def format_response(data: dict) -> None:
    """Format the response for display."""
    if not data.get("success"):
        _emit(f"{Colors.RED}✗ Error: {data.get('error', 'Unknown error')}{Colors.RESET}")
        return

    _emit(f"{Colors.GREEN}✓ Success{Colors.RESET}")
    _emit()

    if "notebooks" in data:
        _format_notebook_list(data)
    elif "answer" in data:
        _format_answer(data)
    elif "authenticated" in data:
        _format_auth(data)
    elif "notebook" in data:
        _format_single_notebook(data)
    else:
        _emit(json.dumps(data, indent=2))


def show_help() -> None:
    """Show available commands."""
    _emit(f"{Colors.BOLD}Available Commands:{Colors.RESET}")
    _emit()
    _emit(f"  {Colors.BLUE}/notebook-auth status{Colors.RESET}")
    _emit("    Check authentication status")
    _emit()
    _emit(f"  {Colors.BLUE}/notebook-auth setup{Colors.RESET}")
    _emit("    Setup authentication (opens Chrome for Google login)")
    _emit()
    _emit(f"  {Colors.BLUE}/notebook add <url>{Colors.RESET}")
    _emit("    Add a notebook to your library")
    _emit()
    _emit(f"  {Colors.BLUE}/notebook list{Colors.RESET}")
    _emit("    List all notebooks in your library")
    _emit()
    _emit(f"  {Colors.BLUE}/notebook activate <name>{Colors.RESET}")
    _emit("    Activate a specific notebook")
    _emit()
    _emit(f'  {Colors.BLUE}/notebook ask "<question>"{Colors.RESET}')
    _emit("    Ask a question to the active notebook")
    _emit()
    _emit(f"  {Colors.BLUE}/help{Colors.RESET}")
    _emit("    Show this help message")
    _emit()
    _emit(f"  {Colors.BLUE}/exit{Colors.RESET}")
    _emit("    Exit Claude Code")
    _emit()


def main() -> None:
    """Run the main REPL loop."""
    _configure_logging()
    print_header()
    _emit(f"{Colors.YELLOW}NOTE: This is a SIMULATED environment.{Colors.RESET}")
    _emit(f"{Colors.YELLOW}Real Claude Code requires installation and API keys.{Colors.RESET}")
    _emit(
        f"{Colors.YELLOW}Browser automation is mocked (requires Chrome + network).{Colors.RESET}",
    )
    _emit()
    _emit("Type /help for available commands")
    _emit()

    while True:
        try:
            # Prompt
            user_input = input(f"{Colors.BOLD}claude> {Colors.RESET}").strip()

            if not user_input:
                continue

            # Parse command
            should_continue = _handle_command(user_input)
            if not should_continue:
                break
            _emit()

        except KeyboardInterrupt:
            _emit(f"\n{Colors.YELLOW}Use /exit to quit{Colors.RESET}")
        except EOFError:
            _emit(f"\n{Colors.YELLOW}Goodbye!{Colors.RESET}")
            break


if __name__ == "__main__":
    main()
