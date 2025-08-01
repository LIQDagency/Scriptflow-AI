document.getElementById("result").innerHTML = formatScript(data.script);
function formatScript(script) {
    // Convert double new lines into paragraph breaks
    const paragraphs = script.split('\n\n').map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`);
    return paragraphs.join('');
}

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
