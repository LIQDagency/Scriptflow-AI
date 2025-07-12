from flask import Flask, jsonify, request, render_template_string
import requests
import os

app = Flask(_name_)

# Simple HTML page for user input
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ScriptFlow AI 🎬</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 2rem;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(145deg, #0d0d0d, #1a1a1a);
            color: #f2f2f2;
        }

        h1 {
            text-align: center;
            font-size: 2.5rem;
            color: #00FFF0;
            margin-bottom: 1rem;
        }

        form {
            max-width: 600px;
            margin: 0 auto;
            background-color: #1c1c1c;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 255, 240, 0.1);
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }

        input[type="text"] {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border-radius: 6px;
            border: none;
            background-color: #2b2b2b;
            color: #fff;
        }

        button {
            width: 100%;
            padding: 0.75rem;
            background-color: #00FFF0;
            color: #000;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #00ddd0;
        }

        .result-box {
            max-width: 600px;
            margin: 2rem auto;
            background-color: #262626;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 255, 240, 0.05);
        }

        .section-title {
            color: #00FFF0;
            margin-bottom: 0.5rem;
        }

        @media (max-width: 600px) {
            body { padding: 1rem; }
            form, .result-box { padding: 1rem; }
        }
    </style>
</head>
<body>
    <h1>ScriptFlow AI 🎬</h1>
    <form method="POST">
        <label for="prompt">💡 Enter your idea:</label>
        <input type="text" id="prompt" name="prompt" required>
        <button type="submit">🚀 Generate Script</button>
    </form>

    {% if result %}
    <div class="result-box">
        <h2 class="section-title">📝 Generated Script:</h2>
        <p>{{ result }}</p>
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
    "max_tokens": 1000,
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
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
