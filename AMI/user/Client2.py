from Client import Client

if __name__ == "__main__":
    main = Client("10.2.24.35", "10.2.24.35", self_port=10083)
    main.start()

    while True:
        main.non_blocking_cmdline()