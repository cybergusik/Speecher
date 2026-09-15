import tkinter as tk
from tkinter import ttk, font, filedialog

import platform
from screeninfo import get_monitors
from datetime import datetime

import threading
from pathlib import Path
import hashlib

import backend


class Utils:
    def __init__(self):
        system = platform.system()

        home = Path.home()

        if system == "Darwin":
            self.cache_path = home / "Library" / "Caches" / "Speecher"
        elif system == "Linux":
            self.cache_path = home / ".cache"  / "Speecher"
        elif system == "Windows":
            self.cache_path = home / "AppData" / "Local" / "Speecher"
        else:
            self.cache_path = Path(__file__).resolve().parent / ".cache"

        self.tmp_path = self.cache_path / "tmp"
        self.res_path = self.cache_path / "res"

        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.tmp_path.mkdir(parents=True, exist_ok=True)
        self.res_path.mkdir(parents=True, exist_ok=True)


    def calculate_geometry(self, width: int, height: int):
        monitor = get_monitors()[0]
        x = (monitor.width // 2) - (width // 2)
        y = (monitor.height // 2) - (height // 2)
        return f"{width}x{height}+{x}+{y}"


    def large_func(self, func: function, args: tuple|list):
        thread = threading.Thread(target=func, args=args)
        thread.daemon = True
        thread.start()


    def get_hash(self, filepath)->str:
        sha256_hash = hashlib.sha256()
        
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()[:15]


    def save_cache(self, root):
        sha256_16 = self.get_hash(root.filepath)
        check_sha256_16 = [item.name != sha256_16 for item in self.res_path.iterdir() if item.is_file()]

        if all(check_sha256_16):
            with open(self.res_path / sha256_16, "w", encoding="utf-8") as file:
                root.add_log("Сохраняем в кэш")
                file.write(root.recognized_text + "\n")


    def try_load_cache(self, root)->bool:
        sha256_16 = self.get_hash(root.filepath)
        files = [item.name for item in self.res_path.iterdir() if item.is_file()]

        if sha256_16 in files:
            with open(self.res_path / sha256_16) as file:
                root.add_log("Найден кэш, пропускаем распознавание")
                root.finish_recognition(file.read())
                return True
        return False


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.utils = Utils()

        self.auidotypes = [
            ("MP3 Audio", "*.mp3"),
            ("WAV Audio", "*.wav"),
            ("M4A Audio", "*.m4a"),
            ("FLAC Audio", "*.flac"),
            ("AAC Audio", "*.aac"),
            ("Ogg Audio", "*.ogg"),
            ("WMA Audio", "*.wma"),
            ("All Audio Files", "*.mp3;*.wav;*.m4a;*.flac;*.aac;*.ogg;*.wma"),
        ]

        self.videotypes = [
            ("MP4 Video", "*.mp4"),
            ("QuickTime Movie", "*.mov"),
            ("AVI Video", "*.avi"),
            ("Matroska Video", "*.mkv"),
            ("WebM Video", "*.webm"),
            ("Flash Video", "*.flv"),
            ("Flash MP4 Video", "*.f4v"),
            ("Windows Media Video", "*.wmv"),
            ("MPEG Video", "*.mpeg"),
            ("MPEG Video", "*.mpg"),
            ("Ogg Video", "*.ogv"),
            ("GIF Animation", "*.gif"),
            ("All Video Files", "*.mp4;*.mov;*.avi;*.mkv;*.webm;*.flv;*.f4v;*.wmv;*.mpeg;*.mpg;*.ogv;*.gif"),
        ]

        self.filetypes = [
            *self.auidotypes,
            *self.videotypes,
            ("All Media Files", "*.mp4;*.mov;*.avi;*.mkv;*.webm;*.flv;*.f4v;*.wmv;*.mpeg;*.mpg;*.ogv;*.gif;*.mp3;*.wav;*.m4a;*.flac;*.aac;*.ogg;*.wma"),
            ("All Files", "*.*")
        ]

        self.header_font = font.Font(size=24, weight="bold")

        self._init_window()
        self._init_widgets()


    def _init_window(self):
        self.title("Speech recognizer")
        geometry = self.utils.calculate_geometry(800, 600)
        self.geometry(geometry)
        # self.resizable(False, False)


    def _init_widgets(self):
        self.title_lable = tk.Label(master=self, text="Распознавание речи OpenAI Whisper", font=self.header_font)
        self.title_lable.pack(pady=20)

        self.frame_for_buttons = tk.Frame(master=self)
        self.frame_for_buttons.pack()

        self.open_button = tk.Button(master=self.frame_for_buttons, text="Открыть аудио или видео файл", command=self.choice_file)
        self.open_button.pack(expand=True, fill="both", side="left")

        self.save_button = tk.Button(master=self.frame_for_buttons, text="Сохранить распознанный текст", command=self.save_text, state="disabled")
        self.save_button.pack(expand=True, fill="both", side="right")

        self.copy_button = tk.Button(master=self.frame_for_buttons, text="Скопировать распознанный текст", command=self.copy_text, state="disabled")
        self.copy_button.pack(expand=True, fill="both", side="right")

        self.log_text = tk.Text(master=self, height=10, state="disabled")
        self.log_text.pack(expand=True, fill="both", padx=30, pady=(10, 5))

        self.result_text = tk.Text(master=self, state="disabled")
        self.result_text.pack(expand=True, fill="both", padx=30, pady=(5, 10))


    def add_log(self, chars: str):
        self.log_text.config(state="normal")
        chars = f"[+] [{datetime.now().time()}] {chars}\n"
        self.log_text.insert(index="end", chars=chars)
        self.log_text.config(state="disabled")
        self.log_text.see(index="end")


    def choice_file(self):
        self.add_log("Открытие окна выбора файла")
        filepath = filedialog.askopenfilename(filetypes=self.filetypes)
        if not filepath:
            self.add_log("Файл не выбран")
            return
        self.add_log(f"Выбран файл {filepath}")
        self.filepath = Path(filepath)

        if self.utils.try_load_cache(self):
            return

        for d, t in self.videotypes:
            if t.replace("*", "") in filepath:
                self.add_log(f"Получаем аудио дорожку из видео")
                self.utils.large_func(backend.get_audio, (self.filepath, self,))
                break
        else:
            self.start_recognition(self.filepath)
        

    def start_recognition(self, audio_path):
        self.add_log(f"Начинаем распознование текста из аудио")
        self.utils.large_func(backend.recognition, (audio_path, self,))


    def finish_recognition(self, recognized_text):
        self.utils.save_cache(self)
        self.add_log("Вставка текста")
        self.recognized_text = recognized_text

        self.result_text.config(state="normal")
        self.result_text.delete(index1="1.0", index2="end")
        self.result_text.insert(index="1.0", chars=recognized_text)
        self.result_text.config(state="disabled")

        self.copy_button.config(state="normal")
        self.save_button.config(state="normal")


    def copy_text(self):
        self.add_log("Копирование текста")
        self.clipboard_clear()
        self.clipboard_append(self.recognized_text)


    def save_text(self):
        self.add_log("Открытие окна сохранение в txt")
        filepath = filedialog.asksaveasfilename(filetypes=[("Plain text", "*.txt")])
        if not filepath:
            self.add_log("Путь не выбран")
            return
        self.add_log(f"Сохранение в {filepath}")

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(self.recognized_text + "\n")



def main():
    app = Gui()
    app.mainloop()

if __name__ == "__main__":
    main()
