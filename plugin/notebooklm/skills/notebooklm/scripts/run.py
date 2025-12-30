#!/usr/bin/env python3
"""
NotebookLM Automation Wrapper
Provides a unified interface for all NotebookLM operations.
"""

import sys
import json
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

def ensure_data_dir():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR

def run_command(script_name: str, args: list):
    """Run a NotebookLM script with the given arguments"""
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        return {
            "success": False,
            "error": f"Script not found: {script_name}",
            "available_scripts": [
                "auth_manager.py",
                "notebook_manager.py", 
                "ask_question.py"
            ]
        }
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Try to parse JSON output
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out after 60 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """Main entry point"""
    ensure_data_dir()
    
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "No command specified",
            "usage": "run.py <command> [args]",
            "commands": {
                "auth": "Manage authentication",
                "add": "Add a notebook to library",
                "list": "List all notebooks", 
                "activate": "Activate a notebook",
                "ask": "Ask a question to NotebookLM",
                "search": "Search for notebooks by topic"
            }
        }, indent=2))
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Route commands to appropriate scripts
    if command == "auth":
        result = run_command("auth_manager.py", args)
    elif command in ["add", "list", "activate", "search"]:
        result = run_command("notebook_manager.py", [command] + args)
    elif command == "ask":
        if not args:
            result = {
                "success": False,
                "error": "Question required",
                "usage": "run.py ask \"Your question here\""
            }
        else:
            result = run_command("ask_question.py", args)
    else:
        result = {
            "success": False,
            "error": f"Unknown command: {command}",
            "available_commands": ["auth", "add", "list", "activate", "ask", "search"]
        }
    
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)

if __name__ == "__main__":
    main()
