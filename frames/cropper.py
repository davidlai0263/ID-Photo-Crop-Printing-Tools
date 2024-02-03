from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

class CropperFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # 初始化變數
        self.original_image = None
        self.image = None
        self.cropped_image = None
        self.resize_ratio = None  # 圖片縮放比例
        self.red_box = None
        self.guild_line = None
        self.crop_size = (3.5, 4.5)
        self.drag_data = {"x": 0, "y": 0}
        self.cursor_in_resize_area = False

        # 標題容器
        title_frame = tk.Frame(self)
        title_frame.pack(side="top", fill="x")
        title_label = tk.Label(title_frame, text="Cropper", font=("Arial", 18))
        title_label.pack()

        # 建立 Canvas 用於顯示圖片
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        # 建立打開圖片的按鈕
        self.open_button = tk.Button(self, text="打開圖片", command=self.open_image)
        self.open_button.pack()

        # 建立裁切圖片的按鈕
        self.crop_button = tk.Button(self, text="裁切圖片", command=self.crop_image)
        self.crop_button.pack()

        # 1寸照片
        self.one_inch_button = tk.Button(self, text="1寸照片", command=self.one_inch)
        self.one_inch_button.pack()

        # 2寸照片
        self.two_inch_button = tk.Button(self, text="2寸照片", command=self.two_inch)
        self.two_inch_button.pack()

        # Debug
        self.debug_button = tk.Button(self, text="Debug", command=self.debug)
        self.debug_button.pack()

        # 監聽滑鼠事件
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)

    def one_inch(self):
        self.crop_size = (2.8, 3.5)
        self.draw_red_box()

    def two_inch(self):
        self.crop_size = (3.5, 4.5)
        self.draw_red_box()

    def debug(self):
        print(self.canvas.coords(self.red_box))

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # 讀取圖片
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            self.resize_ratio = 500 / max(self.image.size)
            print(self.image.size)
            self.image.thumbnail((self.image.size[0] * self.resize_ratio, self.image.size[1] * self.resize_ratio))  # 調整圖片大小
            self.photo = ImageTk.PhotoImage(self.image)

            # 更新圖片
            self.canvas.image = self.photo
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # 繪製紅框
            self.draw_red_box()

    def draw_red_box(self):
        if self.red_box:
            self.canvas.delete("red_box")
        box_width = self.crop_size[0]
        box_height = self.crop_size[1]
        box_ratio = box_width / box_height

        if self.canvas.image.width() / self.canvas.image.height() > box_ratio:
            box_height = self.canvas.image.height()
            box_width = box_height * box_ratio
        else:
            box_width = self.canvas.image.width()
            box_height = box_width / box_ratio

        box_x = (self.canvas.image.width() - box_width) / 2
        box_y = (self.canvas.image.height() - box_height) / 2

        self.red_box = self.canvas.create_rectangle(
            box_x, box_y,
            box_x + box_width, box_y + box_height,
            outline="red", width=3, tags="red_box"
        )

    def crop_image(self):
        box_coords = self.canvas.coords(self.red_box)
        box_x, box_y, box_x2, box_y2 = [coord / self.resize_ratio for coord in box_coords]

        # 裁切圖片
        self.cropped_image = self.original_image.crop((box_x, box_y, box_x2, box_y2))

        # 顯示裁切後的圖片
        self.cropped_image.show()

    def on_press(self, event):
        if not self.image:
            return
        # 紀錄點擊位置和被點擊的物件
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.update_cursor(event)

    def on_drag(self, event):
        if not self.image:
            return
        box_coords = self.canvas.coords(self.red_box)
        box_x, box_y, box_x2, box_y2 = box_coords
        if self.cursor_in_resize_area:
            delta_x = event.x - box_x2
            box_x2 = box_x2 + delta_x

            new_width = box_x2 - box_x
            new_height = new_width / (self.crop_size[0] / self.crop_size[1])
            box_y2 = box_y + new_height

            if box_x2 > self.canvas.image.width():
                box_x2 = self.canvas.image.width()
                box_y2 = box_y + (box_x2 - box_x) / (self.crop_size[0] / self.crop_size[1])
            elif box_y2 > self.canvas.image.height():
                box_y2 = self.canvas.image.height()
                box_x2 = box_x + (box_y2 - box_y) / (self.crop_size[1] / self.crop_size[0])

            self.canvas.delete("red_box")

            self.red_box = self.canvas.create_rectangle(
                box_x, box_y,
                box_x2, box_y2,
                outline="red", width=3, tags="red_box"
            )
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
        else:
            # 移動紅框
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            if box_x + delta_x < 0:
                delta_x = box_x * -1
            elif box_x2 + delta_x > self.canvas.image.width():
                delta_x = self.canvas.image.width() - box_x2
            if box_y + delta_y < 0:
                delta_y = box_y * -1
            elif box_y2 + delta_y > self.canvas.image.height():
                delta_y = self.canvas.image.height() - box_y2

            self.canvas.move(self.red_box, delta_x, delta_y)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_release(self, event):
        # 清空被點擊的物件
        pass

    def on_motion(self, event):
        # 更新游標形狀
        if not self.image:
            return
        self.update_cursor(event)

    def update_cursor(self, event):
        # 檢查游標是否在紅框邊緣範圍內
        cursor_x, cursor_y = event.x, event.y
        box_coords = self.canvas.coords(self.red_box)
        box_x, box_y, box_x2, box_y2 = box_coords

        resize_area_width = 10  # 定義邊緣範圍寬度

        if (
            (box_x - resize_area_width <= cursor_x <= box_x + resize_area_width) or
            (box_x2 - resize_area_width <= cursor_x <= box_x2 + resize_area_width)
        ) and (
            box_y - resize_area_width <= cursor_y <= box_y2 + resize_area_width
        ):
            # 游標在紅框邊緣範圍內
            self.controller.config(cursor="sb_h_double_arrow")
            self.cursor_in_resize_area = True
        else:
            # 游標在其他區域
            self.controller.config(cursor="")
            self.cursor_in_resize_area = False


if __name__ == "__main__":
    root = tk.Tk()
    app = CropperFrame(root, root)
    app.pack()
    root.mainloop()
