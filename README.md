# 🖼️ 画像形式コンバーター

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Build: Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#)
[![Style: CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-eb6134?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)

> **"今時WEBツールとしてたくさんありますが、サイト上にアップロードしたくないときがあるのでWindowsローカルで動く画像ファイル変換ソフトとして軽量なものを用意してみました"**

---

## ▼ Key Features

本ツールは、プライバシーを重視するユーザーのために開発された、完全ローカル動作の画像処理アプリケーションです。

* **・ 高速一括変換**: 複数ファイルをドラッグ&ドロップ（選択）して一瞬で変換。
* **・ 柔軟なリサイズ**:
    * 固定ピクセル指定（Width x Height）
    * パーセント指定による一括拡大・縮小
* **・ スマートリネーム**: 独自の接頭辞＋連番（例: `yukino_photo_1.png`）への自動リネーム。
* **・ モダンなUI**: `CustomTkinter` を採用し、Windows 11に馴染むダークモード対応のデザイン。
* **・ プライバシー保護**: クラウドに画像をアップロードせず、すべての処理をあなたのPC内（ローカル）で完結。

---

## ▼ Screenshots

| メイン画面 | 処理実行イメージ |
|:---:|:---:|
| <img src="https://via.placeholder.com/400x300.png?text=Main+GUI+Image" width="400"> | <img src="https://via.placeholder.com/400x300.png?text=Processing+Image" width="400"> |

---

## ▼ Installation & Usage

### 1. 実行ファイルで使用する場合 (.exe)
`dist/converter_pro.exe` をダウンロードして実行してください。インストールは不要です。

### 2. ソースコードから実行する場合
```bash
# リポジトリをクローン
git clone [https://github.com/parumenn/image-changer]

# 必要ライブラリのインストール
pip install customtkinter Pillow

# 実行
python converter_pro.py
