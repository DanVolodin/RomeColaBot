class HelloItsMeException(Exception):
    def __init__(self):
        self.message = 'Wow, I can\'t shoot myself in the foot🔫'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UserNotInChatException(Exception):
    def __init__(self, user):
        self.user = user
        self.message = f'User {user} not found in chat'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidUsernameException(Exception):
    def __init__(self, user):
        self.user = user
        self.message = f'Username {user} is not valid'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UserNotAdminException(Exception):
    def __init__(self, user):
        self.user = user
        self.message = f'User {user} is not an administrator'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NoPermissionException(Exception):
    def __init__(self, user, action):
        self.user = user
        self.action = action
        self.message = f'User {user} does not have permission to {action}'
        super().__init__(self.message)

    def __str__(self):
        return self.message
