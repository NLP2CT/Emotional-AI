import re
# from chattts1 import text_to_speech
def clean_text(text):
    return text

from openai import OpenAI
import time
client = OpenAI(api_key="sk-b52a7645be8f40458de02539255b8be4", base_url="https://api.deepseek.com")
import traceback

import re
# from chattts1 import text_to_speech
import traceback

def interact_with_deepseek(messages):
    try:
        # 调用 DeepSeek API 获取模型的回答
        print("调用 DeepSeek API 获取模型的回答...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        # 提取模型的回答
        assistant_reply1 = response.choices[0].message.content  # 获取助手的回答内容
        assistant_reply2 = response.choices[0].message.content  # 获取助手的回答内容
        print(f"DeepSeek Assistant: {assistant_reply1}")

        # 将助手的回复按正确格式加入消息历史
        messages.append({"role": "assistant", "content": assistant_reply1})

        # 将 assistant_reply2 保存到当前目录的 txt 文件中
        try:
            with open("assistant_reply2.txt", "w", encoding="utf-8") as file:
                file.write(assistant_reply2)
            print(f"assistant_reply2 已保存为 assistant_reply2.txt")
        except Exception as e:
            print(f"保存文本时出错: {e}")
            traceback.print_exc()

        # 生成语音并保存为 MP3 文件（注释掉的代码保持原样）
        # output_path = "response_test/response_2.mp3"
        # try:
        #     print(f"准备生成语音：{assistant_reply2}")
        #     text_to_speech(assistant_reply2, output_path)  # 调用语音生成函数
        #     print(f"音频保存成功: {output_path}")
        # except Exception as e:
        #     print(f"音频生成时出错: {e}")
        #     traceback.print_exc()  

        return messages
    except Exception as e:
        print(f"DeepSeek API交互出错: {e}")
        traceback.print_exc()  # 打印详细错误信息
        return messages
