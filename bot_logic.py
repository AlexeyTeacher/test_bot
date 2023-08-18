from datetime import datetime
import random

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

from db import session
from config import FIRST, SECOND, FOURTH, FIFTH, END, THREE, ONE, TWO, THIRD, HELP, logger
from models import User, ContentType, Category, History, Document

USER_BASE = {}
N_EXAMPLE = ''


def start(update, context):
    """Стартовый диалог. Автоматически запоминает пользователя и добавляет его в словарь."""
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
        keyboard = [
            [
                InlineKeyboardButton("🎞 Видео", callback_data=str(ONE)),
                InlineKeyboardButton("🏋 Задание‍", callback_data=str(TWO)),
            ],
            [
                InlineKeyboardButton("📁 Текстовый разбор", callback_data=str(THREE)),
                InlineKeyboardButton("🆘 Справка", callback_data=str(HELP))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"🦾 Приветствую, *{update.message.from_user.first_name}*! "
            f"Я бот-помощник для подготовки к ЕГЭ по информатике!\n"
            f"Я могу посоветовать видеоразбор или текстовое объяснение одной из задач, а также дать "
            f"упражнение на тренировку\n\n"
            f"🧠 Все задания и текстовые разборы взяты с "
            f"[сайта](https://kpolyakov.spb.ru/school/ege/generate.htm) *К.Ю. Полякова* _(номера заданий совпадают)_\n"
            f"😅 Видео с разборами задач созданы автором чат-бота или взято лучшее из ютуб \n"
            f"🤝 Отдельное спасибо за помощь с доступом к заданиям *Алексею Кабанову* "
            f"и его [сайту kompege](https://kompege.ru/) \n\n"
            f"Выберите на клавиатуре, что вы сейчас хотите 👇", reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def stop(update, context):
    """Принудительный выход из диалога по команде /stop.
    После выполнения сохраняет в базу данных информацию о сессии пользователя"""
    try:
        name = str(update.message.from_user.name)
        old_user = session.query(User).filter(User.login == name).first()
        update.message.reply_text(f'🖖 Всего доброго, {update.message.from_user.first_name}! \n'
                                  f'Если захотите продолжить подготовку к ЕГЭ, нажмите или напишите /start')
        logger.info(f'{name} >>> /stop')
    except Exception as e:
        logger.error(f'{e}')
    return ConversationHandler.END


def end(update, context):
    """Плановый выход из диалога по кнопке "Хватит".
    После выполнения сохраняет в базу данных информацию о сессии пользователя"""
    try:
        query = update.callback_query
        query.answer()
        name = str(query.from_user.name)
        old_user = session.query(User).filter(User.login == name).first()
        query.edit_message_text(text=f'🖖 Всего доброго, {query.from_user.first_name}! \n'
                                     f'Если захотите продолжить подготовку к ЕГЭ, нажмите или напишите /start')
        logger.info(f'{name} >>> Закончил сеанс')
    except Exception as e:
        logger.error(f'{e}')
    return ConversationHandler.END


def draw_keyboard(update):
    """Рисуем клавиатуру с меню"""
    keyboard = [
            [
                InlineKeyboardButton("🎞 Видео", callback_data=str(ONE)),
                InlineKeyboardButton("🏋 Задание‍", callback_data=str(TWO))
            ],
            [
                InlineKeyboardButton("📁 Текстовый разбор", callback_data=str(THREE)),
                InlineKeyboardButton("💔 Хватит", callback_data=str(END)),
            ],
            [InlineKeyboardButton("🆘 Справка", callback_data=str(HELP))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        update.message.reply_text(text="👇 Выбирайте снова 👇", reply_markup=reply_markup)
    except AttributeError as e:
        logger.error(f'{e}')
        update.callback_query.edit_message_text(text="👇 Выбирайте снова 👇", reply_markup=reply_markup)


def run_doc(update, context):
    """Кнопка Документ"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания, текстовый разбор которого вы хотите получить',
                                parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return FIFTH


def doc(update, context):
    """Возвращает текстовый из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_lesson = update.message.text.strip().replace('№', '')
        update.message.reply_text('Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
        draw_keyboard(update)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def run_video(update, context):
    """Кнопка видео"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания, видео которого вы хотите посмотреть',
                                parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return FOURTH


def video(update, context):
    """Возвращает видео из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_lesson = update.message.text.strip().replace('№', '')
        update.message.reply_text('Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
        draw_keyboard(update)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def run_example(update, context):
    """Кнопка задание"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания',
                                parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return SECOND


def example(update, context):
    """Возвращает случайное задание из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_example = update.message.text.strip().replace('№', '')
        if number_example in [str(i) for i in range(1, 28)]:
            login = update.message.from_user.name
            old_user = session.query(User).filter(User.login == login).first()
            if number_example in ['20', '21']:
                number_example = '19'


            if number_example in ['19', '20', '21']:
                update.message.reply_text(f"✍ Напишите *ответы* на все три вопроса.\n"
                                          f"*Формат:* 1) X 2) Y 3) Z\n"
                                          f"Если ответов на какой-то из вопросов несколько, укажите их через *пробел*",
                                          parse_mode='Markdown')
            else:
                update.message.reply_text(f"✍ Напишите *ответ* на задание. "
                                          f"Если ответов несколько, укажите их через *пробел*",
                                          parse_mode='Markdown')
            return THIRD
        else:
            update.message.reply_text('❌ Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
    except Exception as e:
        logger.error(f'{e}')
        draw_keyboard(update)
        return FIRST


def answer(update, context):
    """Проверяет ответ на задание"""
    try:
        user_answer = update.message.text.strip().upper().split()
        old_user = session.query(User).filter(User.login == update.message.from_user.name).first()

        update.message.reply_text(f'🧐 Правильно, так держать!')

        session.commit()
        draw_keyboard(update)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def help_(update, context):
    """Справка"""
    keyboard = [
        [
            InlineKeyboardButton("🎞 Видео", callback_data=str(ONE)),
            InlineKeyboardButton("🏋 Задание‍", callback_data=str(TWO))
        ],
        [
            InlineKeyboardButton("📁 Текстовый разбор", callback_data=str(THREE)),
            InlineKeyboardButton("💔 Хватит", callback_data=str(END)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    query.answer()

    text = f"*Привет!*\n" \
           f"ЕГЭ по информатике с 2021 года сдают на компьютере. " \
           f"В отличие  от практических работ на уроках информатики, " \
           f"вам не нужно предоставлять решения самих задач. Нужны только ответы. " \
           f"Если ответов несколько, то их нужно писать *через пробел*. " \
           f"Даже если это несколько строк, то всё-равно пишите через пробелы.\n" \
           f"Все типы задач в боте называются *\"номера\"*, их в этом году *27!*\n" \
           f"В боте можно посмотреть *видео* или прочитать *текстовый разбор* каждого типа задания. " \
           f"Если вы уже изучили тему, то смело решайте задачи. " \
           f"Сами задачи взяты с сайта К.Ю. Полякова (номера заданий совпадают).\n" \
           f"Бот ведет счет правильно решенных задач.\n\n" \
           f"*Номера задач:*\n"\
           f"\n_(Задания 19, 20, 21 объединены в одно, "\
           f"так как это одна задача с тремя вопросами)_\n\n" \
           f"*Помимо кнопок есть текстовые команды:*\n" \
           f"/start - запускает бота после остановки\n" \
           f"/stop - принудительно завершает работу бота"

    query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)