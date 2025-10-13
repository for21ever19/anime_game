import tkinter as tk
from PIL import ImageTk, Image, ImageDraw, ImageFont
import random 
import json
import os
import card_creator
import collection_screen

c_cards = []
b_cards = []
a_cards = []
s_cards = []

all_subjects_data = {}

current_quiz_question = None
current_quiz_difficulty = None


try:
    with open('collection.json', 'r', encoding='utf-8') as f:
        user_collection = json.load(f)
    
except FileNotFoundError:
    user_collection = []
    balance = 0

QUESTIONS_FOLDER = 'questions' # Указываем имя нашей папки

# Проверяем, существует ли папка
if os.path.exists(QUESTIONS_FOLDER):
    # Проходим по каждому файлу в этой папке
    for filename in os.listdir(QUESTIONS_FOLDER):
        print(f"Найден файл: {filename}")
        # Нас интересуют только файлы, заканчивающиеся на .json
        if filename.endswith('.json') and not filename.startswith('.'):
            # Извлекаем имя предмета из имени файла (например, 'biology.json' -> 'biology')
            subject_name = filename.split('.')[0]
            
            # Собираем полный путь к файлу
            file_path = os.path.join(QUESTIONS_FOLDER, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    questions_list = json.load(f)
                    
                    # Та же самая логика сортировки, что и раньше
                    sorted_questions = {"легкий": [], "средний": [], "сложный": []}
                    for q_data in questions_list:
                        difficulty = q_data['difficulty']
                        if difficulty in sorted_questions:
                            sorted_questions[difficulty].append(q_data)
                    
                    # Складываем отсортированные вопросы в наше общее хранилище
                    all_subjects_data[subject_name] = sorted_questions
                    print(f"Предмет '{subject_name}' успешно загружен.")
            except Exception as e:
                print(f"Ошибка при загрузке файла {filename}: {e}")
else:
    print(f"ВНИМАНИЕ: Папка '{QUESTIONS_FOLDER}' не найдена. Викторина будет недоступна.")



all_cards = [{'anime': 'One Piece', 
          'name': 'Monkey D. Luffy',
          'rarity': 'S',
          'image_path': 'luffy.png'},
          {'anime': 'Gintama', 
          'name': 'Sakata Gintoki',
          'rarity': 'S',
          'image_path': 'Gintoki.png'},
          {'anime': 'Bleach', 
          'name': 'Kisuke Urahara',
          'rarity': 'B',
          'image_path': 'Urahara2.png'},
          {'anime': 'Bleach', 
          'name': 'Shunsui Kyoraku',
          'rarity': 'A',
          'image_path': 'Kyoraku.png'},
          {'anime': 'GTO', 
          'name': 'Eikichi Onizuka',
          'rarity': 'A',
          'image_path': 'onizuka.png'},
          {'anime': 'Reborn: Vending Machine', 
          'name': 'Vending Machine',
          'rarity': 'C',
          'image_path': 'vending_machine.png'},
          {'anime': 'Blue Lock', 
          'name': 'Niko Ikki',
          'rarity': 'C',
          'image_path': 'niko.png'},
          {'anime': 'Demon Slayer', 
          'name': 'Nezuko Kamado',
          'rarity': 'B',
          'image_path': 'nezuko.png'},
          {'anime': 'Jojo', 
          'name': 'Gyro Zeppeli',
          'rarity': 'S',
          'image_path': 'zeppeli.png'},
          {'anime': 'Jojo', 
          'name': 'Guido Mista',
          'rarity': 'A',
          'image_path': 'mista.png'},
          {'anime': 'Jojo', 
          'name': 'Rohan Kishibe',
          'rarity': 'B',
          'image_path': 'rohan.png'},
          {'anime': 'Jojo', 
          'name': 'Mike O.',
          'rarity': 'C',
          'image_path': 'Mike_O.png'},
          {'anime': 'Attack on Titan', 
          'name': 'The Shiganshina',
          'rarity': 'C',
          'image_path': 'wall.png'},
          {'anime': 'GTO', 
          'name': 'Hiroshi Utiamada',
          'rarity': 'C',
          'image_path': 'hirosi.png'},
          {'anime': 'Blue Lock', 
          'name': 'Julian Loki',
          'rarity': 'A',
          'image_path': 'Loki.png'},
         {'anime': 'Gintama',
          'name': 'Katsura Kataro',
          'rarity': 'B',
          'image_path': 'katsura4.png'}, 
          {'anime': 'Vinland Saga',
          'name': 'Torkel The Tall',
          'rarity': 'A',
          'image_path': 'Thorkell.png'},
          {'anime': 'Vinland Saga',
          'name': 'Askeladd',
          'rarity': 'A',
          'image_path': 'askeladd2.png'},
          {'anime': 'Vinland Saga',
          'name': 'Ragnar',
          'rarity': 'C',
          'image_path': 'Ragnar.png'},
          {'anime': 'Gintama',
          'name': 'Shinpachi',
          'rarity': 'A',
          'image_path': "Shinpachi.png"},
          {'anime': 'Demon Slayer',
          'name': 'Inosuke',
          'rarity': 'C',
          'image_path': 'inosuke1.png'},

]

for card in all_cards:
    if card['rarity'] == 'C':
        c_cards.append(card)
    elif card['rarity'] == 'B':
        b_cards.append(card)
    elif card['rarity'] == 'A':
        a_cards.append(card)
    elif card['rarity'] == 'S':
        s_cards.append(card)


window = tk.Tk()
window.minsize(200, 300)

main_menu_frame = tk.Frame(window) 
main_menu_frame.pack()

subjects_frame = tk.Frame(window)
difficulty_frame = tk.Frame(window)
quiz_frame = tk.Frame(window)
collection_frame = tk.Frame(window)



question_label = tk.Label(quiz_frame, text="Текст вопроса", font=("Arial", 16), pady=10)
question_label.pack()

option_buttons = []
for i in range(4):
    button = tk.Button(quiz_frame, text=f"Вариант {i+1}")
    button.pack(pady=5)
    option_buttons.append(button)

feedback_label = tk.Label(quiz_frame, text="", font=("Arial", 12), pady=10)
feedback_label.pack()


def start_quiz(subject_name, difficulty_level):
    global current_quiz_question, current_quiz_difficulty
    current_quiz_difficulty = difficulty_level
    
    # Используем ОБА аргумента для выбора списка вопросов
    questions_list = all_subjects_data[subject_name][difficulty_level]
    current_quiz_question = random.choice(questions_list)
    
    display_question(current_quiz_question)

    difficulty_frame.pack_forget()
    quiz_frame.pack()


def show_collection_screen():
    # Вызываем конструктор из нашего нового файла!
    # Он сам построит все, что нужно, внутри collection_frame
    collection_screen.create_collection_screen(collection_frame, user_collection, show_main_menu_from_collection)
    
    main_menu_frame.pack_forget()
    collection_frame.pack(fill="both", expand=True)
    print('Привет')

def show_main_menu_from_collection():
    collection_frame.pack_forget()
    main_menu_frame.pack()


def check_answer(selected_option):
    global balance
    
    # Блокируем кнопки
    for btn in option_buttons:
        btn.config(state="disabled")

    correct = current_quiz_question['correct_answer']
    if selected_option == correct:
        feedback_label.config(text="Правильно!", fg="green")
        if current_quiz_difficulty == "легкий":
            balance += 210
        elif current_quiz_difficulty == "средний":
            balance += 280
        else: # Сложный
            balance += 360
        balance_l.config(text=f"Ваш баланс: {balance} алмазиков")
    else:
        feedback_label.config(text=f"Неверно!", fg="red")   

    # Планируем возврат на экран сложности через 2 секунды
    window.after(2000, show_difficulty_from_quiz)


def display_question(question_data):
    feedback_label.config(text="")

    question_label.config(text=question_data['question'])
    
    options = question_data['options']
    random.shuffle(options) 

    for i in range(4):
        button = option_buttons[i]
        option_text = options[i]
        button.config(text=option_text, state="normal", command=lambda opt=option_text: check_answer(opt))


    

def show_difficulty_from_quiz():
    quiz_frame.pack_forget()
    difficulty_frame.pack()
    difficulty_frame.update_idletasks()

def show_subjects_screen():
    # 1. Очищаем фрейм
    for widget in subjects_frame.winfo_children():
        widget.destroy()

    # 2. ДИНАМИЧЕСКИ СОЗДАЕМ КНОПКИ ЗДЕСЬ
    for subject_name in all_subjects_data.keys():
        btn_text = subject_name.title()
        command = lambda s=subject_name: show_difficulty_screen(s)
        btn = tk.Button(subjects_frame, text=btn_text, command=command)
        btn.pack(pady=5)
    
    # 3. Создаем кнопку "Назад"
    back_to_main_button = tk.Button(subjects_frame, text="Назад", command=show_main_menu_screen)
    back_to_main_button.pack(pady=10)

        # 4. Переключаем экраны
    main_menu_frame.pack_forget()
    subjects_frame.pack()

def show_main_menu_screen():
    subjects_frame.pack_forget()
    main_menu_frame.pack()

def show_difficulty_screen(subject_name):
    # Настраиваем команды для кнопок, передавая им ДВА аргумента
    easy_button.config(command=lambda: start_quiz(subject_name, "легкий"))
    mid_button.config(command=lambda: start_quiz(subject_name, "средний"))
    difficult_button.config(command=lambda: start_quiz(subject_name, "сложный"))

    subjects_frame.pack_forget()
    difficulty_frame.pack()

def show_subjects_from_difficulty():
    difficulty_frame.pack_forget()
    subjects_frame.pack()




back_to_main_button = tk.Button(subjects_frame, text="Назад", command=show_main_menu_screen)
back_to_main_button.pack(pady=10)


########### Третий Экран 



easy_button = tk.Button(difficulty_frame, text="Легкий", command=lambda: start_quiz("легкий"))

easy_button.pack(pady=5)

mid_button = tk.Button(difficulty_frame, text="Средний", command=lambda: start_quiz("средний"))
mid_button.pack(pady=5)

difficult_button = tk.Button(difficulty_frame, text="Сложный", command=lambda: start_quiz("сложный"))
difficult_button.pack(pady=5)

back_to_mid_button = tk.Button(difficulty_frame, text="Назад", command=show_subjects_from_difficulty)
back_to_mid_button.pack(pady=10)



############# Функции
def get_new_card():
    global balance
    message_label.config(text="")
    card_cost = 100
    if balance < card_cost:
        message_label.config(text=f"Необходимо еще {card_cost - balance} алмазиков")
        return
    
    balance = balance - card_cost
    balance_l.config(text=f"Ваш баланс: {balance} алмазиков")

    chance = random.randint(1, 100)

    if chance <= 60:
        card = random.choice(c_cards) 
    elif chance <= 85:
        card = random.choice(b_cards) 
    elif chance <= 99:
        card = random.choice(a_cards) 
    else: # или elif chance == 100:
        card = random.choice(s_cards)

    user_collection.append(card)
    result_text = f"Выпала карта: [{card['rarity']}] {card['name']} ({card['anime']})"
    result_l.config(text=result_text)
    if "image_path" in card:
        final_card_image = card_creator.create_card_image(card)
        photo_image = ImageTk.PhotoImage(final_card_image)  
        result_l.config(image=photo_image, text="") 
        result_l.image = photo_image 
    else:
        result_l.config(image="", text=result_text)





def balance_work():
    message_label.config(text="")
    global balance
    balance += 300
    balance_l.config(text=f"Ваш баланс: {balance} алмазиков")


window.title('')

roll_button = tk.Button(master = main_menu_frame, text = 'Получить новую карту', command=get_new_card)
roll_button.pack()

collection_button = tk.Button(master = main_menu_frame, text = 'Моя коллекция', command=show_collection_screen)
collection_button.pack()

tasks_button = tk.Button(master=main_menu_frame, text='Выполнить задание', command=show_subjects_screen)
tasks_button.pack()

balance_button = tk.Button(master = main_menu_frame, text = 'Мани-мани', command=balance_work)
balance_button.pack()

balance_l = tk.Label(master = main_menu_frame, text = f"Ваш баланс: {balance} алмазиков")
balance_l.pack()


message_label = tk.Label(master=main_menu_frame, text="")
message_label.pack()

result_l = tk.Label(master = main_menu_frame, text = '')
result_l.pack()




window.mainloop()
