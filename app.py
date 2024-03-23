from getcourse import search_courses, load_allcrs_into_db, selectdb, deleteTable
from waitress import serve
from flask import Flask, render_template, request, jsonify, json
import sqlite3

app = Flask(__name__)


# 註冊路由
@app.route("/")
def home():
    return render_template("page.html")


@app.route("/search", methods=["POST"])
def search():
    # res = selectdb(crsclass="", tchnm="羅家玲")
    # return jsonify(res)
    data = request.json
    res = selectdb(
        year=data.get("year"),
        semester=data.get("semester"),
        crsclass=data.get("crsclass"),
        week=data.get("week"),
        is_all_eng=data.get("isAllEng"),
        is_dis_learn=data.get("isDisLearn"),
        crsid=data.get("crsid"),
        crsnm=data.get("crsnm"),
        tchnm=data.get("tchnm"),
        crslimit=data.get("crslimit"),
    )
    # print(res)
    return jsonify(res)


# @app.route("/00")
# def webapi():
#     load_allcrs_into_db()

#     # render_template() 函式 : 第二個參數可以附帶資料內容
#     return render_template("data.html", title=title)

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)
    # app.run(debug=True)
