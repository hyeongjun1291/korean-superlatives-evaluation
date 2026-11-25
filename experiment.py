"""실험에 사용한 모델별 API 요청 설정."""
import json
import os
from urllib.request import Request, urlopen

ENDPOINTS = {
    "OpenAI": "https://api.openai.com/v1/chat/completions",
    "OpenRouter": "https://openrouter.ai/api/v1/chat/completions",
}
ROUTES = {
    "gpt-4o-2024-08-06": ("OpenAI", None),
    "gpt-5.2-2025-12-11": ("OpenAI", None),
    "gpt-6.1-terra": ("OpenAI", None),
    "meta-llama/llama-3.1-70b-instruct": ("OpenRouter", "amazon-bedrock"),
    "qwen/qwen-2.5-72b-instruct": ("OpenRouter", "deepinfra/fp8"),
    "upstage/solar-pro4": ("OpenRouter", "upstage"),
    "kt/midm-k-3.0-pro": ("OpenRouter", "kt"),
    "anthropic/claude-sonnet-4.5": ("OpenRouter", "anthropic"),
}


def request_body(model, messages):
    service, provider = ROUTES[model]
    body = {"model": model, "messages": messages, "temperature": 0}
    if service == "OpenAI":
        body.update(max_completion_tokens=32, top_p=1)
        if model == "gpt-6.1-terra":
            body.update(reasoning_effort="none", service_tier="flex", store=False)
        else:
            body.update(stream=False, n=1)
            if model.startswith("gpt-5.2"):
                body["reasoning_effort"] = "none"
        return body
    restriction = {"only": [provider], "allow_fallbacks": False, "require_parameters": True}
    body.update(max_tokens=32, provider=restriction)
    if provider == "anthropic":
        restriction["max_price"] = {"prompt": 3, "completion": 15}
    else:
        body["top_p"] = 1
        if provider == "kt":
            restriction["max_price"] = {"prompt": 0.2, "completion": 0.8}
        else:
            body["stream"] = False
        if provider in ("kt", "upstage"):
            body["reasoning"] = {"effort": "none"}
    return body


def send_one(body, *, timeout=90):
    """요청 한 건을 보내고 응답 JSON을 읽는다."""
    service = ROUTES[body["model"]][0]
    key_name = "OPENAI_API_KEY" if service == "OpenAI" else "OPENROUTER_API_KEY"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer "+os.environ[key_name]}
    request = Request(ENDPOINTS[service], data=json.dumps(body).encode(), headers=headers)
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)
