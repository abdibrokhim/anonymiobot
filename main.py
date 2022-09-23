#!/usr/bin/env python

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackContext,
    InlineQueryHandler,
    CallbackQueryHandler,
)
from telegram.constants import ParseMode
from html import escape
from uuid import uuid4

import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


TELEGRAM_BOT_TOKEN = ''
PAYME_LINK = ''


_en_learn_more = """
The way to use me is to write the inline query by your self

The format should be in this arrangement:

@anonyiobot your AnonyIO @username

Now I'll split out the format in 3 parts and explain every part of it

1 - @anonyiobot
this is my username it should be at the beginning of the inline query so I'll know that you are using me and not another bot.

2 - AnonyIO message
it is the AnonyIO that will be sent to the target user, you need to remove your AnonyIO and insert your actual AnonyIO.

3 - @username
you should replace this with target's username so the bot will know that the user with this username can see your AnonyIO message.

Example:
@anonyiobot Good morning! @durov

The bot works in groups and the target user should be in the same group with you
what you are waiting for?!
try me now 😉
"""

_ru_learn_more = """
Способ использовать меня написать встроенный запрос самостоятельно.

Формат должен быть в таком расположении:

@anonyiobot ваш AnonyIO @username

Теперь я разделю формат на 3 части и объясню каждую его часть.

1 - @anonyiobot
это мое имя пользователя, оно должно быть в начале встроенного запроса, чтобы я знал, что вы используете меня, а не другого бота.

2 - AnonyIO message
это AnonyIO, который будет отправлен целевому пользователю, вам нужно удалить AnonyIO и вставить свой фактический AnonyIO.

3 - @username
вы должны заменить это именем пользователя цели, чтобы бот знал, что пользователь с этим именем пользователя может видеть ваше сообщение AnonyIO.

Пример:
@anonyiobot Доброе утро! @durov

Бот работает в группах и целевой пользователь должен быть в одной группе с вами
чего вы ждете?!
попробуй меня сейчас 😉
"""

_uzb_learn_more = """
Mendan foydalanishning yo'li ichki so'rovni o'zingiz yozish

Format ushbu tartibda bo'lishi kerak:

@anonyiobot sizning AnonyIO @username

Endi men formatni 3 qismga ajrataman va uning har bir qismini tushuntiraman

1 - @anonyiobot
bu mening foydalanuvchi nomim, u ichki so'rovning boshida bo'lishi kerak, shuning uchun siz boshqa botdan emas, mendan foydalanayotganingizni bilaman.

2 - AnonyIO message
bu maqsadli foydalanuvchiga yuboriladigan AnonyIO, siz AnonyIO-ni olib tashlashingiz va haqiqiy AnonyIO-ni kiritishingiz kerak.

3 - @username
uni maqsadli foydalanuvchi nomi bilan almashtirishingiz kerak, shunda bot ushbu foydalanuvchi nomiga ega bo'lgan foydalanuvchi sizning AnonyIO xabaringizni ko'rishi mumkinligini bilib oladi.

Masalan:
@anonyiobot Hayrli tong! @durov

Bot guruhlarda ishlaydi va maqsadli foydalanuvchi siz bilan bir guruhda bo'lishi kerak
nima kutyapsiz?!
meni hozir sinab ko'ring 😉
"""

_en_about = """
🥱 This bot was made by @abdibrokhim

/start - to go back to the main page.
"""

_ru_about = """
🥱 Бот разработал @abdibrokhim

/start - вернуться на главную страницу.
"""

_uzb_about = """
🥱 Bot @abdibrokhim tomonidan ishlab chiqilgan

/start - bosh menyuga qaytish.
"""

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    txt = f"""
Tilni tanlang 🦋 Выберите язык 🦋 Choose language

"""

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🇺🇿 Uzbek', callback_data='_uzb',),
                InlineKeyboardButton('🇷🇺 Russian', callback_data='_ru',),
                InlineKeyboardButton('🇺🇸 English', callback_data='_en',),
            ],
        ]
    )

    await update.message.reply_text(text=txt, reply_markup=reply_markup)


async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Callback query
    query = update.callback_query

    # Who pressed button
    from_ = update.callback_query.from_user


    # Move to specifik language
    if query.data == '_uzb':
        await uzb_lang_handler(update, context)

    # Move to specifik language
    elif query.data == '_ru':
        await ru_lang_handler(update, context)

    # Move to specifik language
    elif query.data == '_en':
        await en_lang_handler(update, context)

    elif query.data == '_uzb_learn_more':
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text='👽 Sinab ko\'rish',
                        switch_inline_query='AnonyIO',
                    )
                ]
            ]
        )

        await query.edit_message_text(text=_uzb_learn_more, reply_markup=reply_markup, )
    elif query.data == '_uzb_about':
        await query.edit_message_text(text=_uzb_about,)

    elif query.data == '_ru_learn_more':
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text='👽 Попробовать',
                        switch_inline_query='AnonyIO',
                    )
                ]
            ]
        )

        await query.edit_message_text(text=_ru_learn_more, reply_markup=reply_markup, )
    elif query.data == '_ru_about':
        await query.edit_message_text(text=_ru_about,)

    elif query.data == '_en_learn_more':
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text='👽 Try now',
                        switch_inline_query='AnonyIO',
                    ),
                    # InlineKeyboardButton('Back', callback_data='_en_about',)
                ]
            ]
        )

        await query.edit_message_text(text=_en_learn_more, reply_markup=reply_markup, )

    elif query.data == '_en_about':
        await query.edit_message_text(text=_en_about,)

    # show if button was pressed by original Sender or Receiver
    elif from_.username == from__.username or from_.username == to_[1]:
        await context.bot.answer_callback_query(
            callback_query_id=query.id,
            text=f'{to_[0]}',
            show_alert=True,
        )
    # show if button was pressed by invalid receivers
    else:
        await context.bot.answer_callback_query(
            callback_query_id=query.id,
            text="Sorry you can't see this AnonyIO, because it wasn't sent to you 🔐",
            show_alert=True,
        )


async def uzb_lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ error function """
    user = update.effective_user

    # Callback query
    query = update.callback_query

    txt = f"""
    
Assolomu alaykum: {user.full_name}!
💀 Men bot AnonyIO.

💬 Guruhlarda maxfiy AnonyIO'larni yuborish uchun mendan foydalanishingiz mumkin.

🔮 Men Inline rejimida ishlayman, ya'ni guruhda bo'lmasam ham mendan foydalanishingiz mumkin.

😌 Mendan foydalanish juda oson.

Agar siz men haqimda ko'proq ma'lumot olishni istasangiz, quyidagi tugmani bosing.

"""

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🙉 Ko\'proq o\'qish', callback_data='_uzb_learn_more',),
                InlineKeyboardButton('🦉 Haqida', callback_data='_uzb_about',)
            ]
        ]
    )

    await query.edit_message_text(text=txt, reply_markup=reply_markup)


async def ru_lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ error function """
    user = update.effective_user

    # Callback query
    query = update.callback_query

    txt = f"""
    
Добро пожаловать: {user.full_name}!
💀 Я бот AnonyIO.

💬 Вы можете использовать меня для отправки секретных AnonyIO в группах.

🔮 Я работаю в режиме Inline, что означает, что вы можете использовать меня, даже если я не в группе.

😌 Меня очень легко использовать.

Если вам интересно узнать обо мне больше, нажмите на кнопку ниже.

"""

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🙉 Узнать больше', callback_data='_ru_learn_more',),
                InlineKeyboardButton('🦉 Инфо', callback_data='_ru_about',)
            ]
        ]
    )

    await query.edit_message_text(text=txt, reply_markup=reply_markup)


async def en_lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ error function """
    user = update.effective_user

    # Callback query
    query = update.callback_query

    txt = f"""
        
Welcome: {user.full_name}!
💀 I'm the AnonyIO Bot.

💬 You can use me to send secret AnonyIOs in groups.

🔮 I work in the Inline mode that means you can use me even if I'm not in the group.

😌 It is very easy to use me.

If you are interested to learn more about me click on the Button below.

"""

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🙉 Learn more', callback_data='_en_learn_more',),
                InlineKeyboardButton('🦉 About', callback_data='_en_about',)
            ]
        ]
    )

    await query.edit_message_text(text=txt, reply_markup=reply_markup)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the inline query. This is run when you type: @botusername <query>"""
    global to_
    global from__

    # Inline query
    query = update.inline_query.query

    # Who send message
    from__ = update.inline_query.from_user

    # Splitting message and username -> ['message', 'username']
    to_ = query.split('@')

    print(to_[0], ' - to - ', to_[1], ' - from - ', from__.username)  # initial info from who, what message and to whom

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"🔒 A AnonyIO message to {to_[1]}\nhe/she can open it.",
            input_message_content=InputTextMessageContent(
                f'<b>{escape(f"🔒 A AnonyIO message to {to_[1]}, Only he/she can open it.")}</b>',
                parse_mode=ParseMode.HTML, ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='Show Message 🔐',
                            callback_data=str(to_),
                        )
                    ],
                ]
            ),
        ),
    ]

    query = await context.bot.answerCallbackQuery(callback_query_id=update.inline_query.id,)

    context.user_data['from_tg_username'] = from__.username
    context.user_data['whisper'] = to_[0]
    context.user_data['to_tg_username'] = to_[1]

    await update.inline_query.answer(results=results,)


async def _donate_handler(update: Update, context: CallbackContext):
    await update.message.reply_photo(
        photo=open('payme/payme.png', 'rb'),
        caption='📱 Scan QR code or\n\n⛓ Tap the link below\n\n' + PAYME_LINK,
        filename='Donation'
    )


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).read_timeout(7).get_updates_read_timeout(42).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("donate", _donate_handler))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(callback_query))

    print("updated ...")
    app.run_polling()
