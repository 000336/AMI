from BaseAI import BaseAI

OPENAI_API_KEY = "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"


if __name__ == "__main__":
    AI4USER1 = BaseAI(OPENAI_API_KEY, debug=False)
    rst = AI4USER1.user_input("Hello")
    rst = AI4USER1.user_input("I like dogs")
    rst = AI4USER1.user_input("Do you like dogs")

    AI4USER2 = BaseAI(OPENAI_API_KEY, debug=False)
    rst2 = AI4USER1.user_input("Hello")
    rst2 = AI4USER1.user_input("I like dogs")
    rst2 = AI4USER1.user_input("Do you like dogs")

    a1 = AI4USER1.export_AIPersonality()
    u2 = AI4USER2.exportUSERPersonality()
    print(a1)
    print(u2)
    rst = AI4USER1.isSimilar(a1, u2)
    print(rst, "###")