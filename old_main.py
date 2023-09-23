import tools


def main(isInitial: bool, i: int = 1):
    # ----- READING STAGE -----
    # Read the internal config.
    internal_config = tools.readConfig()
    user_config = tools.readSettings()

    # _____ EXECUTING _____
    if isInitial:
        print("CHOSEN MODE: INITIALIZE")
        print(f'Initialize from Week {user_config["currentWeekNo"]}')
        input("Press enter to continue...")

        # First Time User
        isInitial = False

        print("===== EXECUTION =====")
        # Start action
        print("Loading datas")
        initialList = tools.file_readers(r'input\input_layout.txt',
                                         user_config["seperationChar"])
        initialList = tools.sortingAlgo(user_config["currentWeekNo"],
                                        user_config["rowShiftCycle"],
                                        user_config["groupShiftCycle"],
                                        user_config["groupShiftDuration"],
                                        user_config["rowShiftDuration"],
                                        initialList, True,
                                        user_config["rowDurationOffset"],
                                        user_config["groupDurationOffset"])
        genDict = tools.rawListToDict(initialList)

        print("Generating HTML...")
        tools.write_html(genDict, user_config["classEntranceTitle"],
                         user_config["teachersTableTitle"])

        # Save Info
        tools.saveData(genDict)

        internal_config["currentWeek"] = user_config["currentWeekNo"]
        tools.writeConfig(internal_config)
    else:
        print("CHOSEN MODE: CYCLE")
        print(f'Currently Week {internal_config["currentWeek"]}')
        print(f'Generating Week {internal_config["currentWeek"]+1}')
        input("Press Enter to continue... ")

        print("===== EXECUTION =====")
        print("Loading datas")
        initialList = tools.dictToRawList(tools.readData())
        # print(initialList)
        initialList = tools.sortingAlgo(internal_config["currentWeek"],
                                        user_config['rowShiftCycle'],
                                        user_config['groupShiftCycle'],
                                        user_config['groupShiftDuration'],
                                        user_config['rowShiftDuration'],
                                        initialList, False,
                                        user_config["rowDurationOffset"],
                                        user_config["groupDurationOffset"])
        genDict = tools.rawListToDict(initialList)
        # print(initialList)

        print("Generating HTML...")
        tools.write_html(genDict, user_config["classEntranceTitle"],
                         user_config["teachersTableTitle"], i)

        # Save Info
        tools.saveData(genDict)

        internal_config["currentWeek"] += 1
        tools.writeConfig(internal_config)


if __name__ == "__main__":
    print("======== Class Seat Sorters ========")
    print("Choose your mode:")
    print("I - INITIALIZE MODE")
    print("C - CYCLE MODE")

    # Loop for pre-generate
    # for i in range(1, 102):
    #     main(False, i)

    option = input("Enter your option: ")
    while option not in ["I", "C"]:
        option = input("Enter your option: ")

    main(False if option == "C" else True)
