#coding:utf-8
from flask import Flask, render_template, jsonify, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/postfiles',methods=['POST'])
def post_files():
    file_ = request.files.get('dataset')
    print(type(file_))
    name = file_.filename
    file_.save("./datas/{}".format(name))
    return jsonify({'msg':'OK'})

if __name__ == '__main__':
    app.run(debug=True)