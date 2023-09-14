import tools


def main():
    # ----- READING STAGE -----
    # Read the internal config.
    internal_config = tools.readConfig()
    user_config = tools.readSettings()

    print("MODE: "+"INITIALIZE" if internal_config["isInitial"] else "CYCLE")
    print(f'CURRENT WEEK: {internal_config["currentWeek"]}')
    input('Continue? Press Enter to continue... ')

    # _____ EXECUTING _____
    if internal_config["isInitial"]:
        # First Time User
        internal_config["isInitial"] = False

        # Start action
        print("Loading datas")
        initialList = tools.file_readers(r'input\test.txt')
        initialList = tools.sortingAlgo(user_config["currentWeekNo"],
                                        user_config["rowShiftCycle"],
                                        user_config["groupShiftCycle"],
                                        user_config["groupShiftDuration"],
                                        user_config["rowShiftDuration"],
                                        initialList, True)
        genDict = tools.rawListToDict(initialList)

        print("Generating HTML...")
        tools.write_html(genDict)

        # Save Info
        tools.saveData(genDict)

        internal_config["currentWeek"] = user_config["currentWeekNo"] + 1
        tools.writeConfig(internal_config)
    else:
        print("Loading datas")
        initialList = tools.dictToRawList(tools.readData())
        # print(initialList)
        initialList = tools.sortingAlgo(internal_config["currentWeek"],
                                        user_config['rowShiftCycle'],
                                        user_config['groupShiftCycle'],
                                        user_config['groupShiftDuration'],
                                        user_config['rowShiftDuration'],
                                        initialList, False)
        genDict = tools.rawListToDict(initialList)
        # print(initialList)

        print("Generating HTML...")
        tools.write_html(genDict)

        # Save Info
        tools.saveData(genDict)

        internal_config["currentWeek"] += 1
        tools.writeConfig(internal_config)


if __name__ == "__main__":
    main()
