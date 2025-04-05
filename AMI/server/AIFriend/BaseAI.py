import copy
import openai as ai


class BaseAI:
    def __init__(self, api, init_mes="", model="gpt-4o", debug=True):
        self.init_mes = ("You are simulating to be my friend and you will try to act in the way that I ask. " + init_mes)
        self.model = model
        self.history = []
        self.history.append({"role": "user", "content": self.init_mes})
        self.debug = debug
        self.client = ai.OpenAI(api_key=api)

    def user_input(self, data):
        if str(data).lower() == 'exit': return "BYE"

        self.history.append({"role": "user", "content": data})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            n=1,
            stop=None,
            stream=False
        )

        response = response.choices[0].message.content.strip()
        self.history.append({"role": "system", "content": response})

        if self.debug: print("USER INPUT: {} \nRESPONSE: {}\n".format(data, response))
        return response

    def export_AIPersonality(self):
        history = copy.deepcopy(self.history)
        cmd = 'Describe what type of friend I prefer. Include my hobbies, my preference, my characters, my motivations and etc'
        history.append({"role": "user", "content": cmd})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=history,
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            n=1,
            stop=None,
            stream=False
        )

        response = response.choices[0].message.content.strip()

        if self.debug: print("AI PERSONALITY: {}\n".format(response))
        return response

    def exportUSERPersonality(self):
        history = copy.deepcopy(self.history)
        cmd = 'Describe what type of friend am I. Include my hobbies, my preference, my characters, my motivations and etc'
        history.append({"role": "user", "content": cmd})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=history,
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            n=1,
            stop=None,
            stream=False
        )

        response = response.choices[0].message.content.strip()

        if self.debug: print("USER PERSONALITY: {}\n".format(response))
        return response

    def isSimilar(self, user1, user2):
        history = []
        cmd = 'Compare the two personality if they are similar: 1: {}, 2: {}, answer me in True/False answer'.format(user1, user2)
        history.append({"role": "user", "content": cmd})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=history,
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            n=1,
            stop=None,
            stream=False
        )

        response = response.choices[0].message.content.strip()

        if self.debug: print("SIMILARITY: {}\n".format(response))

        if "false" in response.lower(): return False
        if "true" in response.lower(): return True
        else: self.isSimilar(user1, user2)
