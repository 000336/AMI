from BaseProtocol import Protocol


if __name__ == '__main__':
    parser = Protocol()
    rst = parser.switch_AI2Real("user1")
    print(rst, "1")

    rst = parser.parse_data(rst)
    print(rst, "2")