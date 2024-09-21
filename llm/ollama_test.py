import json
import requests

MODEL = "qwen2:0.5b-instruct"
API_URL = "http://localhost:11434/api/generate"


def generate(prompt, context):
    try:
        response = requests.post(API_URL, json={"model": MODEL, "prompt": prompt, "context": context}, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"HTTP请求错误: {e}")
        return context

    for line in response.iter_lines():
        if line:
            try:
                body = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                continue

            response_part = body.get("response", "")
            print(response_part, end="", flush=True)

            if "error" in body:
                print(f"模型错误: {body['error']}")
                break

            if body.get("done", False):
                return body.get("context", context)
    return context


def main():
    context = []
    while True:
        user_input = input("Enter a prompt: ")
        if not user_input:
            print("退出程序.")
            break
        print("生成响应中...")
        context = generate(user_input, context)
        print("\n")


if __name__ == "__main__":
    main()
