#!/usr/bin/env python3
"""
Claude Code Simulator - NotebookLM Plugin Demo
Simulates Claude Code CLI with the NotebookLM plugin installed.
"""

import sys
import json
import subprocess
from pathlib import Path

PLUGIN_DIR = Path.home() / ".claude" / "plugins" / "installed" / "notebooklm"
SCRIPTS_DIR = PLUGIN_DIR / "skills" / "notebooklm" / "scripts"

class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header():
    """Print Claude Code header"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║              Claude Code CLI v2.0.12                        ║")
    print("║         NotebookLM Plugin Demo (SIMULATED)                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

def execute_command(cmd: str, args: list):
    """Execute a plugin command"""
    script_path = SCRIPTS_DIR / "run.py"
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), cmd] + args,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        data = json.loads(result.stdout)
        return data
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def format_response(data: dict):
    """Format the response for display"""
    if not data.get("success"):
        print(f"{Colors.RED}✗ Error: {data.get('error', 'Unknown error')}{Colors.RESET}")
        return
    
    print(f"{Colors.GREEN}✓ Success{Colors.RESET}")
    print()
    
    # Handle different response types
    if "notebooks" in data:
        # List response
        print(f"{Colors.BOLD}Notebooks in library:{Colors.RESET}")
        for nb in data["notebooks"]:
            active = "●" if nb.get("active") else "○"
            print(f"  {active} {nb['name']}")
            print(f"    ID: {nb['id'][:16]}...")
            print(f"    Topics: {', '.join(nb['topics'])}")
            print()
    
    elif "answer" in data:
        # Question response
        print(f"{Colors.BOLD}Question:{Colors.RESET}")
        print(f"  {data['question']}")
        print()
        print(f"{Colors.BOLD}Answer from {data['notebook']['name']}:{Colors.RESET}")
        print(f"{data['answer']}")
        print()
        
        if data.get("citations"):
            print(f"{Colors.BOLD}Citations:{Colors.RESET}")
            for cite in data["citations"]:
                print(f"  • {cite['source']}")
        print()
        
        if data.get("follow_up_questions"):
            print(f"{Colors.YELLOW}Suggested follow-ups:{Colors.RESET}")
            for q in data["follow_up_questions"]:
                print(f"  ? {q}")
    
    elif "authenticated" in data:
        # Auth response
        if data["authenticated"]:
            print(f"{Colors.GREEN}● Authenticated{Colors.RESET}")
            if data.get("email"):
                print(f"  Email: {data['email']}")
        else:
            print(f"{Colors.YELLOW}○ Not authenticated{Colors.RESET}")
            print(f"  {data.get('message', '')}")
    
    elif "notebook" in data:
        # Single notebook response
        nb = data["notebook"]
        print(f"{Colors.BOLD}{nb['name']}{Colors.RESET}")
        print(f"  ID: {nb['id']}")
        print(f"  Description: {nb.get('description', 'N/A')}")
        print(f"  Topics: {', '.join(nb.get('topics', []))}")
        print(f"  Sources: {nb.get('sources_count', 'N/A')}")
    
    else:
        # Generic response
        print(json.dumps(data, indent=2))

def show_help():
    """Show available commands"""
    print(f"{Colors.BOLD}Available Commands:{Colors.RESET}")
    print()
    print(f"  {Colors.BLUE}/notebook-auth status{Colors.RESET}")
    print(f"    Check authentication status")
    print()
    print(f"  {Colors.BLUE}/notebook-auth setup{Colors.RESET}")
    print(f"    Setup authentication (opens Chrome for Google login)")
    print()
    print(f"  {Colors.BLUE}/notebook add <url>{Colors.RESET}")
    print(f"    Add a notebook to your library")
    print()
    print(f"  {Colors.BLUE}/notebook list{Colors.RESET}")
    print(f"    List all notebooks in your library")
    print()
    print(f"  {Colors.BLUE}/notebook activate <name>{Colors.RESET}")
    print(f"    Activate a specific notebook")
    print()
    print(f"  {Colors.BLUE}/notebook ask \"<question>\"{Colors.RESET}")
    print(f"    Ask a question to the active notebook")
    print()
    print(f"  {Colors.BLUE}/help{Colors.RESET}")
    print(f"    Show this help message")
    print()
    print(f"  {Colors.BLUE}/exit{Colors.RESET}")
    print(f"    Exit Claude Code")
    print()

def main():
    """Main REPL loop"""
    print_header()
    print(f"{Colors.YELLOW}NOTE: This is a SIMULATED environment.{Colors.RESET}")
    print(f"{Colors.YELLOW}Real Claude Code requires installation and API keys.{Colors.RESET}")
    print(f"{Colors.YELLOW}Browser automation is mocked (requires Chrome + network).{Colors.RESET}")
    print()
    print("Type /help for available commands")
    print()
    
    while True:
        try:
            # Prompt
            user_input = input(f"{Colors.BOLD}claude> {Colors.RESET}").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(maxsplit=2)
            command = parts[0].lower()
            
            if command == "/exit":
                print(f"{Colors.YELLOW}Goodbye!{Colors.RESET}")
                break
            
            elif command == "/help":
                show_help()
            
            elif command == "/notebook-auth":
                if len(parts) < 2:
                    print(f"{Colors.RED}Usage: /notebook-auth <status|setup|reset>{Colors.RESET}")
                    continue
                
                subcmd = parts[1]
                result = execute_command("auth", [subcmd])
                format_response(result)
            
            elif command == "/notebook":
                if len(parts) < 2:
                    print(f"{Colors.RED}Usage: /notebook <add|list|activate|ask> [args]{Colors.RESET}")
                    continue
                
                subcmd = parts[1]
                args = parts[2].split() if len(parts) > 2 else []
                
                result = execute_command(subcmd, args)
                format_response(result)
            
            else:
                print(f"{Colors.RED}Unknown command: {command}{Colors.RESET}")
                print(f"Type {Colors.BLUE}/help{Colors.RESET} for available commands")
            
            print()
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Use /exit to quit{Colors.RESET}")
        except EOFError:
            print(f"\n{Colors.YELLOW}Goodbye!{Colors.RESET}")
            break

if __name__ == "__main__":
    main()
