import os
import time
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 设置设备ID为 CABLE Input（模拟麦克风）
virtual_mic_device_id = 18  # CABLE Input (VB-Audio Virtual Cable)

# 查看设备的采样率
device_info = sd.query_devices(virtual_mic_device_id)
device_sample_rate = device_info['default_samplerate']

# 定义 MP3 文件的路径
file_path = r"..\gptsovits-r-solution\response_audio.wav"

# 播放音频并打印成功信息
def play_audio(samples, sample_rate):
    try:
        sd.play(samples, samplerate=sample_rate, device=virtual_mic_device_id, blocking=True)
        print("音频已成功播放到虚拟麦克风！")  # 成功信息
    except Exception as e:
        print(f"播放音频时发生错误: {e}")  # 错误信息

# 监听 MP3 文件更新
class Mp3FileHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_modified_time = None
        self.is_playing = False  # 标志播放状态，避免重复播放

    def on_modified(self, event):
        if event.src_path == self.file_path and not self.is_playing:
            # 检查文件是否修改
            current_modified_time = os.path.getmtime(self.file_path)
            if self.last_modified_time != current_modified_time:
                self.last_modified_time = current_modified_time
                print(f"检测到文件 {self.file_path} 被更新，准备播放音频...")

                # 暂时停止监听文件更新
                self.is_playing = True

                # 增加延迟，确保文件已完成更新
                time.sleep(2)  # 等待 2 秒确保文件更新完成

                self.play_updated_audio()

    def play_updated_audio(self):
        try:
            # 加载 MP3 文件
            audio = AudioSegment.from_wav(self.file_path)

            # 打印调试信息
            print(f"加载的音频文件路径：{self.file_path}")
            print(f"音频采样率：{audio.frame_rate}")
            print(f"音频通道数：{audio.channels}")

            # 只调整采样率，与第一段代码一致
            if audio.frame_rate != device_sample_rate:
                audio = audio.set_frame_rate(int(device_sample_rate))

            # 转换为 numpy 数组
            samples = np.array(audio.get_array_of_samples())

            # 如果是立体声，转换成2列（左/右声道）
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))

            # 获取采样率
            sample_rate = audio.frame_rate

            # 播放音频
            play_audio(samples, sample_rate)

        except Exception as e:
            print(f"播放音频时发生错误: {e}")  # 错误信息
        finally:
            # 播放完成后，恢复文件监听
            self.is_playing = False


# 设置文件事件监听器
event_handler = Mp3FileHandler(file_path)
observer = Observer()
observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)

# 打印开始监听文件的提示信息
print("开始监听 MP3 文件更新...")

observer.start()

try:
    while True:
        time.sleep(1)  # 持续监听文件
except KeyboardInterrupt:
    observer.stop()
observer.join()
