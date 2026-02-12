import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import threading
import time

# --- デザイン設定 ---
ctk.set_appearance_mode("dark")
# カスタムテーマカラー（ネオンブルー系）
ctk.set_default_color_theme("blue")

# フォント設定
FONT_FAMILY = "Noto Sans JP Bold" # PCにインストールされている必要があります

class RichImageConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("画像変換 Pro - ローカル完結型")
        self.geometry("750x700")
        self.configure(fg_color="#0D1117") # 深いネイビーブラック

        self.input_paths = []

        # --- メインコンテナ ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(padx=40, pady=40, fill="both", expand=True)

        # --- タイトル ---
        self.title_label = ctk.CTkLabel(
            self.main_container, 
            text="画像変換 PRO", 
            font=(FONT_FAMILY, 32),
            text_color="#58A6FF"
        )
        self.title_label.pack(pady=(0, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_container, 
            text="サーバーへのアップロードなし。安全・軽量なローカル処理。", 
            font=(FONT_FAMILY, 14),
            text_color="#8B949E"
        )
        self.subtitle_label.pack(pady=(0, 30))

        # --- ファイル選択エリア（ホバーで光る！） ---
        self.drop_frame = ctk.CTkFrame(
            self.main_container, 
            height=160, 
            border_width=2, 
            border_color="#30363D",
            fg_color="#161B22"
        )
        self.drop_frame.pack(fill="x", pady=10)
        self.drop_frame.pack_propagate(False)

        # マウスホバー時のイベントをバインド
        self.drop_frame.bind("<Enter>", lambda e: self.on_hover(self.drop_frame, "#58A6FF"))
        self.drop_frame.bind("<Leave>", lambda e: self.on_leave(self.drop_frame, "#30363D"))

        self.btn_select = ctk.CTkButton(
            self.drop_frame, 
            text="ファイルを選択して追加", 
            font=(FONT_FAMILY, 16),
            fg_color="#238636",
            hover_color="#2EA043",
            height=45,
            command=self.select_files
        )
        self.btn_select.place(relx=0.5, rely=0.5, anchor="center")
        
        self.label_count = ctk.CTkLabel(self.main_container, text="選択中のファイル: 0件", font=(FONT_FAMILY, 13))
        self.label_count.pack(pady=5)

        # --- 設定セクション ---
        self.settings_grid = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.settings_grid.pack(fill="x", pady=20)

        # 左：リサイズ設定
        self.resize_group = self.create_glass_frame(self.settings_grid, "リサイズ設定")
        self.resize_group.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.resize_mode = ctk.StringVar(value="none")
        for text, val in [("変換なし", "none"), ("比率指定 (%)", "ratio"), ("固定サイズ (px)", "fixed")]:
            ctk.CTkRadioButton(self.resize_group, text=text, variable=self.resize_mode, value=val, font=(FONT_FAMILY, 13)).pack(anchor="w", pady=5, padx=20)
        
        self.entry_x = self.create_styled_entry(self.resize_group, "幅 / %")
        self.entry_y = self.create_styled_entry(self.resize_group, "高さ (固定時のみ)")

        # 右：保存設定
        self.output_group = self.create_glass_frame(self.settings_grid, "出力設定")
        self.output_group.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(self.output_group, text="一括リネーム（任意）", font=(FONT_FAMILY, 12)).pack(anchor="w", padx=20, pady=(0, 5))
        self.entry_prefix = self.create_styled_entry(self.output_group, "新しいファイル名を入力...")
        
        ctk.CTkLabel(self.output_group, text="変換フォーマット", font=(FONT_FAMILY, 12)).pack(anchor="w", padx=20, pady=(10, 5))
        self.format_var = ctk.StringVar(value="PNG")
        self.format_menu = ctk.CTkOptionMenu(
            self.output_group, 
            values=["PNG", "JPEG", "WEBP"], 
            variable=self.format_var,
            font=(FONT_FAMILY, 13),
            fg_color="#21262D",
            button_color="#30363D",
            button_hover_color="#58A6FF"
        )
        self.format_menu.pack(fill="x", padx=20, pady=(0, 20))

        # --- 進捗・実行 ---
        self.progress_bar = ctk.CTkProgressBar(self.main_container, height=12, progress_color="#58A6FF", fg_color="#30363D")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=20)

        self.btn_run = ctk.CTkButton(
            self.main_container, 
            text="一括変換を実行する", 
            font=(FONT_FAMILY, 18),
            height=60,
            fg_color="#1F6FEB", 
            hover_color="#388BFD",
            command=self.start_thread
        )
        self.btn_run.pack(fill="x")

    # --- ヘルパーメソッド（リッチな装飾用） ---
    def create_glass_frame(self, master, title):
        frame = ctk.CTkFrame(master, fg_color="#161B22", border_width=1, border_color="#30363D")
        ctk.CTkLabel(frame, text=title, font=(FONT_FAMILY, 14, "bold"), text_color="#58A6FF").pack(pady=15)
        # ホバーアニメーション
        frame.bind("<Enter>", lambda e: self.on_hover(frame, "#58A6FF"))
        frame.bind("<Leave>", lambda e: self.on_leave(frame, "#30363D"))
        return frame

    def create_styled_entry(self, master, placeholder):
        entry = ctk.CTkEntry(
            master, 
            placeholder_text=placeholder, 
            height=35, 
            fg_color="#0D1117", 
            border_color="#30363D",
            font=(FONT_FAMILY, 12)
        )
        entry.pack(fill="x", padx=20, pady=5)
        return entry

    def on_hover(self, widget, color):
        widget.configure(border_color=color)
        
    def on_leave(self, widget, color):
        widget.configure(border_color=color)

    # --- 処理ロジック ---
    def select_files(self):
        paths = filedialog.askopenfilenames(filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.webp *.bmp")])
        if paths:
            self.input_paths = paths
            self.label_count.configure(text=f"選択中のファイル: {len(self.input_paths)}件", text_color="#58A6FF")

    def start_thread(self):
        threading.Thread(target=self.process_images, daemon=True).start()

    def process_images(self):
        if not self.input_paths:
            messagebox.showwarning("注意", "ファイルを選択してください。")
            return

        save_dir = filedialog.askdirectory(title="保存先フォルダを選択")
        if not save_dir: return

        self.btn_run.configure(state="disabled", text="変換処理中...")
        
        try:
            total = len(self.input_paths)
            for i, path in enumerate(self.input_paths):
                self.progress_bar.set((i + 1) / total)
                
                img = Image.open(path)
                mode = self.resize_mode.get()
                
                if mode == "ratio":
                    ratio = float(self.entry_x.get()) / 100
                    img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
                elif mode == "fixed":
                    img = img.resize((int(self.entry_x.get()), int(self.entry_y.get())), Image.LANCZOS)

                fmt = self.format_var.get()
                prefix = self.entry_prefix.get()
                new_name = f"{prefix}_{i+1}.{fmt.lower()}" if prefix else os.path.splitext(os.path.basename(path))[0] + f".{fmt.lower()}"

                if fmt == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                img.save(os.path.join(save_dir, new_name), fmt)
                time.sleep(0.02)

            messagebox.showinfo("成功", f"{total}件の画像を変換しました。")
        except Exception as e:
            messagebox.showerror("エラー", f"失敗しました: {e}")
        finally:
            self.btn_run.configure(state="normal", text="一括変換を実行する")
            self.progress_bar.set(0)

if __name__ == "__main__":
    app = RichImageConverter()
    app.mainloop()