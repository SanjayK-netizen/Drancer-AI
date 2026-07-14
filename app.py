py

from flask import Flask, request, jsonify, render_template_string
import os
# Import existing core functions (Assuming they are in the same package or path)
# Adjust import path if needed; here we mock the imports for illustration.
try:
    from brain import ask, listen
except ImportError:
    # Placeholder functions if import fails in this environment.
    def ask(prompt, history=None, language=None):
        return f"Echo: {prompt}"
    def listen():
        return "transcript placeholder"
app = Flask(__name__)
# Load the HTML page from the artifact file (same directory)
HTML_PATH = os.path.join(os.path.dirname(__file__), "Webpage.html")
with open(HTML_PATH, "r", encoding="utf-8") as f:
    HTML_CONTENT = f.read()
@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)
@app.route('/ask', methods=['POST'])
def api_ask():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    response = ask(message)
    return jsonify({"response": response})
@app.route('/listen', methods=['POST'])
def api_listen():
    # Capture microphone input via existing listen(), then pass transcript to ask()
    transcript = listen()
    response = ask(transcript)
    return jsonify({"transcript": transcript, "response": response})
if __name__ == '__main__':
    # Run on localhost, port 5000
    app.run(host='127.0.0.1', port=5000, debug=False)