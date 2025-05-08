# module main

import os
import requests
from datetime import datetime
from flask import Flask, request, jsonify, Response, stream_with_context

# init
app = Flask(__name__)
app.config['LLM_PROXY_KEY'] = os.getenv('LLM_PROXY_KEY')
app.config['LLM_PROXY_MODEL_NAME'] = os.getenv('LLM_PROXY_MODEL_NAME')


@app.route('/')
def service():
    return f'LLM Proxy is running {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}', 200


@app.route('/api/generate', methods=['POST'])
def llm_generate():
    # check for API key in the request
    data = request.get_json()
    if 'key' not in data or data['key'] != app.config['LLM_PROXY_KEY']:
        return jsonify({"error": "Invalid or missing API key"}), 401
    
    # remove key before forwarding to LLM
    data.pop("key", None)

    # check if client wants streaming
    stream = data.get("stream", True)
    
    # override model if specified
    if app.config['LLM_PROXY_MODEL_NAME']:
        data['model'] = app.config['LLM_PROXY_MODEL_NAME']
    
    # generate result
    try:
        if stream:
            def generate():
                with requests.post('http://localhost:11434/api/generate', json=data, stream=True) as r:
                    for line in r.iter_lines():
                        if line:
                            yield line + b'\n'  # send chunk to client
            return Response(stream_with_context(generate()), content_type='application/json')
        else:
            # non-streaming, just forward normally
            response = requests.post('http://localhost:11434/api/generate', json=data)
            return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to local LLM: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/api/chat', methods=['POST'])
def llm_chat():
    # check for API key in the request
    data = request.get_json()
    if 'key' not in data or data['key'] != app.config['LLM_PROXY_KEY']:
        return jsonify({"error": "Invalid or missing API key"}), 401
    
    # remove key before forwarding to LLM
    data.pop("key", None)
    
    # check if client wants streaming
    stream = data.get("stream", True)
    
    # override model if specified
    if app.config['LLM_PROXY_MODEL_NAME']:
        data['model'] = app.config['LLM_PROXY_MODEL_NAME']

    # generate result
    try:
        if stream:
            def generate():
                with requests.post('http://localhost:11434/api/chat', json=data, stream=True) as r:
                    for line in r.iter_lines():
                        if line:
                            yield line + b'\n'  # send chunk to client
            return Response(stream_with_context(generate()), content_type='application/json')
        else:
            # non-streaming, just forward normally
            response = requests.post('http://localhost:11434/api/chat', json=data)
            return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to local LLM: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004, debug=True)