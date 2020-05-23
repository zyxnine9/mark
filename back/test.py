from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS


# 本地接口测试代码


app = Flask(__name__)
CORS(app)

@app.route('/test')
def test():
    return jsonify({'msg':[1,2,3]})

@app.route('/group',methods=['POST'])
def group():
    print(request.get_json()['dataset_name'])
    return jsonify({'group_name':['zzz','xxx','lll']})

if __name__ == '__main__':
    app.run(debug=True)
