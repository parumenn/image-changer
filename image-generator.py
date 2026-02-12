import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("画像形式変換ツール")
        self.geometry("400x300")

        # 選択されたファイルのパスを保持
        self.input_path = ""

        # UIの配置
        self.label = ctk.CTkLabel(self, text="画像ファイルを選択してください", font=("Heading", 16))
        self.label.pack(pady=20)

        self.select_button = ctk.CTkButton(self, text="ファイルを開く", command=self.select_file)
        self.select_button.pack(pady=10)

        self.format_label = ctk.CTkLabel(self, text="変換後の形式を選択:")
        self.format_label.pack(pady=5)
        
        self.format_var = ctk.StringVar(value="PNG")
        self.format_menu = ctk.CTkOptionMenu(self, values=["PNG", "JPEG", "WEBP", "BMP"], variable=self.format_var)
        self.format_menu.pack(pady=10)

        self.convert_button = ctk.CTkButton(self, text="変換して保存", command=self.convert_image, fg_color="green", hover_color="darkgreen")
        self.convert_button.pack(pady=20)

    def select_file(self):
        self.input_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.bmp")])
        if self.input_path:
            self.label.configure(text=f"選択中: {os.path.basename(self.input_path)}")

    def convert_image(self):
        if not self.input_path:
            messagebox.showwarning("警告", "先に画像ファイルを選択してください。")
            return

        # 保存先の選択
        output_format = self.format_var.get()
        save_path = filedialog.asksaveasfilename(defaultextension=f".{output_format.lower()}",
                                                 filetypes=[(f"{output_format} files", f"*.{output_format.lower()}")])
        
        if save_path:
            try:
                img = Image.open(self.input_path)
                # JPEGの場合、透過(RGBA)をRGBに変換
                if output_format == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                img.save(save_path, output_format)
                messagebox.showinfo("成功", f"変換が完了しました！\n{save_path}")
            except Exception as e:
                messagebox.showerror("エラー", f"変換に失敗しました: {e}")

if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()