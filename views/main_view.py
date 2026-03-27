# Copyright 2025 ariefsetyonugroho
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk
from tkinter import *

import cv2

from core import config
from controllers.detection_controller import DetectionController
from core.utils import center_window
from PIL import Image, ImageTk


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.configure(bg=config.THEME_COLOR)

        self.controller = DetectionController()

        center_window(self)

        # MAIN FRAME
        self.main_frame = Frame(self, bg=config.THEME_COLOR)
        self.main_frame.pack(fill=BOTH, expand=True)

        # TOP FRAME
        self.top_frame = Frame(self.main_frame, bg=config.THEME_COLOR)
        self.top_frame.pack(side=TOP, fill=X)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)

        # Kamera 1 (Kiri)
        self.cam1_label = Label(self.top_frame)
        self.cam1_label.grid(row=0, column=0, padx=10, pady=10)

        # Kamera 2 (Kanan)
        self.cam2_label = Label(self.top_frame)
        self.cam2_label.grid(row=0, column=1, padx=10, pady=10)

        # BOTTOM FRAME (INFO)
        self.bottom_frame = Frame(self.main_frame, bg=config.THEME_COLOR)
        self.bottom_frame.pack(side=TOP, fill=X, anchor="n")

        Label(self.bottom_frame, text="INFO",
              fg="black",
              bg=config.THEME_COLOR,
              font=("Arial", 16, "bold")).pack(pady=5)

        self.info_frame = Frame(self.bottom_frame, bg=config.THEME_COLOR)
        self.info_frame.pack(anchor="n")

        self.info_left = Label(self.info_frame,
                               text="",
                               justify=LEFT,
                               anchor="n",  # 🔥 ini penting
                               fg="black",
                               bg=config.THEME_COLOR,
                               font=("Arial", 12))
        self.info_left.grid(row=0, column=0, padx=20, sticky="n")

        self.info_right = Label(self.info_frame,
                                text="",
                                justify=LEFT,
                                anchor="n",  # 🔥 ini penting
                                fg="black",
                                bg=config.THEME_COLOR,
                                font=("Arial", 12))
        self.info_right.grid(row=0, column=1, padx=20, sticky="n")

        self.update_camera()

        self.cam1_label = Label(self.top_frame, width=320, height=240, bg="black")
        self.cam1_label.grid(row=0, column=0, padx=10, pady=10)

        self.cam2_label = Label(self.top_frame, width=320, height=240, bg="black")
        self.cam2_label.grid(row=0, column=1, padx=10, pady=10)

    def update_camera(self):
        frame1, frame2, info1, info2 = self.controller.get_frames()

        if frame1 is not None:
            frame1 = cv2.resize(frame1, (320, 240))  # ✅ FIX ukuran
            img1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(img1)
            img1 = ImageTk.PhotoImage(img1)

            self.cam1_label.imgtk = img1
            self.cam1_label.configure(image=img1)

        if frame2 is not None:
            frame2 = cv2.resize(frame2, (320, 240))  # ✅ HARUS SAMA
            img2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(img2)
            img2 = ImageTk.PhotoImage(img2)

            self.cam2_label.imgtk = img2
            self.cam2_label.configure(image=img2)

            # CAMERA 1
            lines1 = []
            for i, d in enumerate(info1["car_distances"], start=1):
                lines1.append(f"Mobil {i} Jarak {d:.1f} m")

            for i, d in enumerate(info1["motor_distances"], start=1):
                lines1.append(f"Motor {i} Jarak {d:.1f} m")

            # CAMERA 2
            lines2 = []
            for i, d in enumerate(info2["car_distances"], start=1):
                lines2.append(f"Mobil {i} Jarak {d:.1f} m")

            for i, d in enumerate(info2["motor_distances"], start=1):
                lines2.append(f"Motor {i} Jarak {d:.1f} m")

            # tampilkan
            self.info_left.config(
                text="\n".join(lines1) if lines1 else "Tidak ada kendaraan"
            )

            self.info_right.config(
                text="\n".join(lines2) if lines2 else "Tidak ada kendaraan"
            )

        self.after(10, self.update_camera)

