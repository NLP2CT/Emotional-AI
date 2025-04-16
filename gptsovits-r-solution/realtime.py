import os
import time  # 导入 time 模块
import shutil  # 导入 shutil 用于文件移动
from gradio_client import Client, handle_file  # 导入 handle_file 替代 file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pydub import AudioSegment  # 用于转换音频格式

# 获取当前程序的工作目录
current_dir = os.getcwd()

# 创建一个 Gradio 客户端实例，指向你的 Gradio API 地址
client = Client("http://localhost:9872/")  # 根据你的 Gradio API 地址修改

# 参考音频路径
ref_audio_path = r"token.wav"

# 使用 handle_file 来传递参考音频路径
ref_audio_file = handle_file(ref_audio_path)

# 固定的音频文件路径 (我们只创建一个音频文件，不使用时间戳)
output_path = os.path.join(current_dir, "response_audio.wav")  # 固定音频文件名
backup_path = os.path.join(current_dir, "response_audio_backup.wav")


# 监听文件更新并生成语音
class TxtFileHandler(FileSystemEventHandler):
    def __init__(self, txt_file_path):
        self.txt_file_path = txt_file_path
        self.last_modified_time = None

    def on_modified(self, event):
        event_rel_path = os.path.relpath(event.src_path)
        print(event_rel_path)

        if event_rel_path == self.txt_file_path:
            # 检查文件是否修改
            current_modified_time = os.path.getmtime(self.txt_file_path)
            if self.last_modified_time != current_modified_time:
                self.last_modified_time = current_modified_time
                print("检测到文件发生变化")
                # 读取文件内容
                with open(self.txt_file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                print("新的回复:" + text)

                if text:  # 如果文件不为空
                    # 调用 Gradio API 生成语音

                    result = client.predict(
                        ref_wav_path=ref_audio_file,  # 使用 handle_file 返回的 FileData 对象
                        #sovits_path="SoVITS_weights_v3/chun_e2_s192_l32.pth",
                        prompt_text="出格的事？相反，这段时间我可是有好好保护你，替你清除各种暗中的障碍哦！",
                        prompt_language="中文",  # 参考音频的语言
                        text=text,  # 需要合成的文本
                        text_language="中文",  # 生成语音的语言
                        how_to_cut="凑四句一切",  # 合成时的切分方式
                        top_k=15,
                        top_p=1,
                        temperature=1,
                        ref_free=False,
                        speed=1,
                        if_freeze=True,
                        inp_refs=None,
                        sample_steps=32,
                        if_sr=False,
                        pause_second=0.3,
                        api_name="/get_tts_wav"  # API 名称
                    )

                    # 打印完整的 result 返回值
                    print(f"Result: {result}")

                    # 确保 result 是有效的文件路径，如果是路径则打印文件路径
                    if isinstance(result, str) and result.endswith('.wav'):
                        # 移动临时文件到固定的音频路径
                        shutil.copy(result, output_path)
                        shutil.move(result, backup_path)
                        print(f"生成的语音文件路径: {output_path}")

                        # 使用 pydub 转换为 mp3 格式
                        wav_audio = AudioSegment.from_wav(output_path)
                        mp3_output_path = output_path.replace(".wav", ".mp3")
                        wav_audio.export(mp3_output_path, format="mp3")
                        print(f"生成的 MP3 文件路径: {mp3_output_path}")

                        # 删除临时的 wav 文件
                        #os.remove(output_path)

                    else:
                        print("生成音频失败，未返回有效路径。")


# 监听文件的路径
txt_file_path = r"..\deepseek-catgirlfriend\assistant_reply2.txt"

# 设置文件事件监听器
event_handler = TxtFileHandler(txt_file_path)
observer = Observer()
observer.schedule(event_handler, path=os.path.dirname(txt_file_path), recursive=False)

# 打印开始监听文件的提示信息
print("开始监听文件更新...")

observer.start()

try:
    while True:
        time.sleep(1)  # 持续监听文件
except KeyboardInterrupt:
    observer.stop()
observer.join()
