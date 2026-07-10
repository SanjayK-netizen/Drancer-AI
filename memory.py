import json
import os
from datetime import datetime

# ─────────────────────────────────────────
# DRANCER - Memory Module
# Stores user preferences and important facts
# Author: Sanjay.K
# ─────────────────────────────────────────

MEMORY_FILE = "drancer_memory.json"

DEFAULT_MEMORY = {
    "user_name": "Friend",
    "preferences": {},
    "important_facts": [],
    "last_updated": str(datetime.now()),
    "conversation_logs": []
}

def load_memory():
    """Load memory from file. Return default if doesn't exist."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading memory: {e}")
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(memory_data):
    """Save memory to file."""
    try:
        memory_data["last_updated"] = str(datetime.now())
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving memory: {e}")
        return False

def add_fact(fact, category="general"):
    """Add an important fact to memory."""
    memory = load_memory()
    
    if "important_facts" not in memory:
        memory["important_facts"] = []
    
    memory["important_facts"].append({
        "fact": fact,
        "category": category,
        "timestamp": str(datetime.now())
    })
    
    save_memory(memory)

def get_facts(category=None):
    """Get facts, optionally filtered by category."""
    memory = load_memory()
    facts = memory.get("important_facts", [])
    
    if category:
        facts = [f for f in facts if f.get("category") == category]
    
    return facts

def set_user_preference(key, value):
    """Store a user preference."""
    memory = load_memory()
    
    if "preferences" not in memory:
        memory["preferences"] = {}
    
    memory["preferences"][key] = value
    save_memory(memory)

def get_user_preference(key, default=None):
    """Retrieve a user preference."""
    memory = load_memory()
    preferences = memory.get("preferences", {})
    return preferences.get(key, default)

def set_user_name(name):
    """Store the user's name."""
    memory = load_memory()
    memory["user_name"] = name
    save_memory(memory)

def get_user_name():
    """Get the user's name."""
    memory = load_memory()
    return memory.get("user_name", "Friend")

def log_conversation(user_input, drancer_response):
    """Log conversation for history."""
    memory = load_memory()
    
    if "conversation_logs" not in memory:
        memory["conversation_logs"] = []
    
    # Keep only last 50 conversations to avoid huge files
    if len(memory["conversation_logs"]) > 50:
        memory["conversation_logs"] = memory["conversation_logs"][-50:]
    
    memory["conversation_logs"].append({
        "user": user_input,
        "drancer": drancer_response,
        "timestamp": str(datetime.now())
    })
    
    save_memory(memory)

def get_memory_context():
    """Get a summary of important memory for brain context."""
    memory = load_memory()
    user_name = memory.get("user_name", "Friend")
    facts = memory.get("important_facts", [])
    
    context = f"User's name: {user_name}. "
    if facts:
        context += "Important facts: " + "; ".join([f['fact'] for f in facts[:5]])
    
    return context

if __name__ == "__main__":
    # Test memory module
    print("Testing Drancer memory...")
    
    set_user_name("Sanjay")
    print(f"User name: {get_user_name()}")
    
    add_fact("I like coding", category="preferences")
    add_fact("I created Drancer", category="general")
    print(f"Facts: {get_facts()}")
    
    print("Memory system working!")
