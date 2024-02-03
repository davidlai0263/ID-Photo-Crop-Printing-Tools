from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog

class GeneratorFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # 初始化變數
        self.image_size = None
        self.original_image = None

        # 標題容器
        title_frame = tk.Frame(self)
        title_frame.pack(side="top", fill="x")
        title_label = tk.Label(title_frame, text="Generator", font=("Arial", 18))
        title_label.pack()

        # 建立 Canvas 用於顯示圖片
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        # 建立打開圖片的按鈕
        self.open_button = tk.Button(self, text="打開圖片", command=self.open_image)
        self.open_button.pack()

        # 1寸照片
        self.one_inch_button = tk.Button(self, text="1寸照片", command=self.one_inch, state="disabled")
        self.one_inch_button.pack()

        # 2寸照片
        self.two_inch_button = tk.Button(self, text="2寸照片", command=self.two_inch, state="disabled")
        self.two_inch_button.pack()

    # 打開圖片
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # 讀取圖片
            image = Image.open(file_path)
            self.original_image = image.copy()
            resize_ratio = 500 / max(image.size)
            print(image.size)
            image.thumbnail((image.size[0] * resize_ratio, image.size[1] * resize_ratio))  # 調整圖片大小
            photo = ImageTk.PhotoImage(image)

            # 更新圖片
            self.canvas.image = photo
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)

            self.one_inch_button["state"] = "normal"
            self.two_inch_button["state"] = "normal"

    # 1寸照片
    def one_inch(self):
        self.image_size = (2.8, 3.5)
        self.generate_image()
    # 2寸照片
    def two_inch(self):
        self.image_size = (3.5, 4.5)
        self.generate_image()
    
    # 生成
    def generate_image(self):
        # 建立白色背景的圖片
        image_width = 15  # 單位：公分
        image_height = 10  # 單位：公分
        image_background_color = (255, 255, 255)  # 白色
        image_quality = 100  # 圖片品質

        image = Image.new('RGB', (int(image_width * image_quality), int(image_height * image_quality)), image_background_color)
        photo = self.original_image.copy()
        draw = ImageDraw.Draw(image)

        # 計算小圖的大小和間距
        gap = 0.1  # 單位：公分
        margin = 0.1  # 單位：公分

        # 計算小圖水平和垂直的數量
        num_horizontal = int((image_width - 2 * margin + gap) / (self.image_size[0] + gap))
        num_vertical = int((image_height - 2 * margin + gap) / (self.image_size[1] + gap))

        # 計算小圖的起始位置
        start_x = int(margin * image_quality)
        start_y = int(margin * image_quality)

        # 生成小圖填充到長方形
        for i in range(num_horizontal):
            for j in range(num_vertical):
                x = start_x + i * int((self.image_size[0] + gap) * image_quality)
                y = start_y + j * int((self.image_size[1] + gap) * image_quality)

                # 在(x, y)的位置畫一個黑色的框
                draw.rectangle([x-1, y-1, x + int(self.image_size[0] * image_quality)+1, y + int(self.image_size[1] * image_quality) +1], outline=(0, 0, 0))
                photo.thumbnail((int(self.image_size[0] * image_quality), int(self.image_size[1] * image_quality)))
                image.paste(photo, (x, y))
        # 顯示圖片
        image.show()
