from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Connect to OpenRouter
def get_response_from_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://liqdagency.online",
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
        print("🔍 API response:", response.status_code, response.text)

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ 'choices' key not found. Full response: {result}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        result = get_response_from_openrouter(prompt)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
