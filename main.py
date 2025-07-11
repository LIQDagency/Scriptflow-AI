from flask import Flask, request, jsonify, render_template_string
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ['OPENROUTER_API_KEY']

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

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            base_url="https://openrouter.ai/api/v1",
            messages=[
                {"role": "system", "content": "You are a scriptwriting expert."},
                {"role": "user", "content": f"Write a short-form video script based on this idea: {prompt}"}
            ]
        )
        result = response['choices'][0]['message']['content']
    return render_template_string(html, result=result)

if _name_ == '_main_':
    app.run(host="0.0.0.0", port=10000)
