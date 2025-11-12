import random 
import json
import os
import card_creator
import config


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

        self.all_subjects_data = self.load_questions(config.QUESTIONS_DIR) # <--- ИЗМЕНЕНИЕ

        print("--- Чекпойнт 2: Загрузка данных ЗАВЕРШЕНА ---")
        self.current_subject = None
        self.current_question = None

        self.language = None

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
                'image_path': 'inosuke1.png'},
                {'anime': 'Cowboy Bebop',
                'name': 'Spike Spiegel',
                'rarity': 'A',
                'image_path': 'Spike.png'},
                {'anime': 'Cowboy Bebop',
                'name': 'Faye Valentine',
                'rarity': 'B',
                'image_path': 'Valentine.png'},
                {'anime': 'Detective Conan',
                'name': 'Edogawa Conan',
                'rarity': 'A',
                'image_path': 'Conan.png'},
                {'anime': 'Belzebub',
                'name': 'Oga and Belze',
                'rarity': 'A',
                'image_path': 'beelzebub.png'},
                {'anime': 'Grand Blue',
                'name': 'Diving',
                'rarity': 'C',
                'image_path': 'Diving.png'},
                {'anime': 'AOT',
                'name': 'Erwin Smith',
                'rarity': 'A',
                'image_path': 'Erwin_Smith.png'},
                {'anime': 'Naruto',
                'name': 'Hinata Hyuga',
                'rarity': 'C',
                'image_path': 'Hinata.png'},
                {'anime': 'Naruto',
                'name': 'Jiraiya',
                'rarity': 'S',
                'image_path': 'Jiraya.png'},
                {'anime': 'Monster',
                'name': 'The Despair',
                'rarity': 'A',
                'image_path': 'Johan_Libert.png'},
                {'anime': 'Your Name',
                'name': 'Mitsuha',
                'rarity': 'B',
                'image_path': 'Mitsuha.png'},
                {'anime': 'OPM',
                'name': 'Saitama',
                'rarity': 'C',
                'image_path': 'Saitama.png'},
                {'anime': 'Grand Blue',
                'name': 'Diving',
                'rarity': 'B',
                'image_path': 'Diving.png'},
                {'anime': 'Spider Man',
                'name': 'Spider Team',
                'rarity': 'C',
                'image_path': 'Spider_team.png'},
                {'anime': 'Spider Man',
                'name': 'Peter Parker',
                'rarity': 'B',
                'image_path': 'Spider_man.png'}
                ]

            for card in self.all_cards:
                rarity = card['rarity']
                if rarity in self.sorted_cards:
                    self.sorted_cards[rarity].append(card)



    def get_subjects_for_language(self, lang):
        subjects = self.all_subjects_data.get(lang, {}) 
        questions = list(subjects.keys()) 
        return questions


    def subject_selected(self, subjects_name):
        self.current_subject = subjects_name
        return subjects_name

    def difficulty_selected(self, level):
        question = random.choice(self.all_subjects_data[self.language][self.current_subject][level.lower()])
    
        # 2. "Мозг, запомни: текущий вопрос - это вот этот словарь {...}"
        self.current_question = question
        
        # 3. Возвращаем вопрос, чтобы его можно было показать
        return question


    def check_answer(self, selected_option):
        correct = self.current_question['correct_answer']
        is_correct = (selected_option == correct)   
        
        if is_correct:
            if self.current_question['difficulty'] in ('легкий', 'easy'):
                self.gambling(210)
            if self.current_question['difficulty']  in ('средний', 'medium'):
                self.gambling(270)
            if self.current_question['difficulty']  in ('сложный', 'hard'):
                self.gambling(350)

        return is_correct




    



    def load_questions(self, questions_folder_path): # <--- ИЗМЕНЕНИЕ
        all_subjects_data  = {'en': {},
        'ru': {}} 
        supported_languages = ['ru', 'en']
        if not os.path.exists(questions_folder_path): # <--- ИЗМЕНЕНИЕ
            print(f"ВНИМАНИЕ: Папка '{questions_folder_path}' не найдена.")

        for lang in supported_languages:
            lang_folder_path = os.path.join(questions_folder_path, lang)
            print(f"Проверяю путь: {lang_folder_path}")
            for filename in os.listdir(lang_folder_path): # <--- ИЗМЕНЕНИЕ

                print(f"Найден файл: {filename}")
                # Нас интересуют только файлы, заканчивающиеся на .json
                if filename.endswith('.json') and not filename.startswith('.'):
                    # Извлекаем имя предмета из имени файла (например, 'biology.json' -> 'biology')
                    subject_name = filename.split('.')[0]
                    
                    # Собираем полный путь к файлу
                    file_path = os.path.join(lang_folder_path, filename)

                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            questions_list = json.load(f)
                            
                        sorted_questions = {}

                        # Проходим по каждому вопросу из файла
                        for q_data in questions_list:
                            # Получаем сложность, например, "легкий" или "easy"
                            difficulty = q_data['difficulty']
                            
                            # Проверяем, встречали ли мы такую сложность РАНЬШЕ
                            if difficulty not in sorted_questions:
                                # Если нет - создаем для нее новый пустой список
                                sorted_questions[difficulty] = []
                                
                            # Теперь, когда мы уверены, что список существует, добавляем туда вопрос
                            sorted_questions[difficulty].append(q_data)

                                                    
                            # Складываем отсортированные вопросы в наше общее хранилище
                        all_subjects_data[lang][subject_name] = sorted_questions
                        print(f"Предмет '{subject_name}' успешно загружен.")
                    except Exception as e:
                            print(f"Ошибка при загрузке файла {filename}: {e}")



        return all_subjects_data # <--- ИЗМЕНЕНИЕ


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
