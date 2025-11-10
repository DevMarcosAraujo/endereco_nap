from flask import Flask, render_template, request, jsonify
from database import Database
import pandas as pd

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json
    results = db.search(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)