from flask import Flask, request, make_response
from flask import render_template, redirect
from bson.objectid import ObjectId
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import api.tools as processTools
import json
import os


UPLOAD_FOLDER = r'/input'
STATIC_FOLDER = r'/assets'

app = Flask(__name__)

load_dotenv(".env")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

client = MongoClient(app.config["MONGO_URI"])
databases = client["saved_cycle_data"]
collection = databases["cycle_data"]

outputTbl = {}
globConfig = {}


@app.route("/")
def index():
    cookieOpt = True if "last_config" in request.cookies else False
    return render_template("main.html", isCookie=cookieOpt)


@app.route('/print', methods=['POST', 'GET'])  # type: ignore
def success():
    global outputTbl
    global globConfig
    # Without Cookie
    if request.method == 'POST':
        # Getting the configuration datas
        raw_data = request.form.to_dict()
        processData = toSettingsDict(raw_data)
        globConfig = processData.copy()

        # Delete the old cookies

        # Getting the template file:
        file = request.files['fileUpload']
        filename = secure_filename("input_file.txt")
        file.save(r'/tmp/'+filename)

        # Processing
        outputTbl = startProcessing(r'/tmp/input_file.txt', processData)

        # Without cookie
        resp = make_response(render_template("print_output.html",
                                             tbl_table=outputTbl,
                                             isRedirected=False,
                                             groupName=globConfig["groupName"],
                                             teachT=globConfig["teachT"],
                                             classT=globConfig["classT"],
                                             weekNum=globConfig["weekNum"]))

        if processData["cookie"]:
            resp.set_cookie('last_config', json.dumps(processData))
            resp.set_cookie('input_file', json.dumps(outputTbl))
        else:
            resp.delete_cookie('last_config')
            resp.delete_cookie('input_file')

        return resp
    # Use Cookie
    elif request.method == "GET":

        # Get configuration
        cookieData = request.cookies.get("last_config")
        cookieData = json.loads(cookieData if cookieData is not None else "")
        cookieData["weekNum"] += 1

        globConfig = cookieData.copy()

        # Get previous config
        prevData = request.cookies.get("input_file")
        prevData = json.loads(prevData if prevData is not None else "")

        outputTbl = processFromDict(prevDict=prevData, config=cookieData)

        resp = make_response(render_template("print_output.html",
                                             tbl_table=outputTbl,
                                             isRedirected=False,
                                             groupName=globConfig["groupName"],
                                             teachT=globConfig["teachT"],
                                             classT=globConfig["classT"],
                                             weekNum=globConfig["weekNum"]))
        resp.set_cookie('input_file', json.dumps(outputTbl))
        resp.set_cookie('last_config', json.dumps(cookieData))

        return resp


@app.route('/raw-output')
def rawOutput():
    return render_template("output.html", tbl_table=outputTbl,
                           isRedirected=True,
                           groupName=globConfig["groupName"],
                           teachT=globConfig["teachT"],
                           classT=globConfig["classT"])


@app.route('/database/<uuid>')
def openDatabase(uuid):
    global globConfig
    returned_data = collection.find_one({"_id": ObjectId(uuid)})
    returned_data = returned_data if returned_data is not None else {}
    seatData = json.loads(returned_data['classPos'])

    return render_template("output.html", tbl_table=seatData,
                           isRedirected=False,
                           groupName=returned_data["groupName"],
                           teachT=returned_data["teachT"],
                           classT=returned_data["classT"])


@app.route('/new-url/')
def newDatabase():
    global outputTbl
    global globConfig

    id = ObjectId()
    insertionDict = {
        "_id": id,
        "classPos": json.dumps(outputTbl),
        "classT": str(globConfig["classT"]),
        "teachT": str(globConfig["teachT"]),
        "groupName": str(globConfig["groupName"])
    }

    collection.insert_one(insertionDict)
    return redirect('/database/'+str(id))


def toSettingsDict(inputDict: dict) -> dict:
    TO_INT_KEYS = {"weekNum", "rowCycle", "groupCycle",
                   "rowDur", "groupDur"}
    TO_STR_KEYS = {"sepChar", "classT", "teachT", "groupName"}
    TO_BOOL_KEYS = {"rowOff", "groupOff", "cookie"}

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


def processFromDict(prevDict: dict, config: dict) -> dict:
    rawList = processTools.dictToRawList(prevDict)
    sortList = processTools.sortingAlgo(config['weekNum'],
                                        config['rowCycle'],
                                        config["groupCycle"],
                                        config["groupDur"],
                                        config["rowDur"],
                                        rawList, False, config['rowOff'],
                                        config['groupOff'])
    sortDict = processTools.rawListToDict(sortList)
    return sortDict
