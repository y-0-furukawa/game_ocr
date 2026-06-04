import os
import sys
from PIL import ImageGrab
import pytesseract
import pyperclip
from deep_translator import GoogleTranslator

# =====================================================================
# 1. ポータブル版 Tesseract OCR のパス自動設定（5.5.0 最新版対応）
# =====================================================================
# スクリプトが置かれているフォルダの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# スクリプトと同じフォルダ内にある「Tesseract-OCR」フォルダ内の tesseract.exe を指定
TESSERACT_PATH = os.path.join(BASE_DIR, 'Tesseract-OCR', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# 【最新版対応】環境変数には 'tessdata' フォルダそのもののパスを直接指定する
os.environ['TESSDATA_PREFIX'] = os.path.join(BASE_DIR, 'Tesseract-OCR', 'tessdata')


# =====================================================================
# 2. メイン処理関数
# =====================================================================
def ocr_and_translate_from_clipboard():
    """
    クリップボードから画像を取得し、英語OCR処理、改行整形、および日本語翻訳を行う関数
    """
    print("動作環境を確認中...")
    if not os.path.exists(TESSERACT_PATH):
        print(f"【エラー】Tesseractの実行ファイルが見つかりません。")
        print(f"予想されるパス: {TESSERACT_PATH}")
        print("フォルダ配置が正しいか確認してください。")
        return

    print("クリップボードから画像を取得中...")
    # クリップボードから画像オブジェクトを取得
    img = ImageGrab.grabclipboard()
    
    if img is None:
        print("【エラー】クリップボードに画像データがありません。")
        print("画像をコピー（スクリーンショット等）した状態で再実行してください。")
        return
    
    print("OCR処理を実行中（言語設定: 英語のみ）...")
    try:
        # 言語を英語（eng）のみに指定してOCRを実行
        raw_text = pytesseract.image_to_string(img, lang='eng')
        raw_text = raw_text.strip()
    except Exception as e:
        print(f"【エラー】OCR処理中に問題が発生しました:\n{e}")
        print("\ntessdataフォルダ内に 5.x 用の 'eng.traineddata' が正しく配置されているか確認してください。")
        return
    
    if not raw_text:
        print("文字を検出できませんでした。")
        return
        
    # -----------------------------------------------------------------
    # 【新規追加】改行を半角スペースに変換する整形処理
    # -----------------------------------------------------------------
    # 1. まず連続する改行や前後の無駄な空白を整理
    # 2. 改行コード（\n）をすべて半角スペース（" "）に置換
    # 3. 単語の間に不要な二重スペース（"  "）ができた場合の対策として、1つのスペースに集約
    text = " ".join(raw_text.splitlines())
    # 念のため、前後に残った空白を再度トリミング
    text = text.strip()
        
    print("\n================== 抽出テキスト（英語・改行整形済） ==================")
    print(text)
    print("======================================================================\n")
    
    # 翻訳処理
    print("日本語に翻訳中...")
    try:
        # Google翻訳を利用して、整形済みの英文を日本語へ翻訳
        translated_text = GoogleTranslator(source='en', target='ja').translate(text)
        
        print("\n======================== 日本語翻訳結果 ========================")
        print(translated_text)
        print("================================================================\n")
        
        # 翻訳結果をクリップボードに書き戻す
        # pyperclip.copy(translated_text)
        # print("※ 翻訳結果の日本語テキストをクリップボードにコピーしました。")
        # print("任意の場所で Ctrl + V を押して貼り付けられます。")
        
    except Exception as e:
        print(f"【警告】翻訳エラーが発生しました: {e}")
        # 翻訳に失敗した場合は整形済みの英語をコピー
        pyperclip.copy(text)
        print("※ 翻訳に失敗したため、整形成分の英語テキストをクリップボードにコピーしました。")


# =====================================================================
# 3. エントリーポイント
# =====================================================================
if __name__ == "__main__":
    ocr_and_translate_from_clipboard()