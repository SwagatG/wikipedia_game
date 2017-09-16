from flask import Flask, render_template, request
import subprocess
import json

app = Flask(__name__)

STATUS_FILE = 'computation_status.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_status', methods=['GET'])
def get_status():
    with open(STATUS_FILE, 'r') as infile:
        data = json.loads(infile)
    return data

@app.route('/start_computation', methods=['POST'])
def start_computation():
    data = request.get_json()
    validity = validate_articles(data['start_page'], data['end_page'])
    if validity:
        subprocess.popen("python3 wikipedia_game.py " + data['start_page']
                         + " " + data['end_page'], + " -l " + data['max_turns'])
        return True
    else:
        return False



if __name__ == '__main__':
  app.run(port=80)
