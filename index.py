from flask import Flask, request
from flask import render_template
from werkzeug.utils import secure_filename
import api.tools as processTools


UPLOAD_FOLDER = r'/input'
STATIC_FOLDER = r'/assets'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("main.html")


@app.route('/process', methods=['POST'])  # type: ignore
def success():
    if request.method == 'POST':
        # Getting the configuration datas
        raw_data = request.form.to_dict()
        processData = toSettingsDict(raw_data)

        # Getting the template file:
        file = request.files['fileUpload']
        filename = secure_filename("input_file.txt")
        file.save(r'/tmp/'+filename)

        # Processing
        sortTbl = startProcessing(r'/tmp/input_file.txt', processData)

        return render_template("output.html", tbl_table=sortTbl)


def toSettingsDict(inputDict: dict) -> dict:
    TO_INT_KEYS = {"weekNum", "rowCycle", "groupCycle",
                   "rowDur", "groupDur"}
    TO_STR_KEYS = {"sepChar", "classT", "teachT"}
    TO_BOOL_KEYS = {"rowOff", "groupOff"}

    outputDict = {}
    for key in inputDict:
        if key in TO_INT_KEYS:
            outputDict[key] = int(inputDict[key])
        elif key in TO_STR_KEYS:
            outputDict[key] = inputDict[key]
        elif key in TO_BOOL_KEYS:
            outputDict[key] = True if inputDict[key] == "on" else False
    for KEY in TO_BOOL_KEYS:
        if KEY not in outputDict:
            outputDict[KEY] = False
    return outputDict


def startProcessing(fileLocation: str, config: dict) -> dict:
    rawList = processTools.file_readers(fileLocation,
                                        divider=config["sepChar"])
    sortList = processTools.sortingAlgo(config['weekNum'],
                                        config['rowCycle'],
                                        config["groupCycle"],
                                        config["groupDur"],
                                        config["rowDur"],
                                        rawList, True, config['rowOff'],
                                        config['groupOff'])
    sortDict = processTools.rawListToDict(sortList)
    return sortDict
