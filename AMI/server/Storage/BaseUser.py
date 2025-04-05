class BaseUser(object):
    def __init__(self, name, description):
        self.NAME = name
        self.DESCRIPTION = description

        self.FRIEND_LIST = []
        self.AI_HISTORY = classmethod
        self.USER_PERSONALITY = ""
        self.BOT_PERSONALITY = ""

        self.IF_MATCHED = bool(False)

    def get_user_name(self):
        return self.NAME

    def get_user_description(self):
        return self.DESCRIPTION

    def get_user_friends(self):
        return self.FRIEND_LIST

    def get_AIhistory(self):
        return self.AI_HISTORY

    def get_user_personality(self):
        return self.USER_PERSONALITY

    def get_bot_personality(self):
        return self.BOT_PERSONALITY

    def if_matched(self):
        return self.IF_MATCHED