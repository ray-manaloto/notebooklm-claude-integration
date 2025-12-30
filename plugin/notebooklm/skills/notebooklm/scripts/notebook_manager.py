#!/usr/bin/env python3
"""
Notebook Manager for NotebookLM
Handles notebook library operations: add, list, activate, search.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path(__file__).parent.parent / "data"
LIBRARY_FILE = DATA_DIR / "library.json"

def load_library() -> Dict:
    """Load the notebook library"""
    if not LIBRARY_FILE.exists():
        return {"notebooks": []}
    
    with open(LIBRARY_FILE) as f:
        return json.load(f)

def save_library(library: Dict):
    """Save the notebook library"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LIBRARY_FILE, 'w') as f:
        json.dump(library, f, indent=2)

def add_notebook(url: str, name: str = None, description: str = None, topics: List[str] = None):
    """Add a notebook to the library"""
    
    # Extract notebook ID from URL
    if "/notebook/" in url:
        notebook_id = url.split("/notebook/")[-1].split("?")[0]
    else:
        return {
            "success": False,
            "error": "Invalid NotebookLM URL. Expected format: https://notebooklm.google.com/notebook/ID"
        }
    
    library = load_library()
    
    # Check if already exists
    existing = [nb for nb in library["notebooks"] if nb["id"] == notebook_id]
    if existing:
        return {
            "success": False,
            "error": f"Notebook {notebook_id} already in library",
            "existing": existing[0]
        }
    
    # MOCK: Simulate discovering notebook content
    # Real implementation would use browser automation to read notebook metadata
    
    notebook = {
        "id": notebook_id,
        "url": url,
        "name": name or f"Notebook {notebook_id[:8]}",
        "description": description or "Auto-discovered notebook",
        "topics": topics or ["general"],
        "sources_count": 5,  # Mock data
        "added_date": "2025-12-29T22:40:00Z",
        "last_accessed": None,
        "active": False,
        "note": "MOCK DATA - Real implementation would discover actual content"
    }
    
    library["notebooks"].append(notebook)
    save_library(library)
    
    return {
        "success": True,
        "message": f"Added notebook: {notebook['name']}",
        "notebook": notebook
    }

def list_notebooks():
    """List all notebooks in the library"""
    library = load_library()
    
    if not library["notebooks"]:
        return {
            "success": True,
            "notebooks": [],
            "count": 0,
            "message": "No notebooks in library. Add one with: add <url>"
        }
    
    return {
        "success": True,
        "notebooks": library["notebooks"],
        "count": len(library["notebooks"]),
        "active": [nb for nb in library["notebooks"] if nb.get("active")]
    }

def activate_notebook(identifier: str):
    """Activate a notebook by ID or name"""
    library = load_library()
    
    # Deactivate all first
    for nb in library["notebooks"]:
        nb["active"] = False
    
    # Find and activate
    found = None
    for nb in library["notebooks"]:
        if identifier in [nb["id"], nb["name"]]:
            nb["active"] = True
            nb["last_accessed"] = "2025-12-29T22:40:00Z"
            found = nb
            break
    
    if not found:
        return {
            "success": False,
            "error": f"Notebook not found: {identifier}",
            "available": [nb["name"] for nb in library["notebooks"]]
        }
    
    save_library(library)
    
    return {
        "success": True,
        "message": f"Activated notebook: {found['name']}",
        "notebook": found
    }

def search_notebooks(topic: str):
    """Search notebooks by topic"""
    library = load_library()
    
    matches = []
    topic_lower = topic.lower()
    
    for nb in library["notebooks"]:
        # Search in name, description, and topics
        if (topic_lower in nb["name"].lower() or
            topic_lower in nb["description"].lower() or
            any(topic_lower in t.lower() for t in nb["topics"])):
            matches.append(nb)
    
    return {
        "success": True,
        "matches": matches,
        "count": len(matches),
        "query": topic
    }

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        result = list_notebooks()
    else:
        command = sys.argv[1]
        
        if command == "add":
            if len(sys.argv) < 3:
                result = {
                    "success": False,
                    "error": "URL required",
                    "usage": "notebook_manager.py add <url> [name] [description] [topic1,topic2]"
                }
            else:
                url = sys.argv[2]
                name = sys.argv[3] if len(sys.argv) > 3 else None
                description = sys.argv[4] if len(sys.argv) > 4 else None
                topics = sys.argv[5].split(',') if len(sys.argv) > 5 else None
                result = add_notebook(url, name, description, topics)
        
        elif command == "list":
            result = list_notebooks()
        
        elif command == "activate":
            if len(sys.argv) < 3:
                result = {
                    "success": False,
                    "error": "Notebook identifier required",
                    "usage": "notebook_manager.py activate <id_or_name>"
                }
            else:
                result = activate_notebook(sys.argv[2])
        
        elif command == "search":
            if len(sys.argv) < 3:
                result = {
                    "success": False,
                    "error": "Search topic required",
                    "usage": "notebook_manager.py search <topic>"
                }
            else:
                result = search_notebooks(sys.argv[2])
        
        else:
            result = {
                "success": False,
                "error": f"Unknown command: {command}",
                "available_commands": ["add", "list", "activate", "search"]
            }
    
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)

if __name__ == "__main__":
    main()
