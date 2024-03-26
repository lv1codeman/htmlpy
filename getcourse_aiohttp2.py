import aiohttp
import asyncio
from bs4 import BeautifulSoup
import sqlite3
import time
from util import gen_search_res


async def load_into_db(year="112", semester="2"):
    async with aiohttp.request(
        "POST",
        "https://webap0.ncue.edu.tw/DEANV2/Other/OB010",
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        data=f"sel_cls_branch=D&sel_scr_english=&sel_SCR_IS_DIS_LEARN=&sel_yms_year={year}&sel_yms_smester={semester}&scr_selcode=&sel_cls_id=&sel_sct_week=&sub_name=&emp_name=&X-Requested-With=XMLHttpRequest",
    ) as day_course_response:
        html_data = await day_course_response.text()
        day_course_rows = BeautifulSoup(html_data, "html.parser").find_all("tr")

        # 提取表格頭（th）和數據（columns）
        th_row = day_course_rows[0].find_all("th")
        # columns_row = day_course_rows[1].find_all("td")

        conn = sqlite3.connect("database.sqlite3")
        c = conn.cursor()

        # 每筆INSERT INTO
        for i in range(1, len(day_course_rows)):
            columns_row = day_course_rows[i].find_all("td")
            data_dict = {}
            for th, td in zip(th_row, columns_row):
                if th.text.strip() == "上課節次+地點":
                    data_dict["上課節次地點"] = td.text.strip()
                elif th.text.strip() == "開課班別(代表)":
                    data_dict["開課班別"] = td.text.strip()
                else:
                    data_dict[th.text.strip()] = td.text.strip()
            columns = ", ".join(data_dict.keys())
            placeholders = ", ".join(["?"] * len(data_dict))
            insert_sql = f"INSERT INTO courses ({columns}) VALUES ({placeholders})"
            c.execute(insert_sql, list(data_dict.values()))

            update_sql = f"UPDATE courses SET 學年度={year}, 學期={semester} WHERE 課程代碼=課程代碼;"
            c.execute(update_sql)
            # columns_rows.append(data_dict)
        conn.commit()
        conn.close()


async def selectdb(
    year="112",
    semester="2",
    crsid="",
    crsclass="",
    crsnm="",
    is_all_eng="",
    is_dis_learn="",
    crslimit="",
    tchnm="",
    week="",
):

    conn = sqlite3.connect("database.sqlite3")
    cursor = conn.cursor()
    query = """
        SELECT
        ROW_NUMBER() OVER (ORDER BY 序號) AS 查詢序號,
        *
        FROM courses
        WHERE 1=1
    """

    if crsid:
        query += f" AND 課程代碼 = '{crsid}'"
    if crsclass:
        query += f" AND 開課班別 = '{crsclass}'"
    if crslimit:
        query += f" AND 可跨班 = '{crslimit}'"
    if is_all_eng:
        query += f" AND 全英語授課 = '{is_all_eng}'"
    if is_dis_learn == "是":
        query += f" AND 備註 like '%遠距課程%'"
    if is_dis_learn == "否":
        query += f" AND 備註 not like '%遠距課程%'"

    query += f" AND 課程名稱 like '%{crsnm}%'"
    query += f" AND 教師姓名 like '%{tchnm}%'"

    cursor.execute(query)
    res = cursor.fetchall()

    select_res = gen_search_res(res)
    # print(select_res)
    conn.commit()
    conn.close()
    return select_res


async def selectdb1():
    conn = sqlite3.connect("database.sqlite3")
    cursor = conn.cursor()
    query = "select * from courses limit 1"
    cursor.execute(query)
    res = cursor.fetchall()
    resv = {"year": res[0][0], "semester": res[0][1]}
    # print("year={}, sem={}".format(resv["year"], resv["semester"]))

    return resv


async def deleteTable(tablenm="courses"):
    conn = sqlite3.connect("database.sqlite3")
    cursor = conn.cursor()
    query = f"DELETE FROM " + tablenm + ";"
    cursor.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    start_time = time.time()  # 記錄開始時間
    # asyncio.run(deleteTable())
    # asyncio.run(load_into_db(year="112", semester="1"))
    select_res = asyncio.run(selectdb1())

    # print(select_res[0])

    end_time = time.time()  # 記錄結束時間
    print(
        "Execution time: {:.2f} seconds".format(end_time - start_time)
    )  # 顯示執行時間
