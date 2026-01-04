"""Codex CLI task helpers for NotebookLM integration."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> None:
    """Run a subprocess and propagate failures."""
    subprocess.run(cmd, check=True, cwd=cwd, env=env)  # noqa: S603


def _codex_exec(prompt: str, env: dict[str, str]) -> None:
    """Execute a Codex prompt with the current environment."""
    _run(["codex", "--enable", "skills", "exec", prompt], env=env)


def _base_env() -> dict[str, str]:
    """Return a mutable environment for Codex invocations."""
    return os.environ.copy()


def _prompt_common(
    question: str,
    notebook_ids: str,
    *,
    allow_subagents: bool,
) -> str:
    """Build the standard notebook query prompt."""
    prefix = (
        "Use the notebooklm-patterns skill with the notebooklm-rpc server. "
        "Assume cookies were created via notebooklm-mcp-auth --file. "
        "List notebooks with mcp__notebooklm-rpc__notebook_list"
    )
    if allow_subagents:
        prefix += (
            " If subagents or task parallelism are available, spawn one subagent per selected "
            "notebook. If subagents are unavailable, run the notebook queries sequentially."
        )

    if notebook_ids:
        return (
            f"{prefix}, then filter to these notebook IDs (comma-separated): "
            f"'{notebook_ids}'. "
            f"Ask each selected notebook via mcp__notebooklm-rpc__notebook_query using "
            f"'{question}'. "
            "Aggregate responses labeled by notebook name and include citations. "
            "If any response is off-topic, retry once with a narrower prompt that starts with: "
            f"'Answer ONLY about: {question}'. If it still drifts, report a likely "
            "notebook-content mismatch."
        )

    return (
        f"{prefix}, then ask each notebook via mcp__notebooklm-rpc__notebook_query using "
        f"'{question}'. "
        "Aggregate responses labeled by notebook name and include citations. "
        "If any response is off-topic, retry once with a narrower prompt that starts with: "
        f"'Answer ONLY about: {question}'. If it still drifts, report a likely "
        "notebook-content mismatch."
    )


def ask_all() -> None:
    """Query all notebooks sequentially."""
    env = _base_env()
    question = env.get("QUESTION", "How can we improve the Codex implementation in this repo?")
    notebook_ids = env.get("NOTEBOOK_IDS", "")
    _codex_exec(_prompt_common(question, notebook_ids, allow_subagents=False), env)


def ask_all_subagents() -> None:
    """Query notebooks with subagents when available."""
    env = _base_env()
    question = env.get("QUESTION", "How can we improve the Codex implementation in this repo?")
    notebook_ids = env.get("NOTEBOOK_IDS", "")
    _codex_exec(_prompt_common(question, notebook_ids, allow_subagents=True), env)


def ask_all_rpc() -> None:
    """Query all notebooks via the RPC MCP server."""
    env = _base_env()
    question = env.get("QUESTION", "How can we improve the Codex implementation in this repo?")
    notebook_ids = env.get("NOTEBOOK_IDS", "")
    _codex_exec(_prompt_common(question, notebook_ids, allow_subagents=False), env)


def _install_skill(skill_url: str, dest_dir: Path) -> None:
    """Install a skill from GitHub into a destination folder."""
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    installer = (
        codex_home
        / "skills"
        / ".system"
        / "skill-installer"
        / "scripts"
        / "install-skill-from-github.py"
    )
    if not installer.exists():
        message = f"Skill installer not found at {installer}"
        raise FileNotFoundError(message)

    _run([sys.executable, str(installer), "--url", skill_url, "--dest", str(dest_dir)])


def _init_git_repo(repo_dir: Path) -> None:
    """Initialize a scratch git repo for Codex tests."""
    _run(["git", "init", "-q"], cwd=repo_dir)
    readme = repo_dir / "README.md"
    readme.write_text("")
    _run(["git", "add", "README.md"], cwd=repo_dir)
    _run(
        [
            "git",
            "-c",
            "user.name=Codex",
            "-c",
            "user.email=codex@local",
            "commit",
            "-q",
            "-m",
            "init",
        ],
        cwd=repo_dir,
    )


def validate_setup() -> None:
    """Verify Codex skill setup in a fresh scratch repo."""
    env = _base_env()
    skill_url = env.get(
        "SKILL_URL",
        "https://github.com/ray-manaloto/notebooklm-claude-integration/tree/main/.codex/skills/notebooklm-patterns",
    )
    question = env.get(
        "QUESTION",
        "How can we improve the Codex implementation in this repo? Please cite sources.",
    )
    notebook_ids = env.get("NOTEBOOK_IDS", "")

    test_root = Path(env.get("TEST_ROOT", tempfile.mkdtemp(prefix="codex-skill-validate-")))
    skill_tmp = Path(env.get("SKILL_TMP", tempfile.mkdtemp(prefix="skill-download-validate-")))
    shutil.rmtree(test_root, ignore_errors=True)
    shutil.rmtree(skill_tmp, ignore_errors=True)
    test_root.mkdir(parents=True, exist_ok=True)
    skill_tmp.mkdir(parents=True, exist_ok=True)

    _install_skill(skill_url, skill_tmp)
    (test_root / ".codex" / "skills").mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        skill_tmp / "notebooklm-patterns",
        test_root / ".codex" / "skills" / "notebooklm-patterns",
    )

    _init_git_repo(test_root)

    prompt = (
        "Use the notebooklm-patterns skill with notebooklm-rpc. "
        "If RPC auth is not configured, stop and report the failure. Then list all notebooks"
    )
    if notebook_ids:
        prompt += f", filter to these notebook IDs (comma-separated): '{notebook_ids}'."
    prompt += (
        f" Ask each selected notebook (via notebook_id): '{question}'. Aggregate responses labeled "
        "by notebook name and include citations. If any response is off-topic, retry once with a "
        f"narrower prompt that starts with: 'Answer ONLY about: {question}'. If it still drifts, "
        "report a likely notebook-content mismatch."
    )

    _codex_exec(prompt, env)


def skill_e2e() -> None:
    """Run a full end-to-end skill validation."""
    env = _base_env()
    skill_url = env.get(
        "SKILL_URL",
        "https://github.com/ray-manaloto/notebooklm-claude-integration/tree/main/.codex/skills/notebooklm-patterns",
    )
    notebook_url = env.get(
        "NOTEBOOK_URL",
        "https://notebooklm.google.com/notebook/e15da715-d381-4766-9106-08e1444a9dc3",
    )
    notebook_id = env.get("NOTEBOOK_ID", "notebooklm-secondary-test")

    test_root = Path(env.get("TEST_ROOT", tempfile.mkdtemp(prefix="codex-skill-e2e-")))
    skill_tmp = Path(env.get("SKILL_TMP", tempfile.mkdtemp(prefix="skill-download-e2e-")))
    shutil.rmtree(test_root, ignore_errors=True)
    shutil.rmtree(skill_tmp, ignore_errors=True)
    test_root.mkdir(parents=True, exist_ok=True)
    skill_tmp.mkdir(parents=True, exist_ok=True)

    _install_skill(skill_url, skill_tmp)
    (test_root / ".codex" / "skills").mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        skill_tmp / "notebooklm-patterns",
        test_root / ".codex" / "skills" / "notebooklm-patterns",
    )

    _init_git_repo(test_root)

    prompt = (
        "Use the notebooklm-patterns skill with notebooklm-rpc. "
        "If RPC auth is not configured, stop and report the failure. "
        f"List notebooks and locate {notebook_url} if present. If it is not present, stop and "
        "report that the notebook was not found. "
        f"Select {notebook_id}, then ask: 'What is this notebook about?' Return a 3-bullet summary "
        "with citations."
    )

    _codex_exec(prompt, env)


def bootstrap_auth() -> None:
    """Force an auth check via the Codex agent."""
    env = _base_env()
    prompt = (
        "Use the notebooklm-patterns skill with notebooklm-rpc. "
        "If RPC auth is not configured, stop and report the failure."
    )
    _codex_exec(prompt, env)


def bootstrap_parallel() -> None:
    """Run auth and then query all notebooks with subagents."""
    env = _base_env()
    question = env.get(
        "QUESTION",
        "Summarize improvements we can make to the Codex NotebookLM integration.",
    )
    env["QUESTION"] = question
    bootstrap_auth()
    ask_all_subagents()


def notebooklm_integration() -> None:
    """Run the NotebookLM integration query with defaults."""
    env = _base_env()
    env["QUESTION"] = env.get("QUESTION", "Summarize the key sources in this notebook.")
    env["NOTEBOOK_IDS"] = env.get("NOTEBOOK_IDS", "pytest-patterns")
    prompt = (
        "Use the notebooklm-patterns skill with notebooklm-rpc. "
        "If RPC auth is not configured, stop and report the failure. Then list notebooks and "
        "filter to these notebook IDs (comma-separated): '{NOTEBOOK_IDS}'. Ask each selected "
        "notebook (via notebook_id) this question: '{QUESTION}'. Aggregate responses labeled by "
        "notebook name and include citations. If any response is off-topic, retry once with a "
        "narrower prompt that starts with: 'Answer ONLY about: {QUESTION}'. If it still drifts, "
        "report a likely notebook-content mismatch."
    ).format(**env)
    _codex_exec(prompt, env)


def auth_rpc() -> None:
    """Ensure NotebookLM RPC auth is available, launching auth if needed."""
    auth_file = Path(
        os.environ.get("AUTH_FILE", "~/.notebooklm-mcp/auth.json"),
    ).expanduser()
    force_reauth = os.environ.get("FORCE_REAUTH", "0") == "1"
    cookie_file = os.environ.get("COOKIE_FILE", "")

    if not force_reauth and auth_file.exists() and auth_file.stat().st_size > 0:
        check_script = ROOT / "tools" / "notebooklm_auth_check_rpc.py"
        try:
            _run([sys.executable, str(check_script)])
        except subprocess.CalledProcessError:
            pass
        else:
            return

    cmd = ["notebooklm-mcp-auth", "--file"]
    if cookie_file:
        cmd.append(cookie_file)
    _run(cmd)


def auth_check_rpc() -> None:
    """Run the RPC auth health check."""
    _run([sys.executable, str(ROOT / "tools" / "notebooklm_auth_check_rpc.py")])


def main() -> int:
    """Dispatch Codex task commands."""
    parser = argparse.ArgumentParser(description="Codex NotebookLM Pixi tasks")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in (
        "ask-all",
        "ask-all-subagents",
        "ask-all-rpc",
        "validate-setup",
        "skill-e2e",
        "bootstrap-auth",
        "bootstrap-parallel",
        "notebooklm-integration",
        "auth-rpc",
        "auth-check-rpc",
    ):
        sub.add_parser(name)

    args = parser.parse_args()
    commands = {
        "ask-all": ask_all,
        "ask-all-subagents": ask_all_subagents,
        "ask-all-rpc": ask_all_rpc,
        "validate-setup": validate_setup,
        "skill-e2e": skill_e2e,
        "bootstrap-auth": bootstrap_auth,
        "bootstrap-parallel": bootstrap_parallel,
        "notebooklm-integration": notebooklm_integration,
        "auth-rpc": auth_rpc,
        "auth-check-rpc": auth_check_rpc,
    }
    commands[args.command]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
