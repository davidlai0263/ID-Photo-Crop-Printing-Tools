import tkinter as tk
from tkinter import ttk
from frames.cropper import CropperFrame
from frames.generator import GeneratorFrame
from locales.locale import Locale
from settings import Settings

class HomePage(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 初始化變數
        self.settings = Settings()
        self.localeUtil = Locale(self.settings.get("language"))
        self.title(self._t("homepage", "title"))

        # 頁面切換按鈕框架
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x")

        # 主容器
        container = tk.Frame(self, bd=3, relief="groove")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # 頁面
        self.frames = {}
        generator_frame = GeneratorFrame(container, self)
        generator_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Generator"] = generator_frame
        cropper_frame = CropperFrame(container, self, generator_frame)
        cropper_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Cropper"] = cropper_frame
        
        # 頁面切換按鈕
        self.btn_cropper = ttk.Button(button_frame, text=self._t("homepage", "btn_cropper"), command=lambda: self.show_frame("Cropper"))
        self.btn_cropper.pack(side="left", padx=5)
        self.btn_generator = ttk.Button(button_frame, text=self._t("homepage", "btn_generator"), command=lambda: self.show_frame("Generator"))
        self.btn_generator.pack(side="left", padx=5)
        locale_selector = ttk.Combobox(button_frame, values=["zh-TW", "en"], state="readonly", width=5)
        locale_selector.current(locale_selector["values"].index(self.settings.get("language")))
        locale_selector.pack(side="right", padx=5)
        locale_selector.bind("<<ComboboxSelected>>", self.on_locale_change)
        

        self.show_frame("Cropper")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    def on_locale_change(self, event):
        result = tk.messagebox.askquestion(
            self._t("app", "msg_change_lang_title"),
            self._t("app", "msg_change_lang_content"),
        )
        if result != "yes":
            event.widget.set(self.settings.get("language"))
            return
        self.settings.set("language", event.widget.get())

        self.destroy()
        self.__init__()

    def _t(self, section, key):
        return self.localeUtil.translate(section, key)

app = HomePage()
app.mainloop()
