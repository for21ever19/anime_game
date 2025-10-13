import os
from PIL import Image, ImageOps, ImageFilter


SOURCE_FOLDER = "images"
OUTPUT_FOLDER = "images_processed"
TARGET_SIZE = (250, 387)

file_list = os.listdir(SOURCE_FOLDER)
for filename in file_list:
    print(f"Обрабатываю файл: {filename}")
    source_path = os.path.join(SOURCE_FOLDER, filename)
    filename_without_ext, _ = os.path.splitext(filename)
    new_filename = filename_without_ext + ".png"
    output_path = os.path.join(OUTPUT_FOLDER, new_filename)

    try:
       image = Image.open(source_path)
       processed_image = ImageOps.fit(image, TARGET_SIZE, Image.Resampling.LANCZOS)
       
       processed_image = processed_image.filter(ImageFilter.SHARPEN)

       processed_image.save(output_path)

    except Exception as e:
        print(f"Не удалось открыть {filename}. Ошибка: {e}")
        continue