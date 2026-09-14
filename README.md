<div align="center">

[RU](./README.md) | [EN](./README_EN.md)

</div>

![GUI](./images/preview1.png)
![GUI](./images/preview2.png)

# Speecher

Speecher — простое GUI приложение на python для локального распознавание речи из медиа файлов. Для графического интерфейса используется tkinter, а для распознавания текста из аудио — модель OpenAI Whisper. При выборе медиафайла определяется его тип. Для видео предварительно извлекается аудиодорожка с помощью ffmpeg, после чего аудио передаётся модели Whisper для распознавания речи.

---

### Требования:

| Компонент | Требование |
| --------- | ---------- |
| Python    | >= 3.9     |
| ffmpeg    | any        |
| ОЗУ       | >= 8Gb     |
| Хранилище | >= 2Gb     |

---

## Возможности

- **Графический интерфейс**
- **Командый интерфейс**
- **Полностью локальная обработка**
- **Поддержка большинства аудио-видео-форматов**

## Особенности

- **`0%` кода написано ИИ**
- **Кроссплатформенность**
- **Минимализм**
- **Логирование**

---

### Установка [ffmpeg](https://ffmpeg.org/):

```bash
# debian-based
sudo apt update && sudo apt install ffmpeg

# arch-based
sudo pacman -S ffmpeg

# macos (https://brew.sh/)
brew install ffmpeg

# windows (https://chocolatey.org/)
choco install ffmpeg

# windows (https://scoop.sh/)
scoop install ffmpeg
```

### Клонирование репозитория:

```bash
git clone https://github.com/cybergusik/Speecher.git
cd Speecher
```

### Создание и активация виртуального окружения(опционально):

```bash
# unix-based
python3 -m venv .venv
source .venv/bin/activate

# windows
python -m venv venv
venv\Scripts\activate
```

### Установка зависимостей:

```bash
# unix-based
pip3 install -r requirements.txt

# windows
pip install -r requirements.txt
```

---

> [!IMPORTANT]
> При первом запуске скачается модель Whisper `turbo`, размером около 2Gb. Убедитесь, что на диске достаточно свободного места

### Запуск:

Графический интерфейс:

```
# unix-based
python3 gui.py

# windows
python gui.py
```

Также есть поддержка командой строки для `backend.py`:

```
Аргументы:
    --video <path_to_video_file>
    --audio <path_to_audio_file>
```

**Поддерживаемые форматы:**

Видео:

- [x] mp4
- [x] mov
- [x] avi
- [x] mkv
- [x] webm
- [x] flv
- [x] f4v
- [x] wmv
- [x] mpeg
- [x] mpg
- [x] ogv
- [x] gif

Аудио:

- [x] mp3
- [x] wav
- [x] m4a
- [x] flac
- [x] aac
- [x] ogg
- [x] wma

### To-Do:

- [ ] Добавить поддержку [GigaAM](https://github.com/salute-developers/GigaAM)
- [ ] Сделать сохранение промежуточных результатов и уже полностью обработанных данных в кэш
