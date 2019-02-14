from flask import Flask, jsonify

app = Flask(__name__)

stores = [
    {
        'name': '1',
        'data': 'store 1 data'
    },
    {
        'name': '2',
        'data': 'store 2 data'
    },
    {
        'name': '3',
        'data': 'store 3 data'
    }
]


@app.route('/store/<string:name>', methods=['GET'])
def get_stores(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)

app.run(port=8000, debug=True)