import tkinter as tk
from tkinter import ttk
from frames.cropper import CropperFrame
from frames.generator import GeneratorFrame

class HomePage(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("PhotoUtils")  # 直接调用title方法

        # 頁面切換按鈕框架
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x")

        # 主容器
        container = tk.Frame(self, bd=3, relief="groove")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # functions = [
        #     (CropperFrame, "Cropper"),
        #     (GeneratorFrame, "Generator")
        # ]

        self.frames = {}

        # for F, page_name in functions:
        #     frame = F(container, self)
        #     self.frames[page_name] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")

        generator_frame = GeneratorFrame(container, self)
        generator_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Generator"] = generator_frame
        cropper_frame = CropperFrame(container, self, generator_frame)
        cropper_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Cropper"] = cropper_frame
        
        # 頁面切換按鈕
        # for f in functions:
        #     button = ttk.Button(button_frame, text=f[1], command=lambda name=f[1]: self.show_frame(name))
        #     button.pack(side="left", padx=5)
        cropper_button = ttk.Button(button_frame, text="Cropper", command=lambda: self.show_frame("Cropper"))
        cropper_button.pack(side="left", padx=5)
        generator_button = ttk.Button(button_frame, text="Generator", command=lambda: self.show_frame("Generator"))
        generator_button.pack(side="left", padx=5)

        self.show_frame("Cropper")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

app = HomePage()
# app.geometry("400x300")
app.mainloop()
