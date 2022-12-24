CLEAR = False

TOKEN = '5861365734:AAHsaiUqaOKEeW0uY1Ewa8JCxCLagRtBsHE'
my_username = '@romecolabot'

inviting_url = 'https://t.me/romecolabot?startgroup=hbase'
ask_smn_url = 'https://t.me/d_lkem'

start_message = 'Привет\! На связи *Ром\-Кола Бот* \- твой персональный помощник для управления чатами'

help_message = 'У меня есть несколько очень полезных команд\n\n' \
               'Список команд:\n\n' \
               '*/help* \- показать это сообщение со всеми командами\n\n' \
               '*/add\_to\_chat* \- добавить меня в чат\. Необходимо будет дать мне необходимые права\n\n' \
               'Теперь команды для работы внутри чатов:\n\n' \
               '*/promote\_to\_admin @username* \- сделать пользователя администратором\n\n' \
               '*/ban @username* \- забанить пользователя\n\n' \
               '*/unban @username* \- разабанить пользователя\n\n' \
               '*/stats* \- получить статистику чата\n\n' \
               '*/kick\_romecolabot\_no\_please\_no* \- удалить меня из чата\n\n' \
               'Для использования команд в inline mode просто введите @romecolabot в сообщении\. Если команда' \
               'связана с пользователем введите @romecolabot @username'

ask_smn_text = 'Задать вопрос можно [\@d\.lkem](https://t.me/d_lkem)'


welcome_sticker = 'CAACAgIAAxkBAAEGn_djh3PzCcgjbGG0zkQs4jibtaLW0gACBQADO2AkFDwYiAABJUt2MSsE'
working_sticker = 'CAACAgIAAxkBAAEGoJBjh5lfY7QdmX_gYvF-ZzrD0A_uxAACEgADO2AkFBf2ezO6T5XEKwQ'
okay_sticker = 'CAACAgIAAxkBAAEGoJJjh5mCYKsWOKXSbN6sHNtY6SKlaAACBAADO2AkFLOr61RvleGrKwQ'
thinking_sticker = 'CAACAgIAAxkBAAEGoJljh6AfpQJnsLX0rJs-8tzqMSggDQACFQADO2AkFIa2SRjuaP8vKwQ'
boss_sticker = 'CAACAgIAAxkBAAEGtH1jjw8W0QZJdpglPCXaJPcsDsoYhQACCwADO2AkFMPPOZh4z_kHKwQ'
dancing_sticker = 'CAACAgIAAxkBAAEGtJ9jjxIAAaQag_apNIjSAAFsBYQoQtQwAAIGAAM7YCQUSyHs-_UOdzsrBA'
sad_sticker = 'CAACAgIAAxkBAAEGte9jj4zPQ9w-fu1VmFzOQ9xAvkZWXAACGwADO2AkFNCUnNAljlGHKwQ'
pleased_sticker = 'CAACAgIAAxkBAAEGtf9jj4_tfuyUl26N5wABwdXyAmGAbO8AAgcAAztgJBQmSqw69PC3aSsE'
crying_sticker = 'CAACAgIAAxkBAAEGt3Jjj9neA1GEd9i6Dj4hAyTrrbB5QAACDAADO2AkFGNzJl_KfnQdKwQ'

style = 'XMAS'

inline_icons = {
    'XMAS' : {
        'help': 'https://cdn-icons-png.flaticon.com/512/9074/9074888.png',
        'add_bot': 'https://cdn-icons-png.flaticon.com/512/9075/9075191.png',
        'kick_bot': 'https://cdn-icons-png.flaticon.com/512/9075/9075197.png',
        'stats': 'https://cdn-icons-png.flaticon.com/512/9075/9075105.png',
        'promote': 'https://cdn-icons-png.flaticon.com/512/9074/9074902.png',
        'ban': 'https://cdn-icons-png.flaticon.com/512/9075/9075119.png',
        'unban': 'https://cdn-icons-png.flaticon.com/512/9074/9074910.png',
    },
    'Basic': {
        'help': 'https://cdn-icons-png.flaticon.com/512/149/149944.png',
        'add_bot': 'https://cdn-icons-png.flaticon.com/512/148/148781.png',
        'kick_bot': 'https://cdn-icons-png.flaticon.com/512/149/149951.png',
        'stats': 'https://cdn-icons-png.flaticon.com/512/148/148986.png',
        'promote': 'https://cdn-icons-png.flaticon.com/512/148/148839.png',
        'ban': 'https://cdn-icons-png.flaticon.com/512/148/148766.png',
        'unban': 'https://cdn-icons-png.flaticon.com/512/149/149162.png',
    }
}

thumb_width = 1000
thumb_height = 1000

help_command = '/help@romecolabot'
add_bot_command = '/add_to_chat@romecolabot'
kick_bot_command = '/kick_romecolabot_no_please_no@romecolabot'
stats_command = '/stats@romecolabot'
ban_command = '/ban@romecolabot'
unban_command = '/unban@romecolabot'
promote_command = '/promote_admin@romecolabot'

promote_description = 'User will be granted the same rights as you have, unless you are not a creator'

ban_description = 'The user will not be able to return to the chat on their' \
                  ' own using invite links, etc'

unban_description = 'The user will not return, but will be able to join via link, etc'
