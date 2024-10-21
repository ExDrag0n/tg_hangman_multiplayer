import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

START_GAME, GUESS_LETTER = range(2)


def start(update, context):
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    chosen_word = random.choice(words)
    guessed_word = ["_"] * len(chosen_word)
    attempts_left = 6

    context.user_data['word'] = chosen_word
    context.user_data['guessed_word'] = guessed_word
    context.user_data['attempts_left'] = attempts_left

    keyboard = [
        ["A", "B", "C", "D", "E"],
        ["F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "O"],
        ["P", "Q", "R", "S", "T"],
        ["U", "V", "W", "X", "Y", "Z"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    update.message.reply_text("Давай сыграем в виселицу!", reply_markup=reply_markup)
    update.message.reply_text(" ".join(guessed_word))
    update.message.reply_text(f"Осталось попыток: {attempts_left}")

    return GUESS_LETTER


def guess_letter(update, context):
    letter = update.message.text.upper()
    word = context.user_data['word']
    guessed_word = context.user_data['guessed_word']
    attempts_left = context.user_data['attempts_left']

    if len(letter) != 1 or not letter.isalpha():
        update.message.reply_text("Пожалуйста, введи одну букву!")
        return GUESS_LETTER

    if letter in word:
        for i in range(len(word)):
            if word[i] == letter:
                guessed_word[i] = letter
    else:
        attempts_left -= 1

    context.user_data['guessed_word'] = guessed_word
    context.user_data['attempts_left'] = attempts_left

    update.message.reply_text(" ".join(guessed_word))
    update.message.reply_text(f"Осталось попыток: {attempts_left}")

    if "_" not in guessed_word:
        update.message.reply_text("Поздравляю! Ты угадал слово!")
        return ConversationHandler.END
    elif attempts_left == 0:
        update.message.reply_text(f"Жаль, ты проиграл. Правильное слово было: {word}")
        return ConversationHandler.END

    return GUESS_LETTER


def cancel(update, context):
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GUESS_LETTER: [MessageHandler(Filters.regex(r'^[A-Z]$'), guess_letter)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
