document.getElementById('generateBtn').addEventListener('click', async () => {
    const topic = document.getElementById('topic').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic })
    });

    const data = await response.json();
    document.getElementById('output').textContent = data.script;
});
