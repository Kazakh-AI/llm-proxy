# Simple LLM Proxy
It receives request meant for LLMs with ollama API and checks if the user has access (rights) to use the model via `key`. It true, then the request is forwarded to the model, otherwise it refuses the request and returns an error.

### Run LLM proxy app
```sh
# clone the project
git clone https://github.com/Kazakh-AI/llm-proxy.git
cd llm-proxy

# install dependencies
python3 -m venv venv && source ./venv/bin/activate
pip install -r ./requirements.txt

# run app (debug)
# python3 src/main.py

# run app with gunicorn
export LLM_PROXY_KEY="your_key"
gunicorn -w 4 -b 0.0.0.0:8004 src.main:app

# run app in background with unicorn
# export LLM_PROXY_KEY="your_key"
# nohup gunicorn -w 4 -b 0.0.0.0:8004 src.main:app > llm-proxy.log 2>&1 &
```

### LLM requests
It's the same format as described in [ollama](https://github.com/ollama/ollama/blob/main/docs/api.md) documentation. There are only two differences:
1. Add content type headers
2. Add API `key`

#### Generate
```sh
curl http://localhost:8004/api/generate -H "Content-Type: application/json" -d '{
    "model": "model_name",
    "prompt": "Why is the sky blue?",
    "stream": false,
    "key": "your_key"
}'
```

Response:
```json
{
  "context": [151644, ..., 13],
  "created_at": "2025-04-13T05:12:23.851197499Z",
  "done": true,
  "done_reason": "stop",
  "eval_count": 210,
  "eval_duration": 3547572045,
  "load_duration": 26215612,
  "model": "model_name",
  "prompt_eval_count": 35,
  "prompt_eval_duration": 23103115,
  "response": "The sky appears blue because of refraction of light.\n\nLight travels through a medium (air or other gas) and bends around objects that lie in front of the light source. This bending of light can change its direction, but if it doesn't completely overlap with an object, we are looking at it as a constant angle of incidence, meaning our eye will see it as being blue.\n\nIn particular, blue represents all colors except red (the primary color of light) and yellow, which is also visible in the sky. Therefore, people use different names for each color: the color \"blue\" corresponds to red, and green or cyan is associated with yellow. These associations make up the language we have learned about color vision.\n\nThe blue color itself was a key element that artists used to depict the sky during prehistoric times because it can be represented as a color called \"ocean blue.\" However, it isn't entirely accurate to say that the sky has \"blue\" in it; it is actually an artificial creation of light and our perception.",
  "total_duration": 3597881148
}
```

#### Chat
```sh
curl http://localhost:8004/api/chat -H "Content-Type: application/json" -d '{
    "model": "model_name",
    "messages": [
        {                   
            "role": "user",
            "content": "why is the sky blue?"
        }
    ], 
    "stream": false,
    "key": "your_key"
}'
```

Response:
```json
{
    "created_at": "2025-04-13T05:22:57.150852886Z",
    "done": true,
    "done_reason": "stop",
    "eval_count": 203,
    "eval_duration": 2365577433,
    "load_duration": 700139280,
    "message": {
        "content": "The sky appears blue because of how our eyes interpret colors. When light hits an object, it bounces off and travels through your eye. Our eyes have sensors that pick up these reflected colors, and we can recognize certain colors as blue or green depending on what we are seeing.\n\nHowever, the Earth's atmosphere does play a role in this phenomenon too. As you move from lower altitudes toward higher altitudes, the air becomes cooler and denser, which causes more light to scatter and bend around the edges of our view. This means that if we are looking at blue objects or areas on the sky, they appear as a shade of blue, but when we look directly at them or those in front of us, it appears to be much darker.\n\nAdditionally, some types of weather patterns can also affect how colors appear on the sky, such as cumulus clouds (which are often grayish-green), cirrus clouds (which are white, fluffy and less dense), or rarer phenomena like rainbows.",
        "role": "assistant"
    },
    "model": "model_name",
    "prompt_eval_count": 35,
    "prompt_eval_duration": 74568969,
    "total_duration": 3143038800
}
```

#### Key error
```json
{
    "error": "Invalid or missing API key"
}
```


## LICENSE
All code is licensed under the MIT license. 

