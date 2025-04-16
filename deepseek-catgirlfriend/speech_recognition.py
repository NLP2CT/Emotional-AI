from gradio_client import Client, handle_file

# 设置Gradio客户端
client = Client("http://127.0.0.1:7860/")  # 假设Gradio应用在本地运行

def speech_to_text(audio_path):
    try:
        print(f"正在进行语音识别，音频路径: {audio_path}")
        # 调用Gradio的API进行语音识别
        result = client.predict(
            input_wav=handle_file(audio_path),
            language="auto",  # 使用自动语言检测
            api_name="/model_inference"    # 使用模型推理API
        )
        print(f"识别结果: {result}")
        return result
    except Exception as e:
        print(f"语音识别过程中出现错误: {e}")
        return ""
