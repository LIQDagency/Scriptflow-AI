from flask import Flask, request, render_template
import requests
import os

app = Flask(_name_, static_folder="static", template_folder="templates")

def get_response_from_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://liqdagency.online",
        "Content-Type": "application/json"
    }

    data = {
        "model": "anthropic/claude-3-sonnet",
        "messages": [
            {"role": "system", "content": "You are a short-form scriptwriting expert."},
            {"role": "user", "content": f"Write a hook, caption, and script based on this idea: {prompt}"}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return "⚠️ Something went wrong. Please try again later."

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        result = get_response_from_openrouter(prompt)
    return render_template("index.html", result=result)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
