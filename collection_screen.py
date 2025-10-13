import tkinter as tk
from PIL import ImageTk, Image
import card_creator
import os
import json

def reset_and_redraw(parent_frame, collection_data, back_command):
    """
    Эта функция очищает коллекцию и немедленно перерисовывает экран.
    """
    # 1. Очищаем список с данными
    collection_data.clear()
    
    # 2. Удаляем файл сохранения
    try:
        os.remove("collection.json")
    except FileNotFoundError:
        print("Файл collection.json не найден, нечего удалять.")
        pass
        
    # 3. Снова вызываем главную функцию отрисовки,
    # но теперь она получит уже пустой список collection_data
    # и покажет сообщение, что коллекция пуста.
    create_collection_screen(parent_frame, collection_data, back_command)


def create_collection_screen(parent_frame, collection_data, back_command):
    for widget in parent_frame.winfo_children():
        widget.destroy()
        
    title_label = tk.Label(parent_frame, text="Моя Коллекция", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Создаем контейнер для кнопок внизу
    bottom_frame = tk.Frame(parent_frame)
    bottom_frame.pack(side="bottom", pady=10, fill="x")

    back_button = tk.Button(bottom_frame, text="Назад в Главное Меню", command=back_command)
    back_button.pack(side="left", padx=20)
    
    # --- ИЗМЕНЕНИЕ НАЧИНАЕТСЯ ЗДЕСЬ ---
    # Создаем кнопку сброса. 
    # Команда для нее - это вызов нашей новой функции reset_and_redraw.
    # Мы используем lambda, чтобы передать в нее все нужные аргументы.
    reset_button = tk.Button(
        bottom_frame, 
        text="Начать заново", 
         # Сделаем текст красным для предупреждения
        command=lambda: reset_and_redraw(parent_frame, collection_data, back_command)
    )
    reset_button.pack(side="right", padx=20)

    if not collection_data:
        empty_label = tk.Label(parent_frame, text="Ваша коллекция пока пуста.\nВыполняйте задания, чтобы получить карты!")
        empty_label.pack(pady=20)
        return
    scroll_container = tk.Frame(parent_frame)
    scroll_container.pack(fill="both", expand=True)

    # 2. Создаем холст (Canvas)
    my_canvas = tk.Canvas(scroll_container)
    my_canvas.pack(side="left", fill="both", expand=True)

    # 3. Создаем полосу прокрутки
    my_scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=my_canvas.yview)
    my_scrollbar.pack(side="right", fill="y")

    # 4. "Связываем" холст и скроллбар
    my_canvas.configure(yscrollcommand=my_scrollbar.set)

    # 5. Создаем ВТОРОЙ фрейм ВНУТРИ холста. На нем и будут картинки.
    # ЭТОТ ФРЕЙМ БУДЕТ ПРОКРУЧИВАТЬСЯ
    image_frame = tk.Frame(my_canvas)

    # 6. Добавляем этот фрейм на холст
    my_canvas.create_window((0, 0), window=image_frame, anchor="nw")

    # 7. Эта функция будет обновлять размер холста, чтобы скроллбар знал, какой он длины
    def on_configure(event):
        my_canvas.configure(scrollregion=my_canvas.bbox("all"))

    image_frame.bind("<Configure>", on_configure)

    # --- КОНЕЦ СОЗДАНИЯ ПРОКРУЧИВАЕМОЙ ОБЛАСТИ ---

        # --- ЦИКЛ ДЛЯ ОТОБРАЖЕНИЯ КАРТОЧЕК ---

# Создаем список, чтобы хранить ссылки на изображения (ВАЖНО!)
    card_images = [] 

    for card_data in collection_data:
        # 1. Генерируем изображение карты "на лету"
        card_image_pil = card_creator.create_card_image(card_data)
        
        # 2. Конвертируем его в формат, понятный tkinter
        card_image_tk = ImageTk.PhotoImage(card_image_pil)
        
        # 3. Сохраняем ссылку на изображение. Если этого не сделать, Python
        # "потеряет" картинку, и она не отобразится. Это частая ловушка в tkinter.
        card_images.append(card_image_tk)
        
        # 4. Создаем Label, но теперь в качестве контента у него будет картинка
        # Родитель - наш новый image_frame!
        card_label = tk.Label(image_frame, image=card_image_tk)
        card_label.image = card_image_tk
        card_label.pack(pady=10, padx=10) # Добавим отступы для красоты
        
                # Этот блок нужен для того, чтобы можно было тестировать этот файл отдельно
if __name__ == '__main__':
    # Создаем тестовое окно
    root = tk.Tk()
    root.geometry("800x600")
    
    # Создаем тестовый фрейм, который будет имитировать наш экран коллекции
    collection_frame = tk.Frame(root)
    collection_frame.pack(fill="both", expand=True)

    # Создаем тестовые данные
    test_collection = [
    {'name': 'Monkey D. Luffy', 'rarity': 'S', 'image_path': 'luffy.png', 'anime': 'One Piece'},
    {'name': 'Katsura Kotaro', 'rarity': 'B', 'image_path': 'katsura4.png', 'anime': 'Gintama'},
]

    create_collection_screen(collection_frame, test_collection, lambda: print("Кнопка 'Назад' нажата!"))

    # Вызываем нашу главную функцию
    root.mainloop()

