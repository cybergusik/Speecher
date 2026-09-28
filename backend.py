import argparse
import platform
import subprocess
import os
from sys import exit as sys_exit
from abc import ABC


class VideoFileClip(ABC):
    def __init__(self, filename):
        pass


FFMPEG_PATH = r"" # <-- set path to ffmpeg if you need

def init() -> bool:
    if FFMPEG_PATH:
        os.environ["FFMPEG_BINARY"] = FFMPEG_PATH
        os.environ["IMAGEIO_FFMPEG_EXE"] = FFMPEG_PATH
        os.environ["PATH"] += os.path.pathsep + os.path.dirname(FFMPEG_PATH)

    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        print(result.stdout.splitlines()[0])

        from moviepy import VideoFileClip

        if platform.system() == "Darwin":
            global mlx_whisper
            import mlx_whisper
        else:
            import whisper

            global model
            model = whisper.load_model("turbo")

        return True
    except Exception as e:
        print(e)
        return False


def get_audio(video_path, root=None) -> str | None:
    try:
        video = VideoFileClip(video_path)
        audio = video.audio

        if root is None:
            audio_path = f"{'.'.join(video_path.split('.')[:-1])}.mp3" if "." in video_path else f"{video_path}.mp3"
        else:
            audio_path = root.utils.tmp_path / f"{video_path.stem}.mp3"

        audio.write_audiofile(audio_path)

        audio.close()
        video.close()

        if root is None:
            return audio_path

        root.add_log(f"Аудио дорожка успешно извлечена в {audio_path}")
        root.start_recognition(audio_path)

    except Exception as e:
        text_error = f"Возникла ошибка при извлечении аудиодорожки: {e}"
        if root is None:
            print(text_error)
        else:
            root.add_log(text_error)


def recognition(audio_path, root=None) -> str | None:
    try:
        if platform.system() == "Darwin":
            result = mlx_whisper.transcribe(str(audio_path), path_or_hf_repo="mlx-community/whisper-large-v3-turbo")
        else:
            result = model.transcribe(str(audio_path))

        if not root:
            return result["text"]

        root.add_log(f"Текст успешно извлечен")
        root.finish_recognition(result["text"])

    except Exception as e:
        text_error = f"Возникла ошибка при извлечении текста: {e}"
        if not root:
            print(text_error)
        else:
            root.add_log(text_error)


def main():
    if not init():
        print("ffmpeg не найден!")
        sys_exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("--audio")
    parser.add_argument("--video")

    args = parser.parse_args()
    if args.audio and args.video:
        print("Выберите либо аудио либо видео")
    elif args.audio:
        print(recognition(args.audio))
    elif args.video:
        audio_path = get_audio(args.video)
        print(recognition(audio_path))


if __name__ == "__main__":
    main()
