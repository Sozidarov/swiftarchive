import sys
import os
import shutil
import tempfile
import time
import py7zr
from pystyle import *
from PIL import Image, UnidentifiedImageError

ascii = """
  _________       .__  _____  __       _____                .__    .__              
 /   _____/_  _  _|__|/ ____\/  |_    /  _  \_______   ____ |  |__ |__|__  __ ____  
 \_____  \\ \/ \/ /  \   __\\   __\  /  /_\  \_  __ \_/ ___\|  |  \|  \  \/ // __ \ 
 /        \\     /|  ||  |   |  |   /    |    \  | \/\  \___|   Y  \  |\   /\  ___/ 
/_______  / \/\_/ |__||__|   |__|   \____|__  /__|    \___  >___|  /__| \_/  \___  >
        \/                                  \/            \/     \/              \/ 
                                                                                   
"""

ascii2 = """
________            _____                .__    .__              
\______ \   ____   /  _  \_______   ____ |  |__ |__|__  __ ____  
 |    |  \_/ __ \ /  /_\  \_  __ \_/ ___\|  |  \|  \  \/ // __ \ 
 |    `   \  ___//    |    \  | \/\  \___|   Y  \  |\   /\  ___/ 
/_______  /\___  >____|__  /__|    \___  >___|  /__| \_/  \___  >
        \/     \/        \/            \/     \/              \/ 
                                                                
"""

def generate_random_name(length=8):
    import random, string
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def clear_file_metadata(file_path, temp_dir):
    filename = os.path.basename(file_path)
    temp_file_path = os.path.join(temp_dir, filename)
    os.utime(path, (timestamp, timestamp))
    shutil.copy2(file_path, temp_file_path)

    timestamp = time.mktime((2000, 1, 1, 0, 0, 0, 0, 0, 0))
    os.utime(temp_file_path, (timestamp, timestamp))

    try:
        with Image.open(temp_file_path) as img:

            data = list(img.getdata())
            img_no_exif = Image.new(img.mode, img.size)
            img_no_exif.putdata(data)
            img_no_exif.save(temp_file_path)
    except UnidentifiedImageError:
        pass
    except Exception as e:
        print(f"Предупреждение: не удалось очистить EXIF: {e}")


    return temp_file_path

def create_archive():
    Write.Print(ascii, Colors.orange, interval=0.0005)
    file_path = input("Введите путь к файлу: ").strip()
    if not os.path.isfile(file_path):
        print("Файл не найден")
        return

    save_dir = input("Введите папку для сохранения архива: ").strip()
    if not os.path.isdir(save_dir):
        print("Папка для сохранения не найдена")
        return

    password = input("Введите пароль (Enter — без пароля): ").strip() or None
    archive_name = f"swiftarchive_{generate_random_name()}.7z"
    archive_path = os.path.join(save_dir, archive_name)

    with tempfile.TemporaryDirectory() as tmpdir:
        clean_file = clear_file_metadata(file_path, tmpdir)

        with py7zr.SevenZipFile(archive_path, 'w', password=password) as archive:
            archive.write(clean_file, arcname=os.path.basename(file_path))

    print(f"Архив создан: {archive_path}")

def extract_archive():
    Write.Print(ascii2, Colors.orange, interval=0.0005)
    archive_path = input("Введите путь к архиву: ").strip()
    if not os.path.isfile(archive_path):
        print("Архив не найден")
        return

    password = input("Введите пароль (Enter — без пароля): ").strip() or None
    extract_dir = os.path.splitext(archive_path)[0] + "_extracted"
    os.makedirs(extract_dir, exist_ok=True)

    try:
        with py7zr.SevenZipFile(archive_path, mode='r', password=password) as archive:
            archive.extractall(path=extract_dir)
        print(f"Архив распакован в: {extract_dir}")
    except py7zr.exceptions.Bad7zFile:
        print("Ошибка: повреждённый архив или неверный пароль")
    except Exception as e:
        print(f"Ошибка при распаковке: {e}")

def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python main.py -archive   # для архивирования")
        print("  python main.py -dearchive # для распаковки")
        return

    cmd = sys.argv[1].lower()
    if cmd == '-archive':
        create_archive()
    elif cmd == '-dearchive':
        extract_archive()
    else:
        print("Неизвестная команда. Используйте -archive или -dearchive")

if __name__ == "__main__":
    main()
