from flask import Flask, jsonify, request, render_template_string
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
    <h2>✨ Content Pack Generated:</h2>
    <div style="white-space: pre-wrap; background: #222; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        {{ result }}
    </div>
{% endif %}
</body>
</html>
"""

# Function to connect to OpenRouter API
def get_response_from_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://liqdagency.online",  # or your site or a placeholder
        "Content-Type": "application/json"
    }

    data = {
    "model": "anthropic/claude-3-sonnet",
    "messages": [
        {"role": "system", "content": "You are a short-form content strategist."},
        {"role": "user", "content": f"""
Given this idea: "{prompt}"

Write:
1. Three scroll-stopping hooks (for short-form videos)
2. A powerful script (30-60 seconds)
3. Three viral captions optimized for IG Reels, TikTok, and YT Shorts

Format:
Hooks:
- ...
- ...
- ...

Script:
[Script content here]

Captions:
- ...
- ...
- ...
"""}
    ]
}

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print("🔍 Full API Response (raw):", response.status_code, response.text)

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ 'choices' key not found. Full response: {result}"

    except Exception as e:
        return f"❌ Error talking to OpenRouter: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        result = get_response_from_openrouter(prompt)
    return render_template_string(html, result=result)

# Run the app on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
