import ollama 
import re
from memory import get_memory_context, get_user_name, log_conversation

# ─────────────────────────────────────────
# DRANCER - Brain Module
# Model: phi3:mini (runs on 8GB RAM)
# Author: Sanjay.K
# ─────────────────────────────────────────

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
}

def get_system_prompt(language=None):
    """Generate system prompt with user-specific context from memory."""
    user_name = get_user_name()
    memory_context = get_memory_context()
    language_note = ""
    if language and language != "en" and language != "auto":
        language_name = LANGUAGE_NAMES.get(language, language)
        language_note = (
            f"\n9. The user is speaking in {language_name}. Reply in that same language naturally."
        )
    else:
        language_note = (
            "\n9. If the user asks in another language, reply in that same language naturally."
        )
    
    base_prompt = f"""You are Drancer, a personal AI assistant created by Sanjay.
You are talking to {user_name}.

**Your Personality:**
- Friendly, intelligent, and conversational
- Professional yet approachable
- Knowledgeable about coding, writing, and general topics
- Always respectful and helpful
- Remember things about {user_name} from previous conversations

**User Context:**
{memory_context}

**Guidelines:**
1. Keep responses concise and direct (2-4 sentences max for voice output)
2. Be conversational and natural - speak as if talking to a friend
3. For coding questions: provide brief explanations with examples
4. For general questions: give practical, useful answers
5. If unsure about something, be honest about it
6. Never claim to be an AI model from any company
7. You are Drancer, created by Sanjay - that's your identity
8. Feel free to reference past conversations if relevant
{language_note}

**Important for Voice Output:**
- Use short, punchy sentences
- Avoid unnecessary filler words
- Be clear and enunciation-friendly
- Break complex answers into smaller pieces"""
    
    return base_prompt

MAX_HISTORY_CONTEXT = 10  # Keep last 10 messages for context

def clean_response(text):
    """
    Clean response text to make it more natural for voice output.
    Removes artifacts and cleans up formatting.
    """
    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)      # Italic
    text = re.sub(r'`(.+?)`', r'\1', text)        # Inline code
    text = re.sub(r'#+\s', '', text)               # Headers
    
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def manage_history(history, max_items=MAX_HISTORY_CONTEXT):
    """
    Keep conversation history manageable by removing oldest messages
    when exceeding max_items to avoid context window overflow.
    """
    if len(history) > max_items:
        return history[-max_items:]
    return history

def ask(prompt, history=None, language=None):
    """
    Send a prompt to phi3:mini and get a response.
    
    Args:
        prompt: User's question or statement
        history: List of previous messages for context
        language: Optional language code of the user's input
    
    Returns:
        String response from Drancer
    """
    # Ensure default history does not persist across calls
    if history is None:
        history = []

    # Manage conversation history to avoid context overflow
    history = manage_history(history)
    
    # Get dynamic system prompt with user context
    system_prompt = get_system_prompt(language)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    if language and language != "en" and language != "auto":
        language_name = LANGUAGE_NAMES.get(language, language)
        messages.append({
            "role": "system",
            "content": (
                f"The user's input is in {language_name}. Reply in that same language "
                "unless explicitly asked to switch to another language."
            )
        })
    
    # Add conversation history
    messages += history
    
    # Add current user message
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=messages,
            stream=False,
            options={
                "temperature": 0.7,      # Balanced creativity and coherence
                "top_p": 0.9,            # Focus on likely tokens
                "top_k": 40,             # Limit token choices
                "num_predict": 150,      # Limit response length (voice-friendly)
            }
        )
        
        reply = response['message']['content']
        # Clean and prepare response for voice
        reply = clean_response(reply)
        
        # Log conversation for memory
        try:
            log_conversation(prompt, reply)
        except Exception as e:
            pass  # Silently fail if logging fails
        
        return reply
    
    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}. Please make sure Ollama is running."
        return error_msg


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