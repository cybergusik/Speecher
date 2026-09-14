from moviepy import VideoFileClip
import argparse
import platform

if platform.system() == "Darwin":
    import mlx_whisper
else:
    import whisper
    model = whisper.load_model("turbo")

def get_audio(video_path, root=None)->str|None:
    try:
        video = VideoFileClip(video_path)

        audio = video.audio
        audio_path = f"{'.'.join(video_path.split('.')[:-1])}.mp3" if "." in video_path else f"{video_path}.mp3"
        audio.write_audiofile(audio_path)

        audio.close()
        video.close()

        if not root:
            return audio_path

        root.add_log(f"Аудио дорожка успешно извлечена в {audio_path}")
        root.start_recognition(audio_path)

    except Exception as e:
        text_error = f"Возникла ошибка при извлечении аудиодорожки: {e}"
        if not root:
            print(text_error)
        else:
            root.add_log(text_error)


def recognition(audio_path, root=None)->str|None:
    try:
        if platform.system() == "Darwin":
            result = mlx_whisper.transcribe(audio_path, path_or_hf_repo="mlx-community/whisper-large-v3-turbo")
        else:
            result = model.transcribe(audio_path)

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
