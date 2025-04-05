import sys
import time
import socket
import select
import threading

from Communication import BaseProtocol


class Client:
    def __init__(self, server_ip, self_ip, server_port=10081, self_port=10082, debug=True):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

        self.server_ip = server_ip
        self.server_port = server_port
        self.sock.bind((self_ip, self_port))

        self.username = str()
        self.friends = []

        self.ifCONT = False
        self.ifREG = False
        self.debug = debug
        self.PARSER = BaseProtocol.Protocol()

        self.INIT = 1

        print("LOG: DEBUG = {}".format(self.debug))

    def THREAD_CONNECT2SERVER(self):
        while True:
            try:
                self.sock.connect((self.server_ip, self.server_port))
                print(f'CONNECTED TO {self.server_ip}:{self.server_port}')
                self.ifCONT = True
                break
            except Exception as Error:
                print(Error)
            time.sleep(0.1)

    def THREAD_RECV_MES(self):
        while True:
            from_user, rst = self.recv_message()
            print("RECV MESSAGE FROM {}: {}".format(from_user, rst))
            time.sleep(0.1)

    def getFriendList(self):
        return self.friends


    def recv_data(self):
        data = self.sock.recv(1024).decode('utf-8')
        if self.debug: print("LOG: DATA RECEIVED FROM SERVER: {}".format(data))
        data = self.PARSER.parse_data(data)
        return data

    # Register an user to the database
    def register_user(self, user_name: str, description: str):
        data = self.PARSER.create_user(user_name, description)
        self.sock.send(data.encode('utf-8'))

        while True:
            try:
                data = self.recv_data()
                if self.debug: print("LOG: COMMAND PARSED: {}".format(data))
                if data[0] == "FLAG" and data[1]:
                    self.username = user_name
                    self.ifREG = True
                    print("USER REGISTERED")
                    return True
                else:
                    time.sleep(0.1)
            except Exception as Error:
                print(Error)
                pass

    # Send data to an AI or an user
    def send_data2user(self, dest_user_name: str, data: str):
        if self.ifREG:
            data = self.PARSER.send_data2user(self.username, dest_user_name, data)
            self.sock.send(data.encode('utf-8'))
        else:
            print("USER NOT REGISTERED YET")

    # Receive data from the ai
    def recv_message(self):
        data = self.recv_data()
        from_user = data[0]
        message = data[1]
        if from_user == "SERVER": from_user = "AI"

        return from_user, message

    # Swap an AI with an User
    def change_AI2Real(self):
        if self.ifREG:
            data = self.PARSER.switch_AI2Real(self.username)
            self.sock.send(data.encode("utf-8"))
            time.sleep(0.5)
        else:
            print("USER NOT REGISTERED YET")
            return "NOT REGISTER"

    def start(self):
        threading.Thread(target=self.THREAD_CONNECT2SERVER, daemon=True).start()
        threading.Thread(target=self.THREAD_RECV_MES, daemon=True).start()

    def THREAD_RECV_MES(self):
        while True:
            from_user, rst = self.recv_message()
            print("RECV MESSAGE FROM {}: {}".format(from_user, rst))
            time.sleep(0.1)

    def non_blocking_cmdline(self):
        flag = select.select([sys.stdin], [], [], 0.0)[0]
        if flag:
            try:
                line = sys.stdin.readline().rstrip()
                if line == "help":
                    print("REG: REGISTER YOURSELF INTO THE SERVER. THIS METHOD TAKES TWO ARGUMENTS: YOUR NAME AND DESCRIPTION")
                    print("SEND: SEND MESSAGE TO SOMEONE. THIS METHOD TAKES TWO ARGUMENTS: DEST-RECEIVER, MESSAGE.\n"
                          "SEPARATE EACH ARGUMENT BY #. SEND TO AI EXAMPLE:   SEND#AI#Hello")
                    print("RECV: RECEIVE MESSAGE FROM SOMEONE. THIS METHOD WILL RETURN A MESSAGES FROM OTHER USERS OR AI")
                    print("CHANGE: SWITCH TO A REAL PERSON IF POSSIBLE, THAT YOUR PREFERENCE MATCHES WITH ANOTHER USER")

                #Registering an user calling register_user
                elif line.startswith("REG"):
                    line = line.replace("REG", "")
                    _, name, description = list(line.split(" "))
                    self.register_user(name, description)
                #Send a message to an user or AI calling send_data2user
                elif line.startswith("SEND"):
                    line = line.replace("SEND", "")
                    _, dest, msg = list(line.split("#"))
                    self.send_data2user(dest, msg)

                # elif line.startswith("RECV"):
                #    from_user, rst = self.recv_message()
                #     print("RECV MESSAGE FROM {}: {}".format(from_user, rst))

                #Swap the AI with a real user calling change_AI2Real

                elif line.startswith("CHANGE"):
                    self.change_AI2Real()
                #Error
                else:
                    print("COMMAND NOT FOUND: {}".format(str(line)))

            except Exception as Error:
                print(Error)
                print("COMMAND NOT FOUND: {}".format(str(line)))
        else: pass


if __name__ == "__main__":
    main = Client("10.2.24.35", "10.2.24.35", self_port=10082, debug=False)
    main.start()

    while True:
        main.non_blocking_cmdline()