from flask import Flask, render_template, request, Markup
import subprocess
import json

from validate_articles import validate

app = Flask(__name__)

STATUS_FILE = 'computation_status.json'

@app.route('/')
def home():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('index.html', values=values, labels=labels)

@app.route('/get_status', methods=['GET'])
def get_status():
    with open(STATUS_FILE, 'r') as infile:
        data = json.load(infile)
    return json.dumps(data);

@app.route('/start_computation', methods=['POST'])
def start_computation():
    print("TESOGISGSDIGN")
    # data = request.form.get('max_turns', None)
    # print(json.dumps(data))
    # print("TESTING")
    try:
        print("1")
        start_page = request.form['start_page']
        print("2")
        end_page = request.form['end_page']
        print("3")
        max_turns = request.form['max_turns']
        print("4")
        validity = validate(start_page, end_page)
        print("5")
        if len(validity) == 0:
            print("6")
            # try:
            subprocess.Popen(["python3", "wikipedia_game.py", start_page, end_page, "-l", max_turns])
            # except Exception as e:
            #     print(str(e))
            #     print("7")
            #     return str(False)
            print(json.dumps({'errors': False}))
            return json.dumps({'errors': False})
        else:
            print(json.dumps({'errors': validity}))
            return json.dumps({'errors': validity})
    except:
        return json.dumps({'errors': True})
        return json.dumps({'errors': True})
    # return render_template('index.html')



if __name__ == '__main__':
  app.run(port=80)
