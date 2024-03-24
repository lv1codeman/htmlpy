import aiohttp
import asyncio
from bs4 import BeautifulSoup
import sqlite3
import time


async def main():
    async with aiohttp.request(
        "POST",
        "https://webap0.ncue.edu.tw/DEANV2/Other/OB010",
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        data="sel_cls_branch=D&sel_cls_branch=&sel_scr_english=&sel_scr_english=&sel_SCR_IS_DIS_LEARN=&sel_SCR_IS_DIS_LEARN=&sel_yms_year=112&sel_yms_year=112&sel_yms_smester=2&sel_yms_smester=2&scr_selcode=&sel_cls_id=&sel_cls_id=&sel_sct_week=&sel_sct_week=&sub_name=&emp_name=&X-Requested-With=XMLHttpRequest",
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

            # columns_rows.append(data_dict)
        conn.commit()
        conn.close()


start_time = time.time()  # 記錄開始時間
asyncio.run(main())
end_time = time.time()  # 記錄結束時間
print("Execution time: {:.2f} seconds".format(end_time - start_time))  # 顯示執行時間
