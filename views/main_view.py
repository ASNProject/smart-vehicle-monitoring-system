import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import time

from controllers.detection_controller import DetectionController
from core.serial_reader import SerialReader


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SMART DETECTION")
        # self.geometry("800x800")
        # self.attributes("-fullscreen", True)

        self.attributes("-zoomed", True)
        self.configure(bg="#F5F6FA")

        self.controller = DetectionController()

        self.serial = SerialReader(
            port="/dev/serial0",
            baudrate=115200,
            callback=self.handle_serial_data
        )

        self.cam_label = Label(self, width=480, height=320, bg="black")
        # self.cam_label.pack(pady=10)
        self.cam_label.pack(pady=5, fill="both", expand=True)

        self.card_container = Frame(self, bg="#F5F6FA")
        # self.card_container.pack(pady=10, padx=20, fill="x")
        self.card_container.pack(pady=5, padx=10, fill="both", expand=True)

        self.card_container.grid_columnconfigure(0, weight=1)
        self.card_container.grid_columnconfigure(1, weight=1)
        self.card_container.grid_rowconfigure(0, weight=1)

        self.yolo_frame = Frame(self.card_container, bg="white", bd=1, relief="solid")
        self.yolo_frame.grid(row=0, column=0, padx=5, sticky="nsew")

        Label(self.yolo_frame,
              text="OBJEK TERDEKAT",
              font=("Arial", 12, "bold"),
              fg="#2E86DE",
              bg="white").pack(pady=5)

        self.object_label = Label(self.yolo_frame,
                                 text="-",
                                 font=("Arial", 16, "bold"),
                                 fg="#2E86DE",
                                 bg="white")
        self.object_label.pack()

        self.distance_label = Label(self.yolo_frame,
                                   text="-",
                                   font=("Arial", 12),
                                   fg="#2E86DE",
                                   bg="white")
        self.distance_label.pack(pady=5)

        self.gps_frame = Frame(self.card_container, bg="white", bd=1, relief="solid")
        self.gps_frame.grid(row=0, column=1, padx=5, sticky="nsew")

        Label(self.gps_frame,
              text="GPS DATA",
              font=("Arial", 12, "bold"),
              fg="#2E86DE",
              bg="white").pack(pady=5)

        self.gps_label = Label(self.gps_frame,
                              text="Menunggu data...",
                              font=("Arial", 10),
                              fg="#2E86DE",
                              bg="white",
                              justify=LEFT)
        self.gps_label.pack(pady=5)

        self.button_frame = Frame(self, bg="#F5F6FA")
        # self.button_frame.pack(pady=10)
        self.button_frame.pack(pady=5, fill="x")

        Button(self.button_frame,
               text="A",
               width=10,
               height=2,
               bg="#27AE60",
               fg="white",
               command=self.send_a).pack(side=LEFT, padx=10)

        Button(self.button_frame,
               text="B",
               width=10,
               height=2,
               bg="#2980B9",
               fg="white",
               command=self.send_b).pack(side=LEFT, padx=10)

        self.last_label = "-"
        self.last_distance = "-"

        self.last_send = 0

        # self.update_camera()

    # =========================
    def send_a(self):
        self.serial.send_raw("A")

    def send_b(self):
        self.serial.send_raw("B")

    # def update_camera(self):
    #     frame, info = self.controller.get_frame()
    #
    #     if frame is not None:
    #         # frame = cv2.resize(frame, (480, 320))
    #         width = self.cam_label.winfo_width()
    #         height = self.cam_label.winfo_height()
    #
    #         if width > 0 and height > 0:
    #             frame = cv2.resize(frame, (width, height))
    #
    #         img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         img = Image.fromarray(img)
    #         img = ImageTk.PhotoImage(img)
    #
    #         self.cam_label.imgtk = img
    #         self.cam_label.configure(image=img)
    #
    #         label = info.get("label")
    #         distance = info.get("distance")
    #
    #         if label is not None and distance is not None:
    #             self.last_label = label.upper()
    #             self.last_distance = f"{distance:.2f} meter"
    #
    #             # kirim serial (optional)
    #             if time.time() - self.last_send > 0.5:
    #                 self.serial.send({
    #                     "object": label,
    #                     "distance": round(distance, 2)
    #                 })
    #                 self.last_send = time.time()
    #
    #         # selalu tampilkan last value
    #         self.object_label.config(text=self.last_label)
    #         self.distance_label.config(text=self.last_distance)
    #
    #     self.after(30, self.update_camera)

    # =========================
    def handle_serial_data(self, data):
        if "lat" in data:
            text = (
                f"Lat   : {data['lat']}\n"
                f"Lon   : {data['lon']}\n"
                f"Sat   : {data['sat']}\n"
                f"Speed : {data['speed']}\n"
                f"Status: {data['status']}"
            )

            self.after(0, lambda: self.gps_label.config(text=text))