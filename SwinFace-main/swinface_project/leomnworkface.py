import cv2
import numpy as np
import torch
import threading
import tkinter as tk
import time
from insightface.app import FaceAnalysis
from model import build_model  # 你已有的 SwinFace 结构定义

# ------------------ 1️⃣ 初始化 SwinFace --------------
class SwinFaceCfg:
    network = "swin_t"
    fam_kernel_size = 3
    fam_in_chans = 2112
    fam_conv_shared = False
    fam_conv_mode = "split"
    fam_channel_attention = "CBAM"
    fam_spatial_attention = None
    fam_pooling = "max"
    fam_la_num_list = [2 for _ in range(11)]
    fam_feature = "all"
    fam = "3x3_2112_F_s_C_N_max"
    embedding_size = 512

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cfg = SwinFaceCfg()
weight_path = "checkpoint_step_79999_gpu_0.pt"

def load_swinface_model():
    model = build_model(cfg)
    dict_checkpoint = torch.load(weight_path, map_location=device)
    model.backbone.load_state_dict(dict_checkpoint["state_dict_backbone"])
    model.fam.load_state_dict(dict_checkpoint["state_dict_fam"])
    model.tss.load_state_dict(dict_checkpoint["state_dict_tss"])
    model.om.load_state_dict(dict_checkpoint["state_dict_om"])
    model.to(device)
    model.eval()
    return model

swinface_model = load_swinface_model()

# ------------------ 2️⃣ 初始化人脸检测模型（InsightFace） --------------
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])  # 可改为 GPUExecutionProvider
face_app.prepare(ctx_id=0)

# ------------------ 3️⃣ Tkinter GUI 设置 --------------
root = tk.Tk()
root.title("Face Attributes")
root.geometry("400x500")

label_var = tk.StringVar()
label = tk.Label(root, textvariable=label_var, font=("Arial", 12), justify="left", anchor="w")
label.pack(padx=10, pady=10, fill="both")

def update_gui(text):
    label_var.set(text)

# ------------------ 4️⃣ 表情识别函数 ------------------
expression_labels = ["Surprise", "Fear", "Disgust", "Happiness", "Sadness", "Anger", "Neutral"]

@torch.no_grad()
def recognize_face(face_img):
    face_img = cv2.resize(face_img, (112, 112))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    face_img = np.transpose(face_img, (2, 0, 1))
    face_img = torch.from_numpy(face_img).unsqueeze(0).float()
    face_img = face_img.div(255).sub(0.5).div(0.5).to(device)
    output = swinface_model(face_img)
    return output["Expression"].cpu().numpy().squeeze()

# ------------------ 5️⃣ 空格键控制逻辑 ------------------
recognizing = False
start_time = None
expression_history = []
last_keypress_time = 0

def save_to_txt(top_2_expressions):
    with open("expression_result.txt", "w", encoding="utf-8") as f:
        f.write("用户在说这段话的时候最可能的表情是：\n")
        for expr, score in top_2_expressions:
            f.write(f"{expr}: {score}\n")

def handle_space_key():
    global recognizing, last_keypress_time, start_time, expression_history
    current_time = time.time()
    if current_time - last_keypress_time > 0.5:
        if not recognizing:
            recognizing = True
            start_time = current_time
            expression_history.clear()
            print("开始识别")
        else:
            recognizing = False
            print("结束识别")
            if expression_history:
                avg_expression_scores = np.mean(expression_history, axis=0)
                top_2 = avg_expression_scores.argsort()[-2:][::-1]
                top_2_expressions = [(expression_labels[i], round(float(avg_expression_scores[i]), 2)) for i in top_2]
                save_to_txt(top_2_expressions)
        last_keypress_time = current_time

# ------------------ 6️⃣ 摄像头线程 ------------------
def camera_thread(event):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open the camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord(" "):  # 空格键
            handle_space_key()

        # 人脸检测
        faces = face_app.get(frame)
        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)
            face_img = frame[y1:y2, x1:x2].copy()
            if recognizing:
                scores = recognize_face(face_img)
                expression_history.append(scores)

        cv2.imshow("Face Recognition", frame)

    cap.release()
    cv2.destroyAllWindows()
    event.set()

# ------------------ 7️⃣ 定时更新GUI ------------------
def periodic_gui_update():
    update_gui("正在识别中...\n" if recognizing else "请按空格键开始识别。\n")
    root.after(200, periodic_gui_update)

event = threading.Event()
threading.Thread(target=camera_thread, args=(event,), daemon=True).start()

periodic_gui_update()
root.mainloop()
