import os
import time
import socket
import threading

from Storage import Storage
from AIFriend import BaseAI
from Communication import BaseProtocol


OPENAI_API_KEY = "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"


class MainServer:
    def __init__(self, ip, port, debug=True):
        os.system("fuser -k 10080/tcp")  # KILL SOCKET PORT IF BLOCKED BY PROGRAM (UNIX PLATFORM)
        self.debug = debug
        self.STORAGE = Storage.Storage(debug=False)
        self.PARSER = BaseProtocol.Protocol()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

        self.clients = []
        self.registered_user = {}
        self.registered_user_names = []

        self.sock.bind((ip, port))
        self.sock.listen()
        print(f'SERVER STARTED，LISTENING ON {port}')

        # TODO -- ALL FURTHER FUNCTION SHOULD BE ADDED BEFORE THREAD_USER_ACK --
        self.THREAD_USER_ACK()

    # HANDLE ALL SOCKET CONNECTION RAISED BY CLIENTS
    def handle_client(self, sock, addr):
        while True:
            try:
                data = sock.recv(1024).decode('utf-8')  # RECV DATA FROM USER
                if not data: break
                action = self.PARSER.parse_data(data)

                if self.debug: print("LOG: DATA FROM {}: {}".format(addr, data))
                if self.debug: print("LOG: ACTION: {}".format(action))

                if action[0] == "SEND2USER":
                    sour_user = action[1]
                    dest_user = action[2]
                    user_description = self.STORAGE.get_user_description(sour_user)
                    message = action[3]
                    print("LOG: MESSAGE FROM {}, TO {}: {}".format(sour_user, "AI" if dest_user == "AI" else dest_user, message))

                    if dest_user == "AI":
                        AI4USER = self.STORAGE.get_AIhistory(sour_user)
                        rst = AI4USER.user_input(str(message))
                        if self.debug: print("LOG: MESSAGE FROM AI TO USER {}, {}".format(sour_user, rst))
                        print(self.PARSER.serv2user(rst))
                        sock.send(self.PARSER.serv2user(rst).encode(), socket.MSG_NOSIGNAL)
                    else:
                        try:
                            # TODO: IMPLEMENT SEND DATA TO ADDED FRIEND
                            dest_user = self.registered_user["USER_ID"+dest_user]
                            dest_user["sock"].send(self.PARSER.serv2user(sour_user + " send you a message: " + message).encode('utf-8'), socket.MSG_NOSIGNAL)
                        except Exception as e:
                            sock.send(self.PARSER.serv2user("USER NOT REGISTERED OR WRONG DESTINATION").encode("utf-8"), socket.MSG_NOSIGNAL)

                elif action[0] == "CREATE":
                    self.registered_user["USER_ID"+action[1]] = ({"username": action[1], "description": action[1], "addr": (addr[0], addr[1]), "sock": sock})
                    self.registered_user_names.append(str("USER_ID"+action[1]))
                    self.STORAGE.create_new_user(name=action[1], descriptions=action[1])
                    self.STORAGE.set_user_AIHistory(name=action[1], history=BaseAI.BaseAI(OPENAI_API_KEY))
                    for i in range(0, 3):
                        sock.send(self.PARSER.TRUE().encode(), socket.MSG_NOSIGNAL)
                        time.sleep(0.1)
                        if self.debug: print("LOG: SERVER SEND ACK COMMAND TO USER")
                    time.sleep(0.1)

                elif action[0] == "SWITCH_AI2REAL":
                    threading.Thread(target=self.THREAD_SYN_USERPERSONALITY, daemon=False).start()
            except  Exception as Error:
                if self.debug: print("LOG: ERROR: {}".format(Error))
                break

        sock.close()


    # Pairing Users together
    def THREAD_SYN_USERPERSONALITY(self, user_name):
        if self.debug: print("START SYN USER PERSONALITY")

        target_user = self.STORAGE.get_user_description("USER_ID_" + user_name)
        judge = BaseAI.BaseAI(OPENAI_API_KEY)

        for user in self.registered_user_names:
            user_profile2compare = self.STORAGE.get_user_description(user)
            rst = judge.isSimilar(target_user, user_profile2compare)
            if rst:
                target_user_addr = self.registered_user["USER_ID_" + user_name]
                target_user_addr["sock"].send(self.PARSER.serv2user("YOU ARE PAIRED WITH {}".format(user.replace("USER_ID_", "")).encode("utf-8")), socket.MSG_NOSIGNAL)
                target_user_addr["sock"].send(self.PARSER.serv2user("WE WISH YOU DEVELOP A GOOD RELATION WITH THEM".encode("utf-8")), socket.MSG_NOSIGNAL)

                paired_user_addr = self.registered_user[user]
                paired_user_addr["sock"].send(self.PARSER.serv2user("YOU ARE PAIRED WITH {}".format(user_name).encode("utf-8")), socket.MSG_NOSIGNAL)
                paired_user_addr["sock"].send(self.PARSER.serv2user("WE WISH YOU DEVELOP A GOOD RELATION WITH THEM".encode("utf-8")),socket.MSG_NOSIGNAL)

        '''
        userbot_list = []

        for user in self.registered_user_names:
            AI = self.STORAGE.get_AIhistory(user)
            BOT_personality = AI.export_AIPersonality()
            USER_personality = AI.export_AIPersonality()
            self.STORAGE.set_user_Personality(user, USER_personality)
            self.STORAGE.set_bot_Personality(user, BOT_personality)

            userbot_list.append([user, USER_personality, BOT_personality])

        judge = BaseAI.BaseAI(OPENAI_API_KEY)
        tmp_user = ""
        for userboti in userbot_list:
            tmp_user = userboti[1]
            for userbotj in userbot_list:
                tmp_bot = userbotj[2]
                if judge.isSimilar(tmp_user, tmp_bot):
                    dest_user = self.registered_user[userbotj[0]]
                    dest_user["sock"].send(self.PARSER.serv2user("YOU ARE PAIRED WITH {}".format(userboti[0]).encode("utf-8")), socket.MSG_NOSIGNAL)

                    sour_user = self.registered_user[userboti[0]]
                    sour_user["sock"].send(self.PARSER.serv2user("YOU ARE PAIRED WITH {}".format(userbotj[0]).encode('utf-8')), socket.MSG_NOSIGNAL)
        '''

    def THREAD_USER_ACK(self):
        while True:
            cli_sock, cli_addr = self.sock.accept()
            self.clients.append(cli_sock)  #
            print(f'USER CONNECTED：{cli_addr[0]}:{cli_addr[1]}')
            client_thread = threading.Thread(target=self.handle_client, args=(cli_sock, cli_addr))
            client_thread.start()


if __name__ == '__main__':
    main = MainServer("10.2.24.35", 10081)