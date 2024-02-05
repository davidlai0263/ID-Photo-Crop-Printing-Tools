from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

class CropperFrame(tk.Frame):
    def __init__(self, parent, controller, generator_frame_instance):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.generator_frame_instance = generator_frame_instance

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
        self.crop_and_gen = False

        # 標題容器
        # title_frame = tk.Frame(self)
        # title_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        # title_label = tk.Label(title_frame, text="Cropper", font=("Arial", 18))
        # title_label.pack()


        title_label = tk.Label(self, text=self._t("cropper", "title"), font=("Arial", 18))
        title_label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # 建立 Canvas 用於顯示圖片
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

        # 建立打開圖片的按鈕
        file_title = tk.Label(self, text=self._t("cropper", "file_title"))
        file_title.grid(row=2, column=0, sticky="nsew")
        open_button = tk.Button(self, text=self._t("cropper", "open_file"), command=self.open_image)
        open_button.grid(row=2, column=1)

        # 建立裁切圖片的按鈕
        self.crop_button = tk.Button(self, text=self._t("cropper", "crop"), command=self.crop_image, state="disabled")
        self.crop_button.grid(row=2, column=2)
        self.gen_checkbox = tk.Checkbutton(self, text=self._t("cropper", "gen_print"), command=self.change_gen_state, state="disabled")
        self.gen_checkbox.grid(row=2, column=3, sticky="nsew")

        size_title = tk.Label(self, text=self._t("cropper", "size_title"))
        size_title.grid(row=3, column=0, sticky="nsew")
        # 1寸照片
        self.one_inch_button = tk.Button(self, text=self._t("cropper", "one_inch"), command=self.one_inch, state="disabled")
        self.one_inch_button.grid(row=3, column=1)

        # 2寸照片
        self.two_inch_button = tk.Button(self, text=self._t("cropper", "two_inch"), command=self.two_inch, state="disabled")
        self.two_inch_button.grid(row=3, column=2)

        # Debug
        debug_button = tk.Button(self, text="Debug", command=self.debug)
        # debug_button.grid(row=4, column=0)

        # 監聽滑鼠事件
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)

        # 設定行和列的權重
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

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
            # print(self.image.size)
            self.image.thumbnail((self.image.size[0] * self.resize_ratio, self.image.size[1] * self.resize_ratio))  # 調整圖片大小
            self.photo = ImageTk.PhotoImage(self.image)

            # 更新圖片
            self.canvas.image = self.photo
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.one_inch_button["state"] = "normal"
            self.two_inch_button["state"] = "normal"
            self.crop_button["state"] = "normal"
            self.gen_checkbox["state"] = "normal"

            # 繪製紅框
            self.draw_red_box()

    def draw_red_box(self):
        # 若紅框、輔助線存在則刪除
        if self.red_box:
            self.canvas.delete("red_box")
            self.red_box = None
        if self.guild_line:
            self.canvas.delete("guildline")
            self.guild_line = None
        
        # 裁切尺寸設定
        box_width = self.crop_size[0]
        box_height = self.crop_size[1]
        box_ratio = box_width / box_height

        # 計算紅框邊緣貼齊哪軸
        # 若圖片寬高比大於紅框寬高比，則紅框貼齊圖片寬
        if self.canvas.image.width() / self.canvas.image.height() > box_ratio:
            box_height = self.canvas.image.height()
            box_width = box_height * box_ratio
        # 若圖片寬高比小於紅框寬高比，則紅框貼齊圖片高
        else:
            box_width = self.canvas.image.width()
            box_height = box_width / box_ratio

        # 計算紅框的位置
        box_x = (self.canvas.image.width() - box_width) / 2
        box_y = (self.canvas.image.height() - box_height) / 2  

        self.red_box = self.canvas.create_rectangle(
            box_x, box_y,
            box_x + box_width, box_y + box_height,
            outline="red", width=3, tags="red_box"
        )

        if self.crop_size == (3.5, 4.5):
            self.guild_line = self.canvas.create_rectangle(
                box_x + 5, box_y + box_height * 0.06,
                box_x - 5 + box_width, box_y + box_height * 0.86,
                outline="blue", width=2, tags="guildline")

    def crop_image(self):
        box_coords = self.canvas.coords(self.red_box)
        box_x, box_y, box_x2, box_y2 = [coord / self.resize_ratio for coord in box_coords]

        # 裁切圖片
        self.cropped_image = self.original_image.crop((box_x, box_y, box_x2, box_y2))

        # 顯示裁切後的圖片
        self.cropped_image.show()

        if self.crop_and_gen:
            self.generator_frame_instance.outer_set_original_image(self.cropped_image)
            self.generator_frame_instance.outer_generate_image(self.crop_size)
            self.controller.show_frame("Generator")

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

        # 縮放功能
        if self.cursor_in_resize_area:
            delta_x = event.x - box_x2
            box_x2 = box_x2 + delta_x

            new_width = box_x2 - box_x
            new_height = new_width / (self.crop_size[0] / self.crop_size[1])
            box_y2 = box_y + new_height

            if box_x2 > self.canvas.image.width():
                box_x2 = self.canvas.image.width()
                box_y2 = box_y + (box_x2 - box_x) / (self.crop_size[0] / self.crop_size[1])
            if box_y2 > self.canvas.image.height():
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
            if self.guild_line:
                self.canvas.delete("guildline")
                self.guild_line = self.canvas.create_rectangle(
                    box_x + 5, box_y + (box_y2 - box_y) * 0.06,
                    box_x2 - 5, box_y + (box_y2 - box_y) * 0.86,
                    outline="blue", width=2, tags="guildline")
        
        # 移動功能
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

            # 移動輔助線
            if self.canvas.find_withtag("guildline"):
                self.canvas.move(self.guild_line, delta_x, delta_y)

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
    def change_gen_state(self):
        self.crop_and_gen = not self.crop_and_gen

    def _t(self, section, key):
        return self.controller.localeUtil.translate(section, key)


if __name__ == "__main__":
    root = tk.Tk()
    app = CropperFrame(root, root, None)
    app.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
