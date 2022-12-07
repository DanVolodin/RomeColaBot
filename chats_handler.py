import json
import os
import shutil
from string import Template
import tg_exceptions as tge


class ChatsHandler:
    # clear - это самое важное, что здесь есть
    # clear == True -> создатутся все папочки с нуля, а существующие очистятся
    # clear == False -> продолжить работать с существующими директориями.
    # Это нужно, чтобы в случае падения и рестарта бота мы не теряли всю инфу :clown:
    def __init__(self, clear=False):
        self.users_t = Template('data/chat_users/users_$chat_id.json')
        self.chats_f = 'data/chats_info.json'
        if clear:
            self.create_from_scratch()

    def create_from_scratch(self):
        try:
            os.mkdir('data')
        except FileExistsError:
            shutil.rmtree('data')
            os.mkdir('data')
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))
        try:
            os.mkdir('data/chat_users')
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))
        with open(self.chats_f, 'w') as file:
            json.dump([], file)

    def get_chats(self):
        with open(self.chats_f, 'r') as file:
            chats = json.load(file)
        return chats

    @staticmethod
    def does_chat_exist(chats_list, check_param, param_val):
        chat = list(filter(lambda cht: cht[check_param] == param_val, chats_list))
        return len(chat) > 0

    @staticmethod
    def create_chat(chat_id=0):
        chat = {'chat_id': chat_id}
        return chat

    def save_chats(self, chats):
        with open(self.chats_f, 'w') as file:
            json.dump(chats, file)

    def add_chat(self, chat_id):
        chats = self.get_chats()
        if not self.does_chat_exist(chats, 'chat_id', chat_id):
            self.save_users(chat_id, [])
            chats.append(self.create_chat(chat_id=chat_id))
            self.save_chats(chats)

    def get_users_file(self, chat_id):
        return self.users_t.substitute(chat_id=str(chat_id))

    def get_users(self, chat_id):
        with open(self.get_users_file(chat_id), 'r') as file:
            users = json.load(file)
        return users

    def save_users(self, chat_id, users):
        with open(self.get_users_file(chat_id), 'w') as file:
            json.dump(users, file)

    @staticmethod
    def is_user_in_chat(users_list, user):
        user = list(filter(lambda usr: usr == user, users_list))
        return len(user) > 0

    @staticmethod
    def create_user(user_id=0, username='@username',
                    first_name='FirstName', last_name='LastName',
                    is_premium=False):
        user = {'user_id': user_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'is_premium': is_premium,}
        return user

    def add_user(self, chat_id, user_id=0, username='@username',
                 first_name='FirstName', last_name='LastName',
                 is_premium=False):
        users = self.get_users(chat_id)
        new_user = self.create_user(user_id, '@' + username, first_name, last_name, is_premium)
        try:
            exst_user = self.get_user_by_id(users, user_id)
            users.remove(exst_user)
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))
        # тут тонкий момент в том, что мы здесь же будем и обновлять информацию о юзере
        # когда я понял, что для обновления счетчиков чата нужно рассматривать порядка 5 случаев,
        # я бросил идею счетчиков, все количества будут пересчитываться в онлайне по запросу
        # а сейчас еще нашел в доке телеги команды, которые сами это делают))))
        users.append(new_user)
        self.save_users(chat_id, users)

    def del_user(self, chat_id, user_id):
        users = self.get_users(chat_id)
        user = self.get_user_by_id(users, user_id)
        users.remove(user)
        self.save_users(chat_id, users)

    @staticmethod
    def get_user_by_id(users_list, user_id):
        user = list(filter(lambda usr: usr['user_id'] == user_id, users_list))
        if len(user) > 0:
            return user[0]
        raise tge.UserNotInChatException(user_id)

    def get_user_by_username(self, chat_id, username):
        if len(username) < 2 or username[0] != '@':
            raise tge.InvalidUsernameException(username)
        users_list = self.get_users(chat_id)
        user = list(filter(lambda usr: usr['username'] == username, users_list))
        if len(user) > 0:
            return user[0]
        raise tge.UserNotInChatException(username)

    def get_user_id(self, chat_id, username):
        user = self.get_user_by_username(chat_id, username)
        return user['user_id']


# chats = ChatsHandler()
# chats.add_chat(101234)
# chats.add_user(101234, 12321, '@d.lkem')
# print(chats.get_users(101234))
# print(chats.get_user_id(101234, '@d.lkem'))
# chats.add_chat(201234)
# chats.add_user(101234, 333666999, '@newman')
# print(chats.get_user_param(101234, 'username', '@newman', 'user_id'))
# chats.add_user(201234, 333666999, '@newman')
# print(chats.get_user_param(201234, 'username', '@newman', 'user_id'))
# chats.add_user(201234, 333666999, '@newman')
# print(chats.get_users(201234))
# print(chats.get_user_id(201234, '@d.lkem'))
