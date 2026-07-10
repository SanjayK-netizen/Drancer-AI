import ollama 

# ─────────────────────────────────────────
# JARVIS - Brain Module
# Model: phi3:mini (runs on 8GB RAM)
# Author: Sanjay.K
# ─────────────────────────────────────────

SYSTEM_PROMPT = """You are Drancer, a personal AI assistant created by Sanjay.
Your job is to assist with writing, coding, and general questions.
Be concise, direct, and helpful.
Never say you are an AI model made by Microsoft or any company.
You are Drancer, created by Sanjay."""

def ask(prompt, history=[]):
    """
    Send a prompt to phi3:mini and get a response.
    history = list of previous messages for context
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add conversation history
    messages += history
    
    # Add current user message
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=messages
        )
        return response['message']['content']
    
    except Exception as e:
        return f"Error contacting Ollama: {str(e)}. Make sure Ollama is running."


def test_brain():
    """Quick test to verify brain is working."""
    print("Testing Drancer brain...")
    response = ask("Say: Drancer online and ready.")
    print(f"Drancer: {response}")


# ─────────────────────────────────────────
# Run this file directly to test
# python brain.py
# ─────────────────────────────────────────
if __name__ == "__main__":
    test_brain()