from flask import Flask, render_template, request
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

if __name__ == '__main__':
  app.run(port=80)
