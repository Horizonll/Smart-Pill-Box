import qianfan
from dotenv import load_dotenv

load_dotenv()
if "__main__" == __name__:
    chat_comp = qianfan.ChatCompletion()
    chat_history = []

    while True:
        message = input("user: ")
        if message != "":
            try:
                chat_history.append({"role": "user", "content": message})
                resp = chat_comp.do(model="ERNIE-Lite-8K", messages=chat_history)
                print(f'\nassistant: {resp["body"]["result"]}\n')
                chat_history.append(
                    {"role": "assistant", "content": resp["body"]["result"]}
                )
            except:
                pass
