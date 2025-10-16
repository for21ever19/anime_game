import random 
import json
import os
import card_creator
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images_processed') # Предполагаю, что картинки в папке 'images'
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
QUESTIONS_DIR = os.path.join(BASE_DIR, 'questions')

class App:
    def __init__(self, questions_dir):
        print("--- Чекпойнт 1: App.__init__ НАЧАЛСЯ ---")
        self.all_cards = []  # Список для всех карт
        self.sorted_cards = {'C': [], 'B': [], 'A': [], 'S': []} 

        self.user_collection = {}

        self.collection_list = []
        self.current_collection_index = 0


        self._load_cards()

        self.balance = 0

        self.all_subjects_data = self.load_questions(questions_dir) # <--- ИЗМЕНЕНИЕ

        print("--- Чекпойнт 2: Загрузка данных ЗАВЕРШЕНА ---")
        self.current_subject = None
        self.current_question = None



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
        return subjects_name

    def difficulty_selected(self, level):
        question = random.choice(self.all_subjects_data[self.current_subject][level.lower()])
    
        # 2. "Мозг, запомни: текущий вопрос - это вот этот словарь {...}"
        self.current_question = question
        
        # 3. Возвращаем вопрос, чтобы его можно было показать
        return question


    def check_answer(self, selected_option):
        correct = self.current_question['correct_answer']
        is_correct = (selected_option == correct)   
        
        if is_correct:
            if self.current_question['difficulty'] == 'легкий':
                self.gambling(210)
            if self.current_question['difficulty']  == 'средний':
                self.gambling(270)
            if self.current_question['difficulty']  == 'сложный':
                self.gambling(350)

        return is_correct




    



    def load_questions(self, questions_folder_path): # <--- ИЗМЕНЕНИЕ
        local_subjects_data = {} 
        if os.path.exists(questions_folder_path): # <--- ИЗМЕНЕНИЕ

            for filename in os.listdir(questions_folder_path): # <--- ИЗМЕНЕНИЕ

                print(f"Найден файл: {filename}")
                # Нас интересуют только файлы, заканчивающиеся на .json
                if filename.endswith('.json') and not filename.startswith('.'):
                    # Извлекаем имя предмета из имени файла (например, 'biology.json' -> 'biology')
                    subject_name = filename.split('.')[0]
                    
                    # Собираем полный путь к файлу
                    file_path = os.path.join(questions_folder_path, filename) # <--- ИЗМЕНЕНИЕ
                    
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
                            local_subjects_data[subject_name] = sorted_questions
                            print(f"Предмет '{subject_name}' успешно загружен.")
                    except Exception as e:
                        print(f"Ошибка при загрузке файла {filename}: {e}")
        else:
            print(f"ВНИМАНИЕ: Папка '{questions_folder_path}' не найдена.")

        return local_subjects_data # <--- ИЗМЕНЕНИЕ


    def gambling(self, amount):
        self.balance += amount
        
    
    



    def get_new_card(self):
        card_cost = 100
        current_balance = self.balance

        if current_balance < card_cost:
            return (f"Необходимо еще {card_cost - current_balance} 💎")

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
        
        self.user_collection[card['name']] = card


        # Обновляем наш список ключей для пагинации
        self.collection_list = list(self.user_collection.keys())

        # Финальный приказ: "Комната, покажи эту карту!"
        print("--- Чекпойнт 5: App.__init__ ЗАВЕРШЕН ---")
        return card        
