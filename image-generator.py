import flet as ft
from PIL import Image
import os
import threading
import time

# --- ロジック担当：画像変換関数 ---
def convert_image_logic(input_path, output_dir, mode, val_x, val_y, prefix, fmt, index):
    img = Image.open(input_path)
    
    # リサイズ
    if mode == "ratio" and val_x:
        ratio = float(val_x) / 100
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    elif mode == "fixed" and val_x and val_y:
        img = img.resize((int(val_x), int(val_y)), Image.LANCZOS)

    # リネーム
    if prefix:
        new_name = f"{prefix}_{index+1}.{fmt.lower()}"
    else:
        new_name = os.path.splitext(os.path.basename(input_path))[0] + f".{fmt.lower()}"

    # 保存
    if fmt == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    img.save(os.path.join(output_dir, new_name), fmt)

def main(page: ft.Page):
    # --- ページ基本設定 ---
    page.title = "Image Convert Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1100
    page.window_height = 850
    page.fonts = {"NotoSansJP": "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf"}
    page.theme = ft.Theme(font_family="NotoSansJP")
    
    selected_files_paths = []

    # --- UI要素の定義 ---
    file_list_view = ft.ListView(expand=1, spacing=10, padding=20)
    
    # 設定入力項目
    resize_dropdown = ft.Dropdown(
        label="リサイズモード",
        value="none",
        options=[
            ft.dropdown.Option("none", "変換なし"),
            ft.dropdown.Option("ratio", "比率指定 (%)"),
            ft.dropdown.Option("fixed", "固定サイズ (px)"),
        ],
        width=300
    )
    
    width_input = ft.TextField(label="幅 / %", width=145, border_color=ft.colors.BLUE_400)
    height_input = ft.TextField(label="高さ (固定時)", width=145, border_color=ft.colors.BLUE_400)
    prefix_input = ft.TextField(label="一括リネーム（接頭辞）", hint_text="例: yukino_photo", width=300)
    format_dropdown = ft.Dropdown(
        label="出力形式",
        value="PNG",
        options=[ft.dropdown.Option("PNG"), ft.dropdown.Option("JPEG"), ft.dropdown.Option("WEBP")],
        width=300
    )

    progress_bar = ft.ProgressBar(width=600, value=0, color=ft.colors.BLUE_400, bgcolor=ft.colors.BLUE_GREY_900)
    progress_status = ft.Text("待機中...")

    # --- イベントハンドラ ---
    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                selected_files_paths.append(f.path)
                file_list_view.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.icons.IMAGE_OUTLINED, color=ft.colors.BLUE_400),
                                title=ft.Text(f.name, weight="bold"),
                                subtitle=ft.Text(f"{round(f.size/1024, 1)} KB"),
                            ),
                            padding=5
                        ),
                        elevation=2,
                        animate_scale=ft.animation.Animation(300, "decelerate"),
                    )
                )
            page.update()

    file_picker = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(file_picker)

    def start_conversion(e):
        if not selected_files_paths:
            page.snack_bar = ft.SnackBar(ft.Text("ファイルを選択してください"))
            page.snack_bar.open = True
            page.update()
            return
        
        # 保存先選択（簡易的にカレントディレクトリまたは固定パスにする例が多いですが、Fletのget_directory_pathを使用）
        def on_dir_result(e: ft.FilePickerResultEvent):
            if e.path:
                output_dir = e.path
                run_convert(output_dir)
        
        dir_picker = ft.FilePicker(on_result=on_dir_result)
        page.overlay.append(dir_picker)
        page.update()
        dir_picker.get_directory_path()

    def run_convert(output_dir):
        total = len(selected_files_paths)
        for i, path in enumerate(selected_files_paths):
            progress_status.value = f"処理中: {i+1}/{total}"
            progress_bar.value = (i + 1) / total
            page.update()
            
            convert_image_logic(
                path, output_dir, resize_dropdown.value, 
                width_input.value, height_input.value, 
                prefix_input.value, format_dropdown.value, i
            )
            time.sleep(0.1)
        
        progress_status.value = "すべての変換が完了しました！"
        page.snack_bar = ft.SnackBar(ft.Text("変換完了！"), bgcolor=ft.colors.GREEN_700)
        page.snack_bar.open = True
        page.update()

    # --- レイアウト構築 ---
    page.add(
        ft.Row(
            [
                # サイドバー（設定）
                ft.Container(
                    content=ft.Column([
                        ft.Text("設定", size=24, weight="bold"),
                        ft.Divider(),
                        resize_dropdown,
                        ft.Row([width_input, height_input], spacing=10),
                        prefix_input,
                        format_dropdown,
                        ft.VerticalDivider(height=20),
                        ft.ElevatedButton(
                            "ファイルを選択", 
                            icon=ft.icons.ADD_PHOTO_ALTERNATE, 
                            on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        ),
                    ], spacing=20),
                    width=350,
                    padding=30,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                # メインエリア（リストと実行）
                ft.Container(
                    content=ft.Column([
                        ft.Text("画像変換 PRO (Next Gen)", size=32, weight="bold", color=ft.colors.BLUE_400),
                        ft.Text("ローカル処理でプライバシーを守ります", color=ft.colors.GREY_500),
                        ft.Container(
                            content=file_list_view,
                            expand=True,
                            border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
                            border_radius=15,
                        ),
                        ft.Container(
                            content=ft.Column([
                                progress_status,
                                progress_bar,
                                ft.FilledButton(
                                    "一括変換を実行", 
                                    icon=ft.icons.PLAY_ARROW_ROUNDED,
                                    width=600,
                                    height=50,
                                    on_click=start_conversion
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20
                        )
                    ], expand=True),
                    expand=True,
                    padding=30
                )
            ],
            expand=True,
            spacing=0
        )
    )

ft.app(target=main)