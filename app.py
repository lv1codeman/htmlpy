from getcourse import search_courses

from flask import Flask, render_template, request, jsonify, json
import sqlite3
app = Flask(__name__)

# 註冊路由


@app.route('/data')
def webapi():
    # title = 'mytitle'
    # res = list()
    res = search_courses(crsid='00002')
    title = res[0][1]
    # render_template() 函式 : 第二個參數可以附帶資料內容
    return render_template('data.html', title=title)


@app.route('/data/message', methods=['GET'])
def getDataMessage():
    if request.method == "GET":
        with open('static/data/message.json', 'r') as f:
            data = json.load(f)
            print("text : ", data)
        f.close
        return jsonify(data)  # 直接回傳 data 也可以，都是 json 格式


@app.route('/data/message', methods=['POST'])
def setDataMessage():
    if request.method == "POST":
        data = {
            'appInfo': {
                'id': request.form['app_id'],
                'name': request.form['app_name'],
                'version': request.form['app_version'],
                'author': request.form['app_author'],
                'remark': request.form['app_remark']
            }
        }
        print(type(data))
        with open('static/data/message.json', 'w') as f:
            json.dump(data, f)
        f.close
        return jsonify(result='OK')


if __name__ == '__main__':
    app.run(debug=True)
