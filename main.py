from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

def get_response_from_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://liqdagency.online",  # Use your real or temporary domain
        "Content-Type": "application/json"
    }

    data = {
        "model": "anthropic/claude-3-sonnet",  # Or your preferred model
        "messages": [
            {"role": "system", "content": "You are a short-form scriptwriting expert."},
            {"role": "user", "content": f"Write a short-form video script based on this idea: {prompt}"}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ Error: {result}"
    except Exception as e:
        return f"❌ Parsing Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        result = get_response_from_openrouter(prompt)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
