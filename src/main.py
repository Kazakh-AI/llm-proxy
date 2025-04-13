# module main

import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response, stream_with_context

# load dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../'))

# init
app = Flask(__name__)
app.config['PROXY_KEY'] = os.getenv('PROXY_KEY')


@app.route('/')
def service():
    return f'LLM Proxy is running {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}', 200


@app.route('/api/generate', methods=['POST'])
def llm_generate():
    # check for API key in the request
    data = request.get_json()
    if 'key' not in data or data['key'] != app.config['PROXY_KEY']:
        return jsonify({"error": "Invalid or missing API key"}), 401
    
    # remove key before forwarding to LLM
    data.pop("key", None)

    # check if client wants streaming
    stream = data.get("stream", True)
    
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
    if 'key' not in data or data['key'] != app.config['PROXY_KEY']:
        return jsonify({"error": "Invalid or missing API key"}), 401
    
    # remove key before forwarding to LLM
    data.pop("key", None)
    
    # check if client wants streaming
    stream = data.get("stream", True)
    
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


# @app.route('/api/chat', methods=['POST'])
# def llm_chat():
#     # check for API key in the request
#     data = request.get_json()
#     if 'key' not in data or data['key'] != app.config['PROXY_KEY']:
#         return jsonify({"error": "Invalid or missing API key"}), 401
    
#     # remove key before forwarding to LLM
#     data.pop("key", None)
    
#     # check if client wants streaming
#     stream = data.get("stream", True)
    
#     # generate result
#     try:
#         # remove the key from the data before forwarding to LLM
#         data.pop('key', None)
#         data['stream'] = False

#         # forward the request to the local LLM
#         response = requests.post('http://localhost:11434/api/chat', json=data)
        
#         # return the LLM's response
#         return jsonify(response.json()), response.status_code 
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": f"Failed to connect to local LLM: {str(e)}"}), 502
#     except Exception as e:
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004, debug=True)