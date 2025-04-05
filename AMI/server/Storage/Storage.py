from .BaseUser import BaseUser


class Storage():
    def __init__(self, debug=True):
        self.number_of_USERS = 0
        self.debug = debug

    # Where new users are born
    def create_new_user(self, name, descriptions):
        new_user = BaseUser(name, descriptions)
        print("CREATE NEW USER: USER_ID_" + str(name))
        setattr(self, "USER_ID_" + str(name), new_user)

    # Giving personality to user
    def set_user_description(self, name, description):
        if self.debug: print("LOG: SET USER DESCRIPTION: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        user.DESCRIPTION = description

    # Give users some friends
    def set_user_friendList(self, name, flist):
        if self.debug: print("LOG: SET USER friendList: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        user.FRIEND_LIST = flist

    # Log of who the user has chatted with
    def set_user_AIHistory(self, name, history):
        if self.debug: print("LOG: SET USER AIHistory: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        user.AI_HISTORY = history

    # Assign personality to the bot
    def set_bot_Personality(self, name, personality):
        if self.debug: print("LOG: SET USER botPersonality: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        user.BOT_PERSONALITY = personality

    # Assign Personality to user
    def set_user_Personality(self, name, personality):
        if self.debug: print("LOG: SET USER userPersonality: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        user.USER_PERSONALITY = personality

    # Returns description of user
    def get_user_description(self, name):
        if self.debug: print("LOG: GET USER DESCRIPTION: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        return user.get_user_description()

    # Returns friends
    def get_user_friends(self, name):
        if self.debug: print("LOG: GET USER FRIEND LIST: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        return user.get_user_friends()

    # Return AI History
    def get_AIhistory(self, name):
        if self.debug: print("LOG: GET USER AI HISTORY: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        return user.get_AIhistory()

    # Return user personality
    def get_user_personality(self, name):
        if self.debug: print("LOG: GET USER PERSONALITY: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        return user.get_user_description()

    # Return bot personality
    def get_bot_personality(self, name):
        if self.debug: print("LOG: GET USER PREFERENCE PERSONALITY: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        return user.get_bot_personality()

    # Checks if 2 users match
    def if_matched(self, name):
        if self.debug: print("LOG: GET USER MATCHED STATUE: USER ID: " + "USER_ID_" + str(name))
        user = getattr(self, "USER_ID_" + str(name), None)
        return user.if_matched()

    def parse_users_data(self):
        # TODO IMPLEMENT READ USER DATA FROM CSV FILE
        pass
