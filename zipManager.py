import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import zipfile
import tkinter as tk
from tkinter import messagebox

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        
        if event.src_path.endswith('.zip'):
            self.ask_to_extract(event.src_path)

    def ask_to_extract(self, zip_path):
    
        root = tk.Tk()
        root.withdraw()  
        response = messagebox.askyesno("解凍確認", f"{zip_path}を解凍しますか？")
        
        if response: 
            self.extract_zip(zip_path)

        root.destroy()  

    def extract_zip(self, zip_path):
        try:
            folder_name = os.path.splitext(os.path.basename(zip_path))[0]
            extract_path = os.path.join(os.path.dirname(zip_path), folder_name)
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
        except zipfile.BadZipFile:
            messagebox.showerror("エラー", f"{zip_path}は無効なZIPファイルです。")
        except Exception as e:
            messagebox.showerror("エラー", f"解凍中にエラーが発生しました: {e}")

def monitor_download_folder(path):
    print(f"監視を開始します: {path}")
    before = dict([(f, None) for f in os.listdir(path)])
    while True:
        time.sleep(10)
        after = dict([(f, None) for f in os.listdir(path)])
        added = [f for f in after if not f in before]
        if added:
            for file in added:
                if file.endswith(".zip"):
                    print(f"新しいZIPファイルが検出されました: {os.path.join(path, file)}")
        before = after

if __name__ == "__main__":
    path = os.path.expanduser("~/Desktop") 
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            pass 
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
