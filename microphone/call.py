import os
import time
import subprocess

file_path = r"..\gptsovits-r-solution\response_audio.wav"
last_modified_time = None

def check_file_update():
    global last_modified_time
    # 获取文件的最后修改时间
    current_modified_time = os.path.getmtime(file_path)
    
    # 如果文件的修改时间发生变化，则执行脚本
    if last_modified_time is None:
        last_modified_time = current_modified_time
        return False
    if current_modified_time > last_modified_time:
        last_modified_time = current_modified_time
        return True
    return False

print("监听中")
while True:
    if check_file_update():
        # 如果文件已更新，运行 vtubertxts.py 脚本
        subprocess.run(['python', 'vtubertxts.py'])
    
    # 每隔一段时间检查一次文件是否更新（这里设置为 5 秒）
    time.sleep(5)
