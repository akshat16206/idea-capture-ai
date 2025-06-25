from flask import Flask, send_from_directory, Response, jsonify, request
import subprocess
import json
import os

app = Flask(__name__)

# Serve index.html from current directory
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Run the run.sh script and stream output to client
@app.route('/capture')
def capture():
    def generate():
        process = subprocess.Popen(['bash', 'run.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            yield f"data: {line.strip()}\n\n"
    return Response(generate(), mimetype='text/event-stream')

# Search ideas.json
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []

    try:
        with open('ideas.json', 'r') as f:
            ideas = json.load(f)

        if isinstance(ideas, list):
            for idea in ideas:
                if query in idea.get('raw', '').lower() or query in idea.get('summary', '').lower():
                    results.append(idea)
        else:
            results.append({'raw': 'Error: ideas.json is not a list', 'summary': '', 'timestamp': ''})

    except FileNotFoundError:
        results.append({'raw': 'ideas.json file not found', 'summary': '', 'timestamp': ''})
    except json.JSONDecodeError:
        results.append({'raw': 'ideas.json is corrupted or empty', 'summary': '', 'timestamp': ''})

    return jsonify(results)

# Serve JS or CSS if needed
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
