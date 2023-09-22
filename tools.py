import json


def readData() -> dict:
    with open(r'input\saved_info.json', 'r') as f:
        return json.loads(f.read())


def saveData(groupingData: dict) -> None:
    with open(r'input\saved_info.json', 'w') as f:
        f.write(json.dumps(groupingData))


def readSettings() -> dict:
    settingDict = {}
    with open(r'input\settings.json', 'r', encoding="UTF-8") as f:
        settingDict = json.loads(f.read())
    return settingDict


def readConfig() -> dict:
    with open(r'input\internal_config.json', 'r') as f:
        return json.loads(f.read())


def writeConfig(internalData: dict) -> None:
    with open(r'input\internal_config.json', 'w') as f:
        f.write(json.dumps(internalData))


# Convert from pure Text to Filterized List
def file_readers(file_path: str, divider: str = " | ") -> list:
    output = []
    with open(file_path, "r", encoding="UTF-8") as f:
        extracted_str = f.readlines()
    rowCounter = 0
    for lineID in range(len(extracted_str)):
        if lineID == 0:
            output.append([])
        elif extracted_str[lineID] == '\n':
            output.append([])
            rowCounter += 1
            continue
        output[rowCounter].append(
            list(map(lambda inStr: inStr.replace('\n', ''), extracted_str[lineID].split(divider))))

    return output


# Convert from Filterized List to Readable Dictionary
def rawListToDict(filterizedList: list) -> dict:
    result = {}
    currentRowID = 0
    for rows in filterizedList:
        result[currentRowID] = {}

        currentGroupID = 0
        for groups in rows:
            result[currentRowID][currentGroupID] = {}

            currentItemID = 0
            for item in groups:
                result[currentRowID][currentGroupID][currentItemID] = item
                currentItemID += 1

            currentGroupID += 1

        currentRowID += 1
    return result


# Convert Readable Dictionary to Filterized List
def dictToRawList(inDict: dict) -> list:
    output = []

    rowID = 0
    for row in inDict:
        output.append([])

        groupID = 0
        for group in inDict[row]:
            output[rowID].append([])

            for seat in inDict[row][group]:
                output[rowID][groupID].append(inDict[row][group][seat])
            groupID += 1
        rowID += 1

    return output


def sortingAlgo(weekCount: int, rowShiftCycle: int, groupShiftCycle: int,
                groupShiftDuration: int, rowShiftDuration: int,
                filteredList: list, isInitial: bool, rowOffset: bool,
                groupOffset: bool) -> list:

    outputList = filteredList.copy()

    if isInitial:
        if weekCount == 0:
            return outputList
        for weekCycle in range(weekCount):
            if weekCycle == 1:
                continue
            # Perform rowShift
            if weekCount % rowShiftDuration == 0 and not rowOffset:
                tempList = (outputList[-rowShiftCycle:]
                            + outputList[:-rowShiftCycle])
                outputList = tempList.copy()
            elif weekCount % rowShiftDuration == 1 and rowOffset:
                tempList = (outputList[-rowShiftCycle:]
                            + outputList[:-rowShiftCycle])
                outputList = tempList.copy()

            # Perform groupShift
            if weekCount % groupShiftDuration == 0 and not groupOffset:
                tempList = []
                for row in outputList:
                    tempList.append(row[groupShiftCycle:]
                                    + row[:groupShiftCycle])
                outputList = tempList.copy()
            elif weekCount % groupShiftDuration == 1 and groupOffset:
                tempList = []
                for row in outputList:
                    tempList.append(row[groupShiftCycle:]
                                    + row[:groupShiftCycle])
                outputList = tempList.copy()
        # return outputList
    else:
        if weekCount % rowShiftDuration == 0:
            tempList = (outputList[-rowShiftCycle:]
                        + outputList[:-rowShiftCycle])
            outputList = tempList.copy()

            # Perform groupShift
        if weekCount % groupShiftDuration == 0:
            tempList = []
            for row in outputList:
                tempList.append(row[groupShiftCycle:]
                                + row[:groupShiftCycle])
            outputList = tempList.copy()
    return outputList


def write_html(tbl_arrange: dict, classEntrance: str, teachersTable: str,
               i=None) -> None:
    outputStr = ""
    HEAD_SECTION = r'<html><head><link rel="stylesheet" href="print.css"><link rel="stylesheet" media="print" href="print.css"></head><body class="grid">'
    body = ""
    END_SECTION = r'</body></html>'

    for rows in tbl_arrange:
        body += "<div>"

        for seatSet in tbl_arrange[rows]:
            body += "<div>"

            for seat in tbl_arrange[rows][seatSet]:
                body += f'<div>{tbl_arrange[rows][seatSet][seat]}</div>'
            body += "</div>"
        if rows == max(list(tbl_arrange.keys())):
            body += rf'<p class="bgv">{teachersTable}</p></div>'
            continue
        elif rows == 0:
            body += rf'<p class="cl">{classEntrance}</p></div>'
        body += r'</div>'
    outputStr = HEAD_SECTION + body + END_SECTION
    with open(f'{"output" if i == None else i}.html', "w", encoding="UTF-8") as f_out:
        f_out.write(outputStr)
