class Protocol:
    def __init__(self):
        pass

    @staticmethod
    def send_data2user(source_USER, dest_USER, data):
        rst = ""
        rst += "SEND_DATA2USER" + str(source_USER).upper() + "SPLIT-PLACEHOLDER-SPLIT" + str(dest_USER).upper() + "SPLIT-PLACEHOLDER-SPLIT" + str(data) + "SPLIT-PLACEHOLDER-SPLIT" + str(len(data)) + "END-PLACEHOLDER-END"
        return rst

    @staticmethod
    def create_user(user_name, description=""):
        rst = ""
        rst += "CREATE_USER" + str(user_name).upper() + "SPLIT-PLACEHOLDER-SPLIT" + str(description) + "SPLIT-PLACEHOLDER-SPLIT" + str(len(user_name) + len(description)) + "END-PLACEHOLDER-END"
        return rst

    @staticmethod
    def serv2user(data):
        rst = "SERV2USER" + str(data) + "SPLIT-PLACEHOLDER-SPLIT" + str(len(data)) + "END-PLACEHOLDER-END"
        return rst

    @staticmethod
    def switch_AI2Real(user_name):
        return "SWITCH_AI2REAL" + str(user_name).upper() + "SPLIT-PLACEHOLDER-SPLIT" + str(len(user_name)) + "END-PLACEHOLDER-END"

    @staticmethod
    def TRUE():
        return "BOOLEANFLAG" + "TRUE" + "END-PLACEHOLDER-END"

    @staticmethod
    def FALSE():
        return "BOOLEANFLAG" + "FALSE" + "END-PLACEHOLDER-END"

    @staticmethod
    def parse_data(data):
        data = str(data)
        if data.startswith("SEND_DATA2USER"):
            data = data.replace("SEND_DATA2USER", "")
            data = data.replace("END-PLACEHOLDER-END", "")
            data = data.split("SPLIT-PLACEHOLDER-SPLIT")
            source_user = str(data[0])
            target_user = str(data[1])
            message = str(data[2])
            length = int(data[3])
            if len(message) == int(length):
                if source_user == "": return "SEND2USER", source_user, "AI", message
                else: return "SEND2USER", source_user, target_user, message

        elif data.startswith("CREATE_USER"):
            data = data.replace("CREATE_USER", "")
            data = data.replace("END-PLACEHOLDER-END", "")
            data = data.split("SPLIT-PLACEHOLDER-SPLIT")
            new_user = str(data[0])
            description = str(data[1])
            length = int(data[2])
            if len(new_user) + len(description) == int(length):
                return "CREATE", new_user, description

        elif data.startswith("SWITCH_AI2REAL"):
            data = data.replace("SWITCH_AI2REAL", "")
            data = data.replace("END-PLACEHOLDER-END", "")
            data = data.split("SPLIT-PLACEHOLDER-SPLIT")
            user_name = str(data[0])
            length = int(data[1])
            if len(user_name) == int(length):
                return "AI2REAL", user_name

        elif data.startswith("SERV2USER"):
            data = data.replace("SERV2USER", "")
            data = data.replace("END-PLACEHOLDER-END", "")
            data = data.split("SPLIT-PLACEHOLDER-SPLIT")
            message = str(data[0])
            length = int(data[1])
            if len(message) == int(length):
                return message

        elif data.startswith("BOOLEANFLAG"):
            data = data.replace("BOOLEANFLAG", "")
            data = data.replace("END-PLACEHOLDER-END", "")
            if data == "TRUE": return "FLAG", True
            if data == "FALSE": return "FLAG", False

        else:
            return "NOT IMPLEMENTED"