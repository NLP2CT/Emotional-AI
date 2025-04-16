import time
import os
from audio_recorder import record_audio
from speech_recognition import speech_to_text
from conversation import clean_text, interact_with_deepseek  

# 表情结果文件的路径
expression_result_path = "../SwinFace-main/expression_result.txt"

# 读取文本文件内容
def read_expression_result():
    try:
        with open(expression_result_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content:
                print("警告: 表情结果文件为空")
            return content
    except Exception as e:
        print(f"读取表情文件时出错: {e}")
        return None

# 检测文件是否更新
def file_updated(last_modified_time):
    try:
        current_modified_time = os.path.getmtime(expression_result_path)
        if current_modified_time > last_modified_time:
            return True
        else:
            print("文件未更新")
            return False
    except Exception as e:
        print(f"检查文件更新时出错: {e}")
        return False

def main():
    try:
        print("开始录音，按下空格键开始录音，按下空格键结束录音并进行识别...")

        messages = []  
        messages.append({   
            "role": "system",    
            "content": "你是用户的青梅竹马，喜欢像雌小鬼一样调戏用户，但是时不时也会认真开导用户，请留意用户的信息中有关情感的表达，例如，这样的格式<|zh|><|Natural|><|Speech|><|withitn|>这里面zh代表中文，natural代表情感平和，剩下两个参数说明是再室内发表的讲话，"
            "有时候我会直接传递用户的情感给你，请留意并对用户做出相应的安抚和回复，在你回复的文本里面不要包括特殊字符，标点符号只需要基础的逗号，句号，叹号，问号，只是中文文本即可，无需增加动作描述，只是返回像是青梅竹马说的话即可"
        })

        # 初始化文件最后修改时间
        last_modified_time = os.path.getmtime(expression_result_path)  # 获取文件初始的修改时间

        while True:  
            # 录音和语音识别  
            audio_path = record_audio(duration=30, fs=16000)
            text = speech_to_text(audio_path)  
            cleaned_text = clean_text(text)
            print(f"识别结果: {cleaned_text}")           
        
            messages.append({"role": "user", "content": cleaned_text})

            # 等待2秒再检测文件更新
            time.sleep(2)

            # 检查表情文件是否更新
            if file_updated(last_modified_time):
                expression_content = read_expression_result()
                if expression_content:
                    # 如果文件更新了，添加到消息中
                    print("检测到文件更新，添加表情结果到消息...")
                    messages.append({"role": "system", "content": f"最新表情识别结果:\n{expression_content}"})
                    last_modified_time = os.path.getmtime(expression_result_path)  # 更新文件时间
                else:
                    print("没有读取到表情识别结果或文件内容为空")
                    continue  # 继续等待下次循环

            # 进行 DeepSeek API 交互
            messages = interact_with_deepseek(messages)

            print("当前对话历史：")  
            for message in messages:    
                print(f"{message['role']}: {message['content']}")

    except Exception as e:
        print(f"程序运行中出现错误: {e}")

if __name__ == "__main__":  
    main()  
  