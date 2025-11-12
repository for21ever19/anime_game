from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import io
import card_creator
import os
import localization
import i18n
import os
import config



from class_App import App



class TelegramBot:
    def __init__(self):
        self.language = None

        self.user_apps = {}
        bot_token = os.environ.get('BOT_TOKEN') 

        self.main_menu_message_id = None

        # Инициализируем бота, используя полученный токен

        self.application = Application.builder().token(bot_token).build()

        start_handler = CommandHandler('start', self.start)




    #registration
        self.application.add_handler(start_handler)

        button_handler = CallbackQueryHandler(self.button)
        self.application.add_handler(button_handler)


    def _create_i18_keyboard(self):
        ru_button = InlineKeyboardButton (text = "Русский 🇷🇺", callback_data = 'ru')
        en_button = InlineKeyboardButton (text = "English 🇬🇧", callback_data = 'en')
        keyboard = [[ru_button], [en_button]]
        return InlineKeyboardMarkup(keyboard)
    
    def _create_main_menu_keyboard(self, language: str):
        print(f"--- DEBUG: Создаю клавиатуру. Переданный язык: '{language}' ---")

        quiz_button = InlineKeyboardButton (text = localization.get_string(language, 'start_quiz_button'), callback_data = 'start_quiz')
        card_button = InlineKeyboardButton (text = localization.get_string(language, 'get_card_button'), callback_data = 'get_card')
        collection_button = InlineKeyboardButton (text = localization.get_string(language, 'show_collection_button'), callback_data = 'show_collection')
        keyboard = [[quiz_button], [card_button], [collection_button]]
        return InlineKeyboardMarkup(keyboard)
    
    def _create_back_to_main_menu_keyboard(self, language: str):
        keyboard = [[InlineKeyboardButton(localization.get_string(language, 'back_to_menu'), callback_data='back_to_main_menu')]]
        return InlineKeyboardMarkup(keyboard)

    def _create_collection_pagination_keyboard(self, current_index, total_cards, language: str):
        keyboard = []
        row = []

        # Кнопка "Назад"
        if current_index > 0:
            row.append(InlineKeyboardButton(localization.get_string(language, 'collection_back_button'), callback_data=f"collection_prev_{current_index - 1}"))
            
        # Индикатор страницы
        row.append(InlineKeyboardButton(f"{current_index + 1}/{total_cards}", callback_data="noop")) # noop - no operation

        # Кнопка "Вперед"
        if current_index < total_cards - 1:
            row.append(InlineKeyboardButton(localization.get_string(language, 'collection_forward_button'), callback_data=f"collection_next_{current_index + 1}"))
        
        keyboard.append(row)
        # Добавляем кнопку выхода в главное меню
        keyboard.append([InlineKeyboardButton(localization.get_string(language, 'back_to_menu'), callback_data='back_to_main_menu')])

        return InlineKeyboardMarkup(keyboard)








    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in self.user_apps:
            
            print(f"--- Создаю новый экземпляр App для пользователя {user_id} ---")
            self.user_apps[user_id] = App(questions_dir=config.QUESTIONS_DIR)


        await update.message.reply_text(''' — Скажите, почему Вы решили стать учителем?
    — И правда, почему?
    — Вы что, решили стать учителем просто так?
    — Помолчи, а? Тебе-то что? Если нужна причина — ну по приколу. ''')
    

        text = "Выберите язык / Choose your language"
        reply_markup = self._create_i18_keyboard()
             # Твоя функция для кнопок ru/en

        await update.message.reply_text(text, reply_markup=reply_markup)




################
    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in self.user_apps:
            print(f"--- Создаю новый экземпляр App для пользователя {user_id} ---")
            self.user_apps[user_id] = App(questions_dir=config.QUESTIONS_DIR)

        app = self.user_apps[user_id]
        language = app.language
        query = update.callback_query

        if not language and query.data not in ['ru', 'en']:
            await query.answer("Пожалуйста, выберите язык, отправив команду /start", show_alert=True)
            return


        await query.answer()

        if query.data in ['ru', 'en']:
            app.language = query.data # Сохраняем выбранный язык ('ru' или 'en')
            print(f"Пользователь {user_id} выбрал язык: {app.language}")
            text = localization.get_string(app.language, 'main_menu_title') + "\n\n"
            text += localization.get_string(app.language, 'balance_text', balance=app.balance)

            # Клавиатуру тоже нужно сделать локализованной
            reply_markup = self._create_main_menu_keyboard(app.language) # Передаем язык в метод

            # Заменяем сообщение "Выберите язык" на Главное Меню
            sent_message = await query.edit_message_text(text=text, reply_markup=reply_markup)
            
            # И СОХРАНЯЕМ ID НАШЕГО "ЯКОРЯ"!
            app.main_menu_message_id = sent_message.message_id
            return


        if query.data == 'start_quiz':
            subjects = app.get_subjects_for_language(app.language)
            keyboard = []

            for subject in subjects:
                button = InlineKeyboardButton(
                    text=subject.title(), 
                    callback_data=f"subject_{subject.lower()}" 
                )

                keyboard.append([button])
            

            back_button_row = [InlineKeyboardButton(localization.get_string(language, 'back_to_menu'), callback_data='back_to_main_menu')]
            keyboard.append(back_button_row)

            subjects_keyboard = InlineKeyboardMarkup(keyboard)



            await query.edit_message_text(
                text=localization.get_string(language, 'ask_subject'),
                reply_markup=subjects_keyboard
            )

        elif query.data == 'get_card':
            card_result = app.get_new_card()
            if isinstance(card_result, str):
                reply_markup1 = self._create_main_menu_keyboard(language)


                await query.edit_message_text(text = card_result, reply_markup=reply_markup1)
            
            else:
                image_object = card_creator.create_card_image(card_result, images_dir=config.IMAGES_DIR, fonts_dir=config.FONTS_DIR)
                bio = io.BytesIO()
                bio.name = 'image.png'
                image_object.save(bio, 'PNG')
                bio.seek(0)

                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(localization.get_string(language, 'back_to_menu'), callback_data='back_to_main_menu')]])
                await context.bot.send_photo(
    chat_id=user_id,      # ID чата, куда отправляем
    photo=bio,            # Наш "виртуальный файл" с картинкой      # Текст подписи
    reply_markup=reply_markup # Наша клавиатура
)

                

        elif query.data.startswith('subject_'):
            selected_subject = query.data[8:]
            app.subject_selected(selected_subject)

            # 1. Наш словарь-переходник. Все верно.
            difficulties = {
                'easy': 'easy_dif',
                'medium': 'mid_dif',
                'hard': 'diff_dif'
            }

            keyboard = []

            # 2. Цикл для создания кнопок. Все верно.
            for key, loc_key in difficulties.items():
                button_text = localization.get_string(language, loc_key)
                button_callback = f"difficulty_{key}"
                
                button = InlineKeyboardButton(
                    text=button_text, 
                    callback_data=button_callback
                )
                keyboard.append([button])
            
            # --- ВОТ ЧТО БЫЛО ПРОПУЩЕНО ---
            
            # 3. Добавляем кнопку "Назад" (она тоже должна быть локализована)
            back_button = InlineKeyboardButton(localization.get_string(language, 'back_to_subjects_button'), callback_data='back_to_subjects')
            keyboard.append([back_button])

            # 4. Создаем из нашего списка объект клавиатуры
            difficulty_keyboard = InlineKeyboardMarkup(keyboard)

            # 5. Отправляем сообщение с текстом и готовой клавиатурой
            subject_name = selected_subject.capitalize()
            await query.edit_message_text(
                text=localization.get_string(language, 'select_difficulty_text', subject = subject_name),
                reply_markup=difficulty_keyboard
            )
            
        elif query.data.startswith('difficulty_'):
            selected_difficulty = query.data[11:] 
            question_data = app.difficulty_selected(selected_difficulty)

            keyboard = []

            for index, option in enumerate(question_data['options']):
                button = InlineKeyboardButton(
                    text=option, 
                    callback_data=f"answer_{index}" 
                )

                keyboard.append([button])

            oprions_keyboard = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text=question_data['question'],
                reply_markup=oprions_keyboard
            )


        elif query.data.startswith('answer_'):
            back_to_menu_keyboard = self._create_back_to_main_menu_keyboard(language)

            current_index = int(query.data[7:])
            selected_answer = app.current_question['options'][current_index]
            is_correct = app.check_answer(selected_answer)
            if is_correct:
                await query.edit_message_text(text=localization.get_string(language, 'correct_answer', balance=app.balance), reply_markup=back_to_menu_keyboard)

            else:
                await query.edit_message_text(text= localization.get_string(language, 'incorrect_answer'), reply_markup=back_to_menu_keyboard)





        
        elif query.data == 'back_to_subjects': 
            subjects = app.all_subjects_data.keys()

            keyboard = []

            for subject in subjects:
                button = InlineKeyboardButton(
                    text=subject.title(), 
                    callback_data=f"subject_{subject.lower()}" 
                )

                keyboard.append([button])
            

            back_button_row = [InlineKeyboardButton(localization.get_string(language, 'back_to_menu'), callback_data='back_to_main_menu')]
            keyboard.append(back_button_row)

            # 2. Теперь, когда список `keyboard` полностью готов, создаем из него объект клавиатуры
            subjects_keyboard = InlineKeyboardMarkup(keyboard)


            await query.edit_message_text(
                text=localization.get_string(language, 'ask_subject'),
                reply_markup=subjects_keyboard
            )

        elif query.data == 'back_to_main_menu':



            reply_markup1 = self._create_main_menu_keyboard(language)
            text = localization.get_string(language, 'main_menu_full_text', balance=app.balance)

            # Проверяем, есть ли у сообщения, с которого пришел запрос, фотография
            if not query.message.photo:
                # СЛУЧАЙ 1: Возврат из текстового меню (например, выбор предметов)
                # Просто редактируем это же сообщение
                await query.edit_message_text(text=text, reply_markup=reply_markup1)
                # И на всякий случай обновляем ID якоря (вдруг что)
                app.main_menu_message_id = query.message.message_id
                print(f"Обновил текстовое меню. ID якоря: {app.main_menu_message_id}")

            else:
                # СЛУЧАЙ 2: Возврат из-под картинки (самое интересное!)
                
                # Шаг А: Удаляем сообщение с картинкой, на котором нажали кнопку
                await query.message.delete()
                
                # Шаг Б: Пытаемся удалить СТАРОЕ главное меню, используя сохраненный ID.
                # Это нужно делать в try/except, т.к. пользователь мог удалить его вручную.
                try:
                    if app.main_menu_message_id:
                        await context.bot.delete_message(chat_id=user_id, message_id=app.main_menu_message_id)
                        print(f"Удалил старый якорь {app.main_menu_message_id}")
                except Exception as e:
                    print(f"Не смог удалить старый якорь (возможно, его уже нет): {e}")

                # Шаг В: Отправляем НОВОЕ главное меню
                new_menu_message = await context.bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=reply_markup1
                )
                
                # Шаг Г: Сохраняем ID НОВОГО якоря!
                app.main_menu_message_id = new_menu_message.message_id
                print(f"Создал новый якорь. ID: {app.main_menu_message_id}")





        elif query.data == 'show_collection':
            collection = app.user_collection
            if not collection:
                back_keyboard = self._create_back_to_main_menu_keyboard(language)



                await query.edit_message_text(text= localization.get_string(language, 'empty_collection'), reply_markup=back_keyboard)
            
            else:
                # 1. Подготовим данные
                app.current_collection_index = 0
                card_name = app.collection_list[app.current_collection_index]
                card_data = collection[card_name]
                total_cards = len(collection)

                # 2. Подготовим картинку 
                image_object = card_creator.create_card_image(card_data, images_dir=config.IMAGES_DIR, fonts_dir=config.FONTS_DIR)
                bio = io.BytesIO()
                bio.name = 'image.png'
                image_object.save(bio, 'PNG')
                bio.seek(0)

                
                # 4. Подготовим клавиатуру
                pagination_keyboard = self._create_collection_pagination_keyboard(app.current_collection_index, total_cards, language)



                # 5. Сначала удалим старое текстовое сообщение
                await query.message.delete()

                # 6. Отправим новое с фото и всеми подготовленными частями
                await context.bot.send_photo(
                    chat_id=user_id,
                    photo=bio,
                    reply_markup=pagination_keyboard
                )


        elif query.data.startswith('collection_next_'):
            collection = app.user_collection
            total_cards = len(collection)

            new_index = int(query.data[16:]) # Тут тоже 16 символов, но см. ниже
            app.current_collection_index = new_index

            card_name = app.collection_list[app.current_collection_index]
            card_data = collection[card_name]


            # 2. Подготовим картинку (твой код идеален)
            image_object = card_creator.create_card_image(card_data, images_dir=config.IMAGES_DIR, fonts_dir=config.FONTS_DIR)
            bio = io.BytesIO()
            bio.name = 'image.png'
            image_object.save(bio, 'PNG')
            bio.seek(0)

            
            # 4. Подготовим клавиатуру
            pagination_keyboard = self._create_collection_pagination_keyboard(app.current_collection_index, total_cards, language)


            media = InputMediaPhoto(media=bio) # Оборачиваем картинку в специальный класс
            # 5. Изменим фотографию
            await query.edit_message_media(
                media=media,
                reply_markup=pagination_keyboard
            )


        elif query.data.startswith('collection_prev_'):
            collection = app.user_collection
            total_cards = len(collection)
            new_index = int(query.data[16:]) 
            app.current_collection_index = new_index

            card_name = app.collection_list[app.current_collection_index]
            card_data = collection[card_name]


            # 2. Подготовим картинку (твой код идеален)
            image_object = card_creator.create_card_image(card_data, images_dir=config.IMAGES_DIR, fonts_dir=config.FONTS_DIR)
            bio = io.BytesIO()
            bio.name = 'image.png'
            image_object.save(bio, 'PNG')
            bio.seek(0)

            
            # 4. Подготовим клавиатуру
            pagination_keyboard = self._create_collection_pagination_keyboard(app.current_collection_index, total_cards, language)



            media = InputMediaPhoto(media=bio) # Оборачиваем картинку в специальный класс
            # 5. Изменим фотографию
            await query.edit_message_media(
                media=media,
                reply_markup=pagination_keyboard
            )






    def run(self):
        print("Бот запущен...")
        self.application.run_polling()
        print("Бот остановлен.")



def main():
    bot = TelegramBot()
    bot.run()
    
# Стандартная конструкция для запуска main функции
if __name__ == '__main__':
    main()
