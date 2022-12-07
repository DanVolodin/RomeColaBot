import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt

import paths as pth
import chats_handler as ch
import tg_exceptions as tge

bot = telebot.TeleBot(pth.TOKEN)
chats = ch.ChatsHandler(clear=pth.CLEAR)
scheduler = BackgroundScheduler()

scheduler.start()


def add_chat_member(command_action):
    def wrapper(message):
        user = message.from_user
        if message.chat.type in ['supergroup', 'group']:
            chats.add_user(message.chat.id, user.id, user.username,
                           user.first_name, user.last_name,
                           user.is_premium)
        command_action(message)
    return wrapper


def delete_command_message(command_action):
    def wrapper(message):
        bot.delete_message(message.chat.id, message.id)
        command_action(message)
    return wrapper


def user_is_admin(command_action):
    def wrapper(message):
        cur_user = bot.get_chat_member(message.chat.id, message.from_user.id)
        if cur_user.status not in ['creator', 'administrator']:
            raise tge.UserNotAdminException(message.from_user.id)
        command_action(message)

    return wrapper


def admin_can_restrict(command_action):
    def wrapper(message):
        cur_user = bot.get_chat_member(message.chat.id, message.from_user.id)
        if cur_user.status == 'administrator' and not cur_user.can_restrict_members:
            raise tge.NoPermissionException(message.from_user.id, 'restrict members')
        command_action(message)

    return wrapper


def admin_can_promote(command_action):
    def wrapper(message):
        cur_user = bot.get_chat_member(message.chat.id, message.from_user.id)
        if cur_user.status == 'administrator' and not cur_user.can_promote_members:
            raise tge.NoPermissionException(message.from_user.id, 'promote members')
        command_action(message)

    return wrapper


def hello_its_me(command_action):
    def wrapper(message):
        username = message.text.split()[1]
        if username == pth.my_username:
            raise tge.HelloItsMeException()
        command_action(message)

    return wrapper


def parse_exceptions(command_action):
    def wrapper(message):
        bot_msg = None
        try:
            command_action(message)
        except IndexError as e:
            bot_msg = bot.send_message(message.chat.id, '⚠️Username was not given in command')
            print("{!s}\n{!s}".format(type(e), str(e)))
        except telebot.apihelper.ApiTelegramException as e:
            bot_msg = bot.send_message(message.chat.id, '⛔ ' + e.description)
            print("{!s}\n{!s}".format(type(e), str(e)))
        except tge.UserNotAdminException as e:
            bot_msg = bot.send_message(message.chat.id, '⛔ You have to be an administrator at least')
            print("{!s}\n{!s}".format(type(e), str(e)))
        except tge.NoPermissionException as e:
            bot_msg = bot.send_message(message.chat.id, f'⛔ You do not have a permission to {e.action}')
            print("{!s}\n{!s}".format(type(e), str(e)))
        except tge.HelloItsMeException as e:
            bot_msg = bot.send_message(message.chat.id, str(e))
            print("{!s}\n{!s}".format(type(e), str(e)))
        except tge.InvalidUsernameException as e:
            bot_msg = bot.send_message(message.chat.id, '⚠️' + str(e))
            print("{!s}\n{!s}".format(type(e), str(e)))
        except tge.UserNotInChatException as e:
            bot_msg = bot.send_message(message.chat.id, '⚠️' + str(e))
            print("{!s}\n{!s}".format(type(e), str(e)))
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))

        def delete_alert(chat_id, msg_id):
            bot.delete_message(chat_id, msg_id)

        if bot_msg is not None:
            try:
                scheduler.add_job(delete_alert, 'date', run_date=dt.datetime.now() + dt.timedelta(seconds=10),
                                  kwargs={'chat_id': message.chat.id, 'msg_id': bot_msg.id})
            except Exception as e:
                print("{!s}\n{!s}".format(type(e), str(e)))

    return wrapper


def start_message_markup():
    markup = types.InlineKeyboardMarkup()
    item_invite = types.InlineKeyboardButton(text='Добавить бота в чат', url=pth.inviting_url)
    item_help = types.InlineKeyboardButton(text='Что я умею?', callback_data='help')
    markup.add(item_invite, item_help)
    return markup


def help_message_markup():
    markup = types.InlineKeyboardMarkup()
    item_clear = types.InlineKeyboardButton(text='Все понятно!', callback_data='help_clear')
    item_question = types.InlineKeyboardButton(text='Есть вопрос', callback_data='help_ask')
    markup.add(item_clear, item_question)
    return markup


def help_inline_markup():
    markup = types.InlineKeyboardMarkup()
    item_clear = types.InlineKeyboardButton(text='Все понятно!', callback_data='help_clear_inline')
    item_question = types.InlineKeyboardButton(text='Есть вопрос', callback_data='help_ask_inline')
    markup.add(item_clear, item_question)
    return markup


def add_bot_button_markup():
    markup = types.InlineKeyboardMarkup()
    item_invite = types.InlineKeyboardButton(text='Добавить бота в чат', url=pth.inviting_url)
    markup.add(item_invite)
    return markup


def add_bot_inline_markup():
    markup = types.InlineKeyboardMarkup()
    item_back = types.InlineKeyboardButton(text='Назад', callback_data='help_inline')
    item_invite = types.InlineKeyboardButton(text='Добавить бота в чат', url=pth.inviting_url)
    markup.add(item_back, item_invite)
    return markup


@bot.message_handler(commands=['start'])
@delete_command_message
@parse_exceptions
@add_chat_member
def start(message):
    bot.send_sticker(message.chat.id, pth.welcome_sticker)

    bot.send_message(message.chat.id, pth.start_message,
                     reply_markup=start_message_markup(),
                     parse_mode='MarkdownV2')

    if message.chat.type in ['supergroup', 'group']:
        chats.add_chat(message.chat.id)


@bot.message_handler(commands=['help'])
@delete_command_message
@parse_exceptions
@add_chat_member
def help(message):
    bot.send_sticker(message.chat.id, pth.thinking_sticker)

    bot.send_message(message.chat.id, pth.help_message,
                     reply_markup=help_message_markup(),
                     parse_mode='MarkdownV2')


@bot.message_handler(commands=['add_to_chat'])
@delete_command_message
@parse_exceptions
@add_chat_member
def add_bot(message):
    bot.send_sticker(message.chat.id, pth.working_sticker)

    bot.send_message(message.chat.id, 'Поехали\!',
                     reply_markup=add_bot_button_markup(),
                     parse_mode='MarkdownV2')


@bot.message_handler(commands=['kick_romecolabot_no_please_no'], chat_types=['supergroup', 'group'])
@delete_command_message
@parse_exceptions
@add_chat_member
@user_is_admin
@admin_can_restrict
def kick_bot(message):
    bot.send_message(message.chat.id, 'Bye, bye, see you soon✋')
    bot.send_sticker(message.chat.id, pth.crying_sticker)
    bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['stats'], chat_types=['supergroup', 'group'])
@delete_command_message
@add_chat_member
@parse_exceptions
def stats(message):
    members_cnt = bot.get_chat_member_count(message.chat.id)
    admins_cnt = len(bot.get_chat_administrators(message.chat.id))

    bot.send_sticker(message.chat.id, pth.dancing_sticker)

    bot.send_message(message.chat.id, f'*Total members*: {members_cnt}\n*Administrators*: {admins_cnt}',
                     parse_mode='MarkdownV2')


@bot.message_handler(commands=['promote_admin'], chat_types=['supergroup', 'group'])
@delete_command_message
@parse_exceptions
@add_chat_member
@user_is_admin
@admin_can_promote
@hello_its_me
def promote_admin(message):
    cur_user = bot.get_chat_member(message.chat.id, message.from_user.id)

    username = message.text.split()[1]
    user_id = chats.get_user_id(message.chat.id, username)

    success = False

    if cur_user.status == 'creator':
        success = bot.promote_chat_member(message.chat.id, user_id,
                                          can_change_info=False,
                                          can_delete_messages=False,
                                          can_pin_messages=True,
                                          can_promote_members=True,
                                          can_restrict_members=True,
                                          can_manage_chat=False,
                                          can_invite_users=True,
                                          can_edit_messages=False,
                                          can_post_messages=True,
                                          can_manage_video_chats=True,
                                          can_manage_voice_chats=True)
    else:
        success = bot.promote_chat_member(message.chat.id, user_id, can_change_info=cur_user.can_change_info,
                                          can_delete_messages=cur_user.can_delete_messages,
                                          can_pin_messages=cur_user.can_delete_messages,
                                          can_promote_members=cur_user.can_promote_members,
                                          can_restrict_members=cur_user.can_restrict_members,
                                          can_manage_chat=cur_user.can_manage_chat,
                                          can_invite_users=cur_user.can_invite_users,
                                          can_edit_messages=cur_user.can_edit_messages,
                                          can_post_messages=cur_user.can_post_messages,
                                          can_manage_video_chats=cur_user.can_manage_video_chats,
                                          can_manage_voice_chats=cur_user.can_manage_voice_chats)

    if success:
        bot.send_message(message.chat.id, f'{username} is now Administrator\!',
                         parse_mode='MarkdownV2')

        bot.send_sticker(message.chat.id, pth.boss_sticker)
    else:
        bot.send_message(message.chat.id, '⚠️Something went wrong',
                         parse_mode='MarkdownV2')


@bot.message_handler(commands=['ban'], chat_types=['supergroup', 'group'])
@delete_command_message
@parse_exceptions
@add_chat_member
@user_is_admin
@admin_can_restrict
@hello_its_me
def ban(message):
    username = message.text.split()[1]
    user_id = chats.get_user_id(message.chat.id, username)

    if bot.ban_chat_member(message.chat.id, user_id):
        bot.send_message(message.chat.id, f'{username} was banned',
                         parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, '⚠️Something went wrong',
                         parse_mode='MarkdownV2')


@bot.message_handler(commands=['unban'], chat_types=['supergroup', 'group'])
@delete_command_message
@parse_exceptions
@add_chat_member
@user_is_admin
@admin_can_restrict
@hello_its_me
def unban(message):
    username = message.text.split()[1]
    user_id = chats.get_user_id(message.chat.id, username)

    if bot.unban_chat_member(message.chat.id, user_id, only_if_banned=True):
        # Я считаю, что качество в мелочах, поэтому я убрал фразу 'he/she can join', вдруг пользователь еще не определился
        bot.send_message(message.chat.id, f'{username} was unbanned and can join chat again',
                         parse_mode='MarkdownV2')

        bot.send_sticker(message.chat.id, pth.pleased_sticker)
    else:
        bot.send_message(message.chat.id, '⚠️Something went wrong',
                         parse_mode='MarkdownV2')


@bot.message_handler(content_types=['new_chat_members'])
@parse_exceptions
def add_user(message):
    new_users = message.new_chat_members
    bot.send_sticker(message.chat.id, pth.welcome_sticker)
    for user in new_users:
        if '@' + user.username == pth.my_username:
            chats.add_chat(message.chat.id)
            bot.send_message(message.chat.id, pth.start_message,
                             reply_markup=start_message_markup(),
                             parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id, f'Hello, @{user.username}👋\nHow are you\?',
                             parse_mode='MarkdownV2')
        chats.add_user(message.chat.id, user.id, user.username,
                       user.first_name, user.last_name,
                       user.is_premium)


@bot.message_handler(content_types=['left_chat_member'])
@parse_exceptions
def del_user(message):
    user = message.left_chat_member
    if '@' + user.username != pth.my_username:
        bot.send_message(message.chat.id, f'Bye, bye, {user.first_name}✋',
                         parse_mode='MarkdownV2')
        bot.send_sticker(message.chat.id, pth.sad_sticker)


@bot.message_handler()
@add_chat_member
def add_user(message):
    pass


@bot.callback_query_handler(lambda call: call.data == 'help')
def help_callback(call):
    try:
        bot.edit_message_text(text=pth.help_message,
                              chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              reply_markup=help_message_markup(),
                              parse_mode='MarkdownV2')

        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.callback_query_handler(lambda call: call.data == 'help_clear')
def help_clear_callback(call):
    try:
        bot.send_sticker(call.message.chat.id, pth.working_sticker)

        bot.send_message(call.message.chat.id, 'Тогда поехали\!',
                         reply_markup=add_bot_button_markup(),
                         parse_mode='MarkdownV2')

        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.callback_query_handler(lambda call: call.data == 'help_ask')
def help_ask_callback(call):
    try:
        markup = types.InlineKeyboardMarkup()
        item_ask = types.InlineKeyboardButton(text='Задать вопрос', url=pth.ask_smn_url)
        item_back = types.InlineKeyboardButton(text='Назад', callback_data='help')
        markup.add(item_back, item_ask)

        bot.edit_message_text(text=pth.ask_smn_text,
                              chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              reply_markup=markup,
                              parse_mode='MarkdownV2')

        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.callback_query_handler(lambda call: call.data == 'help_inline')
def help_callback(call):
    try:
        bot.edit_message_text(text=pth.help_message,
                              inline_message_id=call.inline_message_id,
                              reply_markup=help_inline_markup(),
                              parse_mode='MarkdownV2')

        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.callback_query_handler(lambda call: call.data == 'help_clear_inline')
def help_clear_inline_callback(call):
    try:
        bot.edit_message_text('Тогда поехали\!',
                              inline_message_id=call.inline_message_id,
                              reply_markup=add_bot_inline_markup(),
                              parse_mode='MarkdownV2')

        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.callback_query_handler(lambda call: call.data == 'help_ask_inline')
def help_ask_callback(call):
    try:
        markup = types.InlineKeyboardMarkup()
        item_ask = types.InlineKeyboardButton(text='Задать вопрос', url=pth.ask_smn_url)
        item_back = types.InlineKeyboardButton(text='Назад', callback_data='help_inline')
        markup.add(item_back, item_ask)

        bot.edit_message_text(text=pth.ask_smn_text,
                              inline_message_id=call.inline_message_id,
                              reply_markup=markup,
                              parse_mode='MarkdownV2')

        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.inline_handler(lambda query: query.chat_type == 'sender')
def answer_query(query):
    try:
        r_help = types.InlineQueryResultArticle(
            id='1', title="Help",
            input_message_content=types.InputTextMessageContent(message_text=pth.help_command,
                                                                parse_mode='MarkdownV2'),
            thumb_url=pth.inline_icons[pth.style]['help'],
            thumb_width=pth.thumb_width,
            thumb_height=pth.thumb_height
        )

        r_add_bot = types.InlineQueryResultArticle(
            id='2', title="Add RomeColaBot to chat",
            input_message_content=types.InputTextMessageContent(message_text=pth.add_bot_command,
                                                                parse_mode='MarkdownV2'),
            thumb_url=pth.inline_icons[pth.style]['add_bot'],
            thumb_width=pth.thumb_width,
            thumb_height=pth.thumb_height
        )
        bot.answer_inline_query(query.id, [r_help, r_add_bot])
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


def inline_query_results_help_add():
    r_help = types.InlineQueryResultArticle(
        id='1', title="Help",
        input_message_content=types.InputTextMessageContent(message_text=pth.help_message,
                                                            parse_mode='MarkdownV2'),
        reply_markup=help_inline_markup(),
        thumb_url=pth.inline_icons[pth.style]['help'],
        thumb_width=pth.thumb_width,
        thumb_height=pth.thumb_height
    )

    r_add_bot = types.InlineQueryResultArticle(
        id='2', title="Add RomeColaBot to chat",
        input_message_content=types.InputTextMessageContent(message_text='Поехали\!',
                                                            parse_mode='MarkdownV2'),
        reply_markup=add_bot_button_markup(),
        thumb_url=pth.inline_icons[pth.style]['add_bot'],
        thumb_width=pth.thumb_width,
        thumb_height=pth.thumb_height
    )
    return [r_help, r_add_bot]


@bot.inline_handler(lambda query: query.chat_type == 'private')
def answer_query(query):
    try:
        bot.answer_inline_query(query.id, inline_query_results_help_add())
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.inline_handler(lambda query: query.chat_type in ['group', 'supergroup'] and len(query.query) == 0)
def answer_query(query):
    try:
        r_stats = types.InlineQueryResultArticle(
            id='3', title="Show chat statistics",
            input_message_content=types.InputTextMessageContent(message_text=pth.stats_command,
                                                                parse_mode='MarkdownV2'),
            description='See number of users and admins (add me to chat first)',
            thumb_url=pth.inline_icons[pth.style]['stats'],
            thumb_width=pth.thumb_width,
            thumb_height=pth.thumb_height
        )

        r_kick_bot = types.InlineQueryResultArticle(
            id='4', title="Kick RomeColaBot",
            input_message_content=types.InputTextMessageContent(message_text=pth.kick_bot_command,
                                                                parse_mode='MarkdownV2'),
            description='Be careful, please',
            thumb_url=pth.inline_icons[pth.style]['kick_bot'],
            thumb_width=pth.thumb_width,
            thumb_height=pth.thumb_height
        )

        bot.answer_inline_query(query.id, inline_query_results_help_add() + [r_stats, r_kick_bot])
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.inline_handler(lambda query: query.chat_type in ['group', 'supergroup'] and
                                  len(query.query) > 0 and query.query[0] == '@')
def answer_query(query):
    try:
        r_promote = types.InlineQueryResultArticle(
            id='1', title="Promote member",
            input_message_content=types.InputTextMessageContent(message_text=pth.promote_command + ' ' + query.query,
                                                                parse_mode='MarkdownV2'),
            description=pth.promote_description,
            thumb_url=pth.inline_icons[pth.style]['promote'],
            thumb_width=pth.thumb_width,
            thumb_height=pth.thumb_height
        )

        r_ban = types.InlineQueryResultArticle(
            id='2', title="Ban member",
            input_message_content=types.InputTextMessageContent(message_text=pth.ban_command + ' ' + query.query,
                                                                parse_mode='MarkdownV2'),
            description=pth.ban_description,
            thumb_url=pth.inline_icons[pth.style]['ban'],
            thumb_width=pth.thumb_width,
            thumb_height=pth.thumb_height
        )

        r_unban = types.InlineQueryResultArticle(
            id='3', title="Unban member",
            input_message_content=types.InputTextMessageContent(message_text=pth.unban_command + ' ' + query.query,
                                                                parse_mode='MarkdownV2'),
            description=pth.unban_description,
            thumb_url=pth.inline_icons[pth.style]['unban'],
            thumb_width=pth.thumb_width,
            thumb_height=pth.thumb_height
        )

        bot.answer_inline_query(query.id, [r_promote, r_ban, r_unban])
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


if __name__ == '__main__':
    bot.infinity_polling()
