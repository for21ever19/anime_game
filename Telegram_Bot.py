from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import io
import card_creator
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images_processed') # Предполагаю, что картинки в папке 'images'
FONTS_DIR = os.path.join(BASE_DIR, 'Fonts')
QUESTIONS_DIR = os.path.join(BASE_DIR, 'questions')

from class_App import App



class TelegramBot:
    def __init__(self):
        self.user_apps = {}
        bot_token = os.environ.get('BOT_TOKEN') 

        # Инициализируем бота, используя полученный токен

        self.application = Application.builder().token(bot_token).build()

        start_handler = CommandHandler('start', self.start)




    #registration
        self.application.add_handler(start_handler)

        button_handler = CallbackQueryHandler(self.button)
        self.application.add_handler(button_handler)



    def _create_main_menu_keyboard(self):
        quiz_button = InlineKeyboardButton (text = "Начать викторину", callback_data = 'start_quiz')
        card_button = InlineKeyboardButton (text = "Получить новую карту", callback_data = 'get_card')
        collection_button = InlineKeyboardButton (text = "Посмотреть коллекцию", callback_data = 'show_collection')
        keyboard = [[quiz_button], [card_button], [collection_button]]
        return InlineKeyboardMarkup(keyboard)
    
    def _create_back_to_main_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton("⬅️ Назад в Главное меню", callback_data='back_to_main_menu')]]
        return InlineKeyboardMarkup(keyboard)

    def _create_collection_pagination_keyboard(self, current_index, total_cards):
        keyboard = []
        row = []

        # Кнопка "Назад"
        if current_index > 0:
            row.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"collection_prev_{current_index - 1}"))
            
        # Индикатор страницы
        row.append(InlineKeyboardButton(f"{current_index + 1}/{total_cards}", callback_data="noop")) # noop - no operation

        # Кнопка "Вперед"
        if current_index < total_cards - 1:
            row.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"collection_next_{current_index + 1}"))
        
        keyboard.append(row)
        # Добавляем кнопку выхода в главное меню
        keyboard.append([InlineKeyboardButton("⬆️ В главное меню", callback_data='back_to_main_menu')])

        return InlineKeyboardMarkup(keyboard)








    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in self.user_apps:
            
            print(f"--- Создаю новый экземпляр App для пользователя {user_id} ---")
            self.user_apps[user_id] = App(questions_dir=QUESTIONS_DIR)

        app = self.user_apps[user_id]

        await update.message.reply_text(''' — Скажите, почему Вы решили стать учителем?
    — И правда, почему?
    — Вы что, решили стать учителем просто так?
    — Помолчи, а? Тебе-то что? Если нужна причина — ну по приколу. ''')
    

        
        reply_markup1 = self._create_main_menu_keyboard()

        
        await update.message.reply_text(f"Главное меню\n\nВаш баланс: {app.balance} 💎", reply_markup=reply_markup1)


################
    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in self.user_apps:
            print(f"--- Создаю новый экземпляр App для пользователя {user_id} ---")
            self.user_apps[user_id] = App(questions_dir=QUESTIONS_DIR)

        app = self.user_apps[user_id]


        query = update.callback_query
        await query.answer()

        if query.data == 'start_quiz':
            subjects = app.all_subjects_data.keys()

            keyboard = []

            for subject in subjects:
                button = InlineKeyboardButton(
                    text=subject.title(), 
                    callback_data=f"subject_{subject.lower()}" 
                )

                keyboard.append([button])
            

            back_button_row = [InlineKeyboardButton("⬅️ Назад в Главное меню", callback_data='back_to_main_menu')]
            keyboard.append(back_button_row)

            subjects_keyboard = InlineKeyboardMarkup(keyboard)



            await query.edit_message_text(
                text="Какая тема тебе интересна?",
                reply_markup=subjects_keyboard
            )

        elif query.data == 'get_card':
            card_result = app.get_new_card()
            if isinstance(card_result, str):
                reply_markup1 = self._create_main_menu_keyboard()


                await query.edit_message_text(text = card_result, reply_markup=reply_markup1)
            
            else:
                image_object = card_creator.create_card_image(card_result, images_dir=IMAGES_DIR, fonts_dir=FONTS_DIR)
                bio = io.BytesIO()
                bio.name = 'image.png'
                image_object.save(bio, 'PNG')
                bio.seek(0)

                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ В главное меню", callback_data='back_to_main_menu')]])
                await context.bot.send_photo(
    chat_id=user_id,      # ID чата, куда отправляем
    photo=bio,            # Наш "виртуальный файл" с картинкой      # Текст подписи
    reply_markup=reply_markup # Наша клавиатура
)

                

        elif query.data.startswith('subject_'):
            selected_subject = query.data[8:]
            app.subject_selected(selected_subject)

            difficulty = ["Легкий", "Средний", "Сложный"]

            keyboard = []

            for levels in difficulty:
                button = InlineKeyboardButton(
                    text=levels, 
                    callback_data=f"difficulty_{levels.lower()}" 
                )

                keyboard.append([button])
            
            back_button = InlineKeyboardButton("⬅️ Назад к предметам", callback_data='back_to_subjects')
            keyboard.append([back_button])


            difficulty_keyboard = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text=f"Вы выбрали предмет: {selected_subject.capitalize()}. Теперь выберите сложность.",
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
            back_to_menu_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ В главное меню", callback_data='back_to_main_menu')]])

            current_index = int(query.data[7:])
            selected_answer = app.current_question['options'][current_index]
            is_correct = app.check_answer(selected_answer)
            if is_correct:
                await query.edit_message_text(text=f'Верно! ✅\n\nВаш баланс: {app.balance} 💎', reply_markup=back_to_menu_keyboard)

            else:
                await query.edit_message_text(text= 'Неверно! ❌', reply_markup=back_to_menu_keyboard)





        
        elif query.data == 'back_to_subjects': 
            subjects = app.all_subjects_data.keys()

            keyboard = []

            for subject in subjects:
                button = InlineKeyboardButton(
                    text=subject.title(), 
                    callback_data=f"subject_{subject.lower()}" 
                )

                keyboard.append([button])
            

            back_button_row = [InlineKeyboardButton("⬅️ Назад в Главное меню", callback_data='back_to_main_menu')]
            keyboard.append(back_button_row)

            # 2. Теперь, когда список `keyboard` полностью готов, создаем из него объект клавиатуры
            subjects_keyboard = InlineKeyboardMarkup(keyboard)


            await query.edit_message_text(
                text="Какая тема тебе интересна?",
                reply_markup=subjects_keyboard
            )

        elif query.data == 'back_to_main_menu':


            reply_markup1 = self._create_main_menu_keyboard()
            

            await query.edit_message_text(
                text = f"Главное меню\n\nВаш баланс: {app.balance} 💎",
                reply_markup = reply_markup1
            )



        elif query.data == 'show_collection':
            collection = app.user_collection
            if not collection:
                back_keyboard = self._create_back_to_main_menu_keyboard()



                await query.edit_message_text(text= 'Ваша колекция пуста.', reply_markup=back_keyboard)
            
            else:
                # 1. Подготовим данные
                app.current_collection_index = 0
                card_name = app.collection_list[app.current_collection_index]
                card_data = collection[card_name]
                total_cards = len(collection)

                # 2. Подготовим картинку (твой код идеален)
                image_object = card_creator.create_card_image(card_data, images_dir=IMAGES_DIR, fonts_dir=FONTS_DIR)
                bio = io.BytesIO()
                bio.name = 'image.png'
                image_object.save(bio, 'PNG')
                bio.seek(0)

                
                # 4. Подготовим клавиатуру
                pagination_keyboard = self._create_collection_pagination_keyboard(app.current_collection_index, total_cards)



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
            image_object = card_creator.create_card_image(card_data, images_dir=IMAGES_DIR, fonts_dir=FONTS_DIR)
            bio = io.BytesIO()
            bio.name = 'image.png'
            image_object.save(bio, 'PNG')
            bio.seek(0)

            
            # 4. Подготовим клавиатуру
            pagination_keyboard = self._create_collection_pagination_keyboard(app.current_collection_index, total_cards)


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
            image_object = card_creator.create_card_image(card_data, images_dir=IMAGES_DIR, fonts_dir=FONTS_DIR)
            bio = io.BytesIO()
            bio.name = 'image.png'
            image_object.save(bio, 'PNG')
            bio.seek(0)

            
            # 4. Подготовим клавиатуру
            pagination_keyboard = self._create_collection_pagination_keyboard(app.current_collection_index, total_cards)



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
