from datetime import datetime
from sqlalchemy import desc, func

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

from db import session
from config import (END, FIRST, HELP, logger, DOWNLOAD_START, DOWNLOAD_END, LAST_SELFIE_START,
                    SCHOOL_PHOTO_START, STORY_START, GPT_START, BASES_START, FIRST_LOVE_START, LAST_SELFIE_END,
                    SCHOOL_PHOTO_END, STORY_END, GPT_END, BASES_END, FIRST_LOVE_END, OWNER_LOGIN)
from models import User, ContentType, Category, History, Document

USER_BASE = {}


def start(update, context):
    """Стартовый диалог. Автоматически запоминает пользователя"""
    try:
        login = update.message.from_user.name
        old_user = session.query(User).filter(User.login == login).first()
        if old_user is None:
            new_user = User(
                login=login,
                name=update.message.from_user.full_name,
                created_at=datetime.now()
            )
            session.add(new_user)
            session.commit()
        logger.info(f'{login} >>> Начал сеанс')
        categories = session.query(Category).all()
        keyboard = [
            [
                InlineKeyboardButton(categories[0].name, callback_data=str(LAST_SELFIE_START)),
                InlineKeyboardButton(categories[1].name, callback_data=str(SCHOOL_PHOTO_START)),
            ],
            [
                InlineKeyboardButton(categories[2].name, callback_data=str(STORY_START)),
                InlineKeyboardButton(categories[3].name, callback_data=str(GPT_START)),
            ],
            [
                InlineKeyboardButton(categories[4].name, callback_data=str(BASES_START)),
                InlineKeyboardButton(categories[5].name, callback_data=str(FIRST_LOVE_START)),
            ],
            [
                InlineKeyboardButton("🆘 Справка", callback_data=str(HELP))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"🦾 Приветствую, *{update.message.from_user.first_name}*! "
            f"Я бот для знакомства со мной(автором бота).\n"
            f"Ты можешь узнать информацию обо мне, а также загрузить что-то о себе, чтобы мы лучше познакомились \n\n"
            f"Выберите на клавиатуре, что вы сейчас хотите 👇", reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def stop(update, context):
    """Принудительный выход из диалога по команде /stop"""
    try:
        name = str(update.message.from_user.name)
        update.message.reply_text(f'🖖 Всего доброго, {update.message.from_user.first_name}! \n'
                                  f'Если захотите продолжить, нажмите или напишите /start')
        logger.info(f'{name} >>> /stop')
    except Exception as e:
        logger.error(f'{e}')
    return ConversationHandler.END


def end(update, context):
    """Плановый выход из диалога по кнопке "Хватит" """
    try:
        query = update.callback_query
        query.answer()
        name = str(query.from_user.name)
        query.edit_message_text(text=f'🖖 Всего доброго, {query.from_user.first_name}! \n'
                                     f'Если захотите продолжить, нажмите или напишите /start')
        logger.info(f'{name} >>> Закончил сеанс')
    except Exception as e:
        logger.error(f'{e}')
    return ConversationHandler.END


def get_standard_keyboard():
    categories = session.query(Category).all()

    keyboard = [
        [
            InlineKeyboardButton(categories[0].name, callback_data=str(LAST_SELFIE_START)),
            InlineKeyboardButton(categories[1].name, callback_data=str(SCHOOL_PHOTO_START)),
        ],
        [
            InlineKeyboardButton(categories[2].name, callback_data=str(STORY_START)),
            InlineKeyboardButton(categories[3].name, callback_data=str(GPT_START)),
        ],
        [
            InlineKeyboardButton(categories[4].name, callback_data=str(BASES_START)),
            InlineKeyboardButton(categories[5].name, callback_data=str(FIRST_LOVE_START)),
        ],
        [
            InlineKeyboardButton("🆘 Справка", callback_data=str(HELP)),
            InlineKeyboardButton("💔 Хватит", callback_data=str(END))

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def draw_keyboard(update):
    """Рисуем клавиатуру с меню"""
    reply_markup = get_standard_keyboard()
    try:
        update.message.reply_text(text="👇 Выбирайте снова 👇", reply_markup=reply_markup)
    except AttributeError as e:
        logger.error(f'{e}')
        update.callback_query.edit_message_text(text="👇 Выбирайте снова 👇", reply_markup=reply_markup)


def github(update, context):
    """Возвращаем ссылку на исходники. Тригер на /github"""
    try:
        update.message.reply_text(
            text="Посмотреть из чего я состою на [github](https://github.com/AlexeyTeacher/test_bot)",
            parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    draw_keyboard(update)
    return FIRST


def run_download(update, context):
    """Первый этап загрузки контента. Предлагает выбрать тип контента и категорию. Тригер на /download"""
    categories = (session.query(
        Category.id, Category.name, ContentType.name
    ).join(ContentType, Category.content_type_id == ContentType.id).all())
    text_categories = '\n'.join([f'`{c[0]}`. {c[1]} / _({c[2]})_' for c in categories])
    try:
        update.message.reply_text(
            text=f"Напишите *числом* номер категории, чтобы можно было начать загрузку своих данных:\n{text_categories}",
            parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return DOWNLOAD_START


def download_start(update, context):
    """Второй этап загрузки контента. Дает загрузить сам контент."""
    category_id = update.message.text.strip().replace('№', '')
    category = session.query(Category.name, ContentType.name, ContentType.slug
                             ).join(ContentType, Category.content_type_id == ContentType.id
                                    ).filter(Category.id == int(category_id)).first()
    update.message.reply_text(
        text=f"Загрузите свое *{category[1].lower()}* на тему: *{category[0]}*",
        parse_mode='Markdown')

    USER_BASE[str(update.message.from_user.name)] = {"last_command": category_id}
    return DOWNLOAD_END


def download_end(update, context):
    """Третий этап загрузки контента. Обрабатывает и загружает контент в систему"""
    login = str(update.message.from_user.name)
    user = session.query(User).filter(User.login == login).first()
    category_id = USER_BASE.get(user.login, {}).get('last_command')

    category = session.query(Category.name, ContentType.name, ContentType.slug
                             ).join(ContentType, Category.content_type_id == ContentType.id
                                    ).filter(Category.id == int(category_id)).first()
    try:
        if category[2] == "image":
            photo = update.message.photo[-1]
            photo_file = photo.get_file()
            filename = 'documents/{}.png'.format(photo.file_id)
            photo_file.download(filename)
            update.message.reply_text('Фото сохранено.')
            new_doc = Document(
                user_id=user.id,
                category_id=category_id,
                name=f"{category[0]} от {user.name}",
                filename=filename
            )
        elif category[2] == "voice":
            voice = update.message.voice
            file_id = voice.file_id
            file = context.bot.get_file(file_id)
            filename = 'documents/{}.ogg'.format(voice.file_id)
            file.download(filename)
            update.message.reply_text('Голосовое сообщение сохранено.')

            new_doc = Document(
                user_id=user.id,
                category_id=category_id,
                name=f"{category[0]} от {user.name}",
                filename=filename
            )
        else:
            text = update.message.text.strip()
            new_doc = History(
                user_id=user.id,
                category_id=category_id,
                name=f"{category[0]} от {user.name}",
                description=text
            )
        session.add(new_doc)
        session.commit()
        draw_keyboard(update)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def _run_standard(update, category_name):
    query = update.callback_query
    query.answer()
    query.edit_message_text(f'Напишите *числом* тип ответа по теме: {category_name}\n'
                            f'*Возможные типы ответа:*\n'
                            f'1. Контент автора бота\n'
                            f'2. Контент пользователя бота\n'
                            f'3. Контент случайного пользователя\n',
                            parse_mode='Markdown')


def _get_content(update, context, content_type, variant_answer_num, category_id):
    chat_id = update.message.chat_id
    if content_type == 'image':
        if variant_answer_num == '1':
            user = session.query(User).filter(User.login == OWNER_LOGIN).first()
            photo_path = session.query(Document.filename).filter(
                Document.user_id == user.id, Document.category_id == category_id
            ).order_by(desc(Document.created_at)).first()[0]
        elif variant_answer_num == '2':
            login = update.message.from_user.name
            user = session.query(User).filter(User.login == login).first()
            photo_path = session.query(Document.filename).filter(
                Document.user_id == user.id, Document.category_id == category_id
            ).order_by(desc(Document.created_at)).first()
            if photo_path is None:
                update.message.reply_text("Вы еще не загрузили свое фото")
                return
            else:
                photo_path = photo_path[0]
        else:
            photo_path = session.query(Document.filename
                                       ).filter(Document.category_id == category_id).order_by(func.random()).first()[0]
        context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
    elif content_type == 'text':
        if variant_answer_num == '1':
            user = session.query(User).filter(User.login == OWNER_LOGIN).first()
            history = session.query(History).filter(
                History.user_id == user.id, History.category_id == category_id
            ).order_by(desc(History.created_at)).first()
        elif variant_answer_num == '2':
            login = update.message.from_user.name
            user = session.query(User).filter(User.login == login).first()
            history = session.query(History).filter(
                History.user_id == user.id, History.category_id == category_id
            ).order_by(desc(History.created_at)).first()
            if history is None:
                update.message.reply_text("Вы еще не загрузили свой текст")
                return
        else:
            history = session.query(History).filter(History.category_id == category_id).order_by(func.random()).first()
        update.message.reply_text(f"*{history.name}*\n"
                                  f"{history.description}", parse_mode='Markdown')
        if content_type == 'image':
            if variant_answer_num == '1':
                user = session.query(User).filter(User.login == OWNER_LOGIN).first()
                photo_path = session.query(Document.filename).filter(
                    Document.user_id == user.id, Document.category_id == category_id
                ).order_by(desc(Document.created_at)).first()[0]
            elif variant_answer_num == '2':
                login = update.message.from_user.name
                user = session.query(User).filter(User.login == login).first()
                photo_path = session.query(Document.filename).filter(
                    Document.user_id == user.id, Document.category_id == category_id
                ).order_by(desc(Document.created_at)).first()
                if photo_path is None:
                    update.message.reply_text("Вы еще не загрузили свое фото")
                    return
                else:
                    photo_path = photo_path[0]
            else:
                photo_path = session.query(Document.filename
                                           ).filter(Document.category_id == category_id).order_by(
                    func.random()).first()[0]
            context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
    if content_type == 'voice':
        if variant_answer_num == '1':
            user = session.query(User).filter(User.login == OWNER_LOGIN).first()
            voice_path = session.query(Document.filename).filter(
                Document.user_id == user.id, Document.category_id == category_id
            ).order_by(desc(Document.created_at)).first()[0]
        elif variant_answer_num == '2':
            login = update.message.from_user.name
            user = session.query(User).filter(User.login == login).first()
            voice_path = session.query(Document.filename).filter(
                Document.user_id == user.id, Document.category_id == category_id
            ).order_by(desc(Document.created_at)).first()
            if voice_path is None:
                update.message.reply_text("Вы еще не загрузили свое фото")
                return
            else:
                voice_path = voice_path[0]
        else:
            voice_path = session.query(Document.filename
                                       ).filter(Document.category_id == category_id).order_by(func.random()).first()[0]
        context.bot.send_voice(chat_id=chat_id, voice=open(voice_path, 'rb'))


def run_selfie(update, context):
    """Кнопка Селфи"""
    try:
        category_name = session.query(Category.name).filter(Category.slug == 'last_selfie').first()[0]
        _run_standard(update, category_name)
    except Exception as e:
        logger.error(f'{e}')
    return LAST_SELFIE_END


def selfie(update, context):
    """Возвращает селфи пользователя или админа"""
    variant = update.message.text.strip().replace('№', '')
    category_id = session.query(Category.id).filter(Category.slug == 'last_selfie').first()[0]
    try:
        _get_content(update, context, content_type='image', variant_answer_num=variant, category_id=category_id)
    except Exception as e:
        logger.error(f'{e}')
    draw_keyboard(update)
    return FIRST


def run_school_photo(update, context):
    """Кнопка Школьное фото"""
    try:
        category_name = session.query(Category.name).filter(Category.slug == 'school_photo').first()[0]
        _run_standard(update, category_name)
    except Exception as e:
        logger.error(f'{e}')
    return SCHOOL_PHOTO_END


def school_photo(update, context):
    """Возвращает Школьное фото пользователя или админа"""
    variant = update.message.text.strip().replace('№', '')
    category_id = session.query(Category.id).filter(Category.slug == 'school_photo').first()[0]
    try:
        _get_content(update, context, content_type='image', variant_answer_num=variant, category_id=category_id)
    except Exception as e:
        logger.error(f'{e}')
    draw_keyboard(update)
    return FIRST


def run_story(update, context):
    """Кнопка Главное увлечение"""
    try:
        category_name = session.query(Category.name).filter(Category.slug == 'school_photo').first()[0]
        _run_standard(update, category_name)
    except Exception as e:
        logger.error(f'{e}')
    return STORY_END


def story(update, context):
    """Возвращает Главное увлечение пользователя или админа"""
    variant = update.message.text.strip().replace('№', '')
    category_id = session.query(Category.id).filter(Category.slug == 'story').first()[0]
    try:
        _get_content(update, context, content_type='text', variant_answer_num=variant, category_id=category_id)
    except Exception as e:
        logger.error(f'{e}')
    draw_keyboard(update)
    return FIRST


def run_gpt(update, context):
    """Кнопка GPT """
    try:
        category_name = session.query(Category.name).filter(Category.slug == 'gpt').first()[0]
        _run_standard(update, category_name)
    except Exception as e:
        logger.error(f'{e}')
    return GPT_END


def gpt(update, context):
    """Возвращает GPT пользователя или админа"""
    variant = update.message.text.strip().replace('№', '')
    category_id = session.query(Category.id).filter(Category.slug == 'gpt').first()[0]
    try:
        _get_content(update, context, content_type='voice', variant_answer_num=variant, category_id=category_id)
    except Exception as e:
        logger.error(f'{e}')
    draw_keyboard(update)
    return FIRST


def run_bases(update, context):
    """Кнопка Разница в БД"""
    try:
        category_name = session.query(Category.name).filter(Category.slug == 'bases').first()[0]
        _run_standard(update, category_name)
    except Exception as e:
        logger.error(f'{e}')
    return BASES_END


def bases(update, context):
    """Возвращает Разницу в БД пользователя или админа"""
    variant = update.message.text.strip().replace('№', '')
    category_id = session.query(Category.id).filter(Category.slug == 'bases').first()[0]
    try:
        _get_content(update, context, content_type='voice', variant_answer_num=variant, category_id=category_id)
    except Exception as e:
        logger.error(f'{e}')
    draw_keyboard(update)
    return FIRST


def run_first_love(update, context):
    """Кнопка Первая любовь"""
    try:
        category_name = session.query(Category.name).filter(Category.slug == 'first_love').first()[0]
        _run_standard(update, category_name)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST_LOVE_END


def first_love(update, context):
    """Возвращает "Первую любовь" пользователя или админа"""
    variant = update.message.text.strip().replace('№', '')
    category_id = session.query(Category.id).filter(Category.slug == 'first_love').first()[0]
    try:
        _get_content(update, context, content_type='voice', variant_answer_num=variant, category_id=category_id)
    except Exception as e:
        logger.error(f'{e}')
    draw_keyboard(update)
    return FIRST


def help_(update, context):
    """Справка"""
    categories = session.query(Category).all()

    keyboard = [
        [
            InlineKeyboardButton(categories[0].name, callback_data=str(LAST_SELFIE_START)),
            InlineKeyboardButton(categories[1].name, callback_data=str(SCHOOL_PHOTO_START)),
        ],
        [
            InlineKeyboardButton(categories[2].name, callback_data=str(STORY_START)),
            InlineKeyboardButton(categories[3].name, callback_data=str(GPT_START)),
        ],
        [
            InlineKeyboardButton(categories[4].name, callback_data=str(BASES_START)),
            InlineKeyboardButton(categories[5].name, callback_data=str(FIRST_LOVE_START)),
        ],
        [
            InlineKeyboardButton("💔 Хватит", callback_data=str(END))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    query.answer()
    task = """✅ Напиши на Python бота для Телеграм, который поможет нам с тобой познакомиться, задеплой его и пришли ссылку на работающего бота.
Функционал бота:
- посмотреть 1. твое последнее селфи и 2. фото из старшей школы
- прочитать небольшой пост о твоём главном увлечении
- прислать твой войс:
    - с рассказом в формате «объясняю своей бабушке», что такое GPT (до 1 минуты)
    - и максимально коротко объясни разницу между SQL и NoSQL (до 1 минуты)
    - история первой любви (до 1 минуты) — можно выдумать 🤫
Кроме этого, нужна команда, которая позволит получить нам ссылку на публичный репозиторий с исходниками этого бота.
Сделай часть команд кнопками, а часть — текстом.
"""
    text = f"*Привет!*\n" \
           f"Бот по тестовому заданию для Яндекс Практикум\n" \
           f"*Задание*\n" \
           f"```\n{task}\n```" \
           f"*Помимо кнопок есть текстовые команды:*\n" \
           f"/start - запускает бота после остановки\n" \
           f"/github - Получить исходники бота\n" \
           f"/download - Загрузить свой контент\n" \
           f"/stop - принудительно завершает работу бота"

    query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
