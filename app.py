from getcourse_aiohttp2 import load_into_db, selectdb, deleteTable
from waitress import serve
from flask import Flask, render_template, request, jsonify, json, Response
import sqlite3
import aiohttp
import asyncio
import time
app = Flask(__name__)


async def process_data(data):
    # 模拟异步处理数据
    await asyncio.sleep(1)
    return {"message": "Data processed successfully", "data": data}

# 註冊路由


@app.route("/")
def home():
    return render_template("search_course.html")


@app.route("/getdata", methods=["POST"])
async def getdata():
    year = request.json.get('year')
    semester = request.json.get('semester')
    print(f"get json: year = {year}, semester = {semester}")

    start_time = time.time()  # 記錄開始時間
    await deleteTable()
    await load_into_db(year=year, semester=semester)
    end_time = time.time()  # 記錄結束時間
    print("load_into_db Execution time: {:.2f} seconds".format(
        end_time - start_time))  # 顯示執行時間

    return jsonify({"message": "執行成功", "year": year, "semester": semester})


@app.route("/search", methods=["POST"])
async def search():
    data = request.json
    res = await selectdb(
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
    print(res)
    return jsonify(res)


# @app.route("/00")
# def webapi():
#     load_allcrs_into_db()

#     # render_template() 函式 : 第二個參數可以附帶資料內容
#     return render_template("data.html", title=title)

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)
    # app.run(debug=True)
