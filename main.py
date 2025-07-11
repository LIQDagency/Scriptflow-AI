from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# Simple HTML page for user input
html = """
<!DOCTYPE html>
<html>
<head>
    <title>ScriptFlow AI</title>
    <style>
        body { font-family: sans-serif; background-color: #111; color: white; padding: 2rem; }
        input, button { padding: 0.5rem; margin-top: 1rem; width: 100%; }
    </style>
</head>
<body>
    <h1>ScriptFlow AI 🎬</h1>
    <form method="POST">
        <label>Enter your idea:</label><br>
        <input type="text" name="prompt"><br>
        <button type="submit">Generate Script</button>
    </form>
    {% if result %}
        <h2>Generated Script:</h2>
        <p>{{ result }}</p>
    {% endif %}
</body>
</html>
"""

# Function to connect to OpenRouter API
def get_response_from_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://liqdagency.online",  # use your real domain or placeholder
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # or "anthropic/claude-3-sonnet" if you prefer Claude
        "messages": [
            {"role": "system", "content": "You are a short-form scriptwriting expert."},
            {"role": "user", "content": f"Write a short-form video script based on this idea: {prompt}"}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        result = get_response_from_openrouter(prompt)
    return render_template_string(html, result=result)

# Run the app on Render
if __name__ == "_main_":
    app.run(host="0.0.0.0", port=10000)
