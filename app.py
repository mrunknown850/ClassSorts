from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main.html")


@app.route('/process', methods=['POST'])  # type: ignore
def success():
    if request.method == 'POST':
        raw_data = request.form.to_dict()
        processData = toSettingsDict(raw_data)

        return 'Data received: {}'.format(processData)


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
