from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, Updater

from config import (TOKEN, END, FIRST, HELP, logger, DOWNLOAD_START, DOWNLOAD_END, LAST_SELFIE_START,
                    SCHOOL_PHOTO_START, STORY_START, GPT_START, BASES_START, FIRST_LOVE_START, LAST_SELFIE_END,
                    SCHOOL_PHOTO_END, STORY_END, GPT_END, BASES_END, FIRST_LOVE_END)
from bot_logic import (stop, start, help_, github, run_download, download_start, download_end, run_selfie, selfie, end,
                       run_school_photo, school_photo, run_story, run_gpt, run_bases, run_first_love, story, gpt, bases,
                       first_love)


def main():
    logger.info('restart app')

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(run_selfie, pattern='^' + str(LAST_SELFIE_START) + '$'),
                CallbackQueryHandler(run_school_photo, pattern='^' + str(SCHOOL_PHOTO_START) + '$'),
                CallbackQueryHandler(run_story, pattern='^' + str(STORY_START) + '$'),
                CallbackQueryHandler(run_gpt, pattern='^' + str(GPT_START) + '$'),
                CallbackQueryHandler(run_bases, pattern='^' + str(BASES_START) + '$'),
                CallbackQueryHandler(run_first_love, pattern='^' + str(FIRST_LOVE_START) + '$'),
                CallbackQueryHandler(help_, pattern='^' + str(HELP) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
                CommandHandler('github', github),
                CommandHandler('download', run_download)

            ],
            LAST_SELFIE_END: [MessageHandler(Filters.text, selfie)],
            SCHOOL_PHOTO_END: [MessageHandler(Filters.text, school_photo)],
            STORY_END: [MessageHandler(Filters.text, story)],
            GPT_END: [MessageHandler(Filters.text, gpt)],
            BASES_END: [MessageHandler(Filters.text, bases)],
            FIRST_LOVE_END: [MessageHandler(Filters.text, first_love)],

            DOWNLOAD_START: [MessageHandler(Filters.text, download_start)],
            DOWNLOAD_END: [MessageHandler(Filters.all & ~Filters.command, download_end)]

        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]

    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'MAIN {e}')
