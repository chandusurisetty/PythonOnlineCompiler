from flask import Flask, render_template, request, jsonify
import threading

from solution import Analay
app = Flask(__name__)


class RunnerThread(threading.Thread):
    def __init__(self, code):
        threading.Thread.__init__(self)
        self.code = code

    def run(self):
        global result
        try:
            anan = Analay(self.code)

            result = anan.solution()
            print(result)
        except Exception as e:
            print(str(e))
            result = str(e)


result = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getme", methods=["POST", "GET"])
def getMe():
    data = request.json
    print(data)
    # output = StringIO()
    inputList = data['inputs'].split("\n")
    inputInd = 0
    inputList = [i for i in inputList if i != ""]

    if len(inputList) != data['code'].count("input()"):
        return jsonify({"message": "Invalid inputs \n Note:- Read below points "})
    while "input()" in data["code"]:
        data["code"] = data["code"].replace(
            "input()", f'"{inputList[inputInd]}"', 1)
        inputInd += 1
    # analus = Analay(data["code"])
    # prd = analus.solution()
    global result
    result = None
    runner = RunnerThread(data["code"])
    runner.start()
    runner.join(timeout=3)
    if runner.is_alive():
        result = {"message": "The Code contains Infinity loop please check it"}

    return result


if __name__ == "__main__":
    app.run(debug=True)
