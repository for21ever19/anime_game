import tkinter as tk
from PIL import ImageTk, Image, ImageDraw, ImageFont
import random 
import json
import os
import card_creator

class App:
    def __init__(self, master):
        print("--- Чекпойнт 1: App.__init__ НАЧАЛСЯ ---")
        self.master = master
        self.master.title("Моя ООП Аниме Игра")
        self.master.minsize(300, 400)
        self.all_cards = []  # Список для всех карт
        self.sorted_cards = {'C': [], 'B': [], 'A': [], 'S': []} 

        self.user_collection = []


        self._load_cards()

        self.balance = tk.StringVar()
        self.balance.set("Ваш баланс: 0 алмазиков")
        self.user_collection = []

        self.all_subjects_data = {}
        self.load_questions()
        print("--- Чекпойнт 2: Загрузка данных ЗАВЕРШЕНА ---")
        self.current_subject = None
        self.current_question = None

        container = tk.Frame(master=self.master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F_class in (MainMenuFrame, SubjectsFrame, QuizFrame, DifficultyFrame):
            page_name = F_class.__name__
            print(f"--- Чекпойнт 3: Создаю фрейм: {page_name} ---") 
            frame = F_class(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        print("--- Чекпойнт 4: Все фреймы СОЗДАНЫ ---")
        self.show_frame('MainMenuFrame')
    def _load_cards(self):
            self.all_cards = [{'anime': 'One Piece', 
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
                'image_path': 'inosuke1.png'}]

            for card in self.all_cards:
                rarity = card['rarity']
                if rarity in self.sorted_cards:
                    self.sorted_cards[rarity].append(card)


    def subject_selected(self, subjects_name):
        self.current_subject = subjects_name
        self.show_frame('DifficultyFrame')

    def difficulty_selected(self, level):
        self.current_question = random.choice(self.all_subjects_data[self.current_subject][level.lower()])
        self.show_frame('QuizFrame')
        self.frames['QuizFrame'].display_question(self.current_question)
        print(f"Выбран предмет: {self.current_subject}, сложность: {level}")


    def check_answer(self, selected_option):
        correct = self.current_question['correct_answer']
        is_correct = (selected_option == correct)   
        self.frames['QuizFrame'].show_feedback(is_correct)
        if is_correct:
            if self.current_question['difficulty'] == 'легкий':
                self.gambling(210)
            if self.current_question['difficulty']  == 'средний':
                self.gambling(270)
            if self.current_question['difficulty']  == 'сложный':
                self.gambling(350)
        self.frames['QuizFrame'].block_buttons('disabled')
        self.master.after(2000, self.next_round)


    def next_round(self):
        self.show_frame('SubjectsFrame')
    # А вот здесь уже ВЫЗЫВАЕМ переключение
        self.frames['QuizFrame'].show_feedback(None)
    
    # ПРИКАЗ: "Комната, включи свои кнопки для нового раунда!"
        self.frames['QuizFrame'].block_buttons('normal')




    def load_questions(self):
        QUESTIONS_FOLDER = 'questions' # Указываем имя нашей папки
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
                            self.all_subjects_data[subject_name] = sorted_questions
                            print(f"Предмет '{subject_name}' успешно загружен.")
                    except Exception as e:
                        print(f"Ошибка при загрузке файла {filename}: {e}")
        else:
            print(f"ВНИМАНИЕ: Папка '{QUESTIONS_FOLDER}' не найдена. Викторина будет недоступна.")

        

    def gambling(self, amount):
        current_balance_str = self.balance.get().split()[2] 
        current_balance = int(current_balance_str)
        new_balance = current_balance + amount
        self.balance.set(f"Ваш баланс: {new_balance} алмазиков")

    
    



    def get_new_card(self):
        card_cost = 100
        balance_str = self.balance.get().split()[2]
        current_balance = int(balance_str)

        if current_balance < card_cost:
            self.frames['MainMenuFrame'].show_message(f"Необходимо еще {card_cost - current_balance} алмазиков")
            return

        self.gambling(-card_cost) # Списываем деньги

        chance = random.randint(1, 100)
        card = None
        if chance <= 60:
            card = random.choice(self.sorted_cards['C'])
        elif chance <= 85:
            card = random.choice(self.sorted_cards['B'])
        elif chance <= 99:
            card = random.choice(self.sorted_cards['A'])
        else:
            card = random.choice(self.sorted_cards['S'])
        
        self.user_collection.append(card)
        
        # Финальный приказ: "Комната, покажи эту карту!"
        self.frames['MainMenuFrame'].display_card_result(card)
        print("--- Чекпойнт 5: App.__init__ ЗАВЕРШЕН ---")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        

class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text='Главное меню')
        label.pack(pady=20)
        balance_label = tk.Label(self, textvariable=self.controller.balance)
        balance_label.pack(pady=5)
        self.message_label = tk.Label(self, text="")
        self.message_label.pack()
        self.result_l = tk.Label(self, text = '')
        self.result_l.pack()
        balance_button = tk.Button(self, text='Мани-мани', command=lambda: self.controller.gambling(200))
        balance_button.pack()
        gamble_button = tk.Button(self, text='Крутить барабан', command= self.controller.get_new_card)
        gamble_button.pack()

        start_button = tk.Button(self, text='Начать', command=lambda: controller.show_frame('SubjectsFrame'))
        start_button.pack()


    def show_message(self, message):
        self.message_label.config(text=message)

    def display_card_result(self, card_data):
        self.message_label.config(text="") # Очищаем старые сообщения
        if "image_path" in card_data:
            try:
                final_card_image = card_creator.create_card_image(card_data)
                photo_image = ImageTk.PhotoImage(final_card_image)  
                self.result_l.config(image=photo_image, text="") 
                self.result_l.image = photo_image 
            except Exception as e:
                # Если картинку не удалось загрузить, показываем текст
                print(f"Ошибка загрузки изображения: {e}")
                result_text = f"Выпала карта: [{card_data['rarity']}] {card_data['name']}"
                self.result_l.config(image="", text=result_text)
        else:
            result_text = f"Выпала карта: [{card_data['rarity']}] {card_data['name']}"
            self.result_l.config(image="", text=result_text)
            self.result_l.config(text=result_text)


class SubjectsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        subjects_name = controller.all_subjects_data.keys()
        
        for x in subjects_name:
            subjects_name_button = tk.Button(self, text = x.title(), command = lambda s= x: controller.subject_selected(s))
            subjects_name_button.pack()
        return_button = tk.Button(self, text='Назад', command=lambda: controller.show_frame('MainMenuFrame'))
        return_button.pack(pady=5)

class QuizFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 

        self.question_label = tk.Label(self, text='Тут будет будущий вопрос')
        self.question_label.pack(pady=20)
        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self, text=f"Вариант {i+1}")
            button.pack(pady=5)
            self.option_buttons.append(button)
        
        return_button = tk.Button(self, text='Назад', command=lambda: controller.show_frame('SubjectsFrame'))
        return_button.pack(pady=5)

        self.feedback_label = tk.Label(self, text=" ", font=("Arial", 12), pady=5)
        self.feedback_label.pack()



    def display_question(self, question_data):
        
        self.question_label.config(text=question_data['question'])
        self.options = question_data['options']
        

        for i in range(4):
            option = self.options[i]
            self.option_buttons[i].config(text = option)
            self.option_buttons[i].config(command = lambda opt=option: self.controller.check_answer(opt))

    def show_feedback(self, is_correct):
        if is_correct is None: # Явно проверяем: "Это команда на очистку?"
            self.feedback_label.config(text="")
        elif is_correct:
            self.feedback_label.config(text="Правильно!", fg="green")
        elif not is_correct:
            self.feedback_label.config(text=f"Неверно!", fg="red")
    
    def block_buttons(self, new_state):
        for btn in self.option_buttons:
            btn.config(state=new_state)
        
    

class DifficultyFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        easy_button = tk.Button(self, text="Легкий", command=lambda: controller.difficulty_selected('Легкий'))
        easy_button.pack(pady=5)

        mid_button = tk.Button(self, text="Средний", command=lambda: controller.difficulty_selected("Средний"))
        mid_button.pack(pady=5)

        difficult_button = tk.Button(self, text="Сложный", command=lambda: controller.difficulty_selected('Сложный'))
        difficult_button.pack(pady=5)

        back_to_mid_button = tk.Button(self, text="Назад", command= lambda:controller.show_frame('SubjectsFrame'))
        back_to_mid_button.pack(pady=10)




main_window = tk.Tk()

app = App(main_window)

main_window.mainloop()
