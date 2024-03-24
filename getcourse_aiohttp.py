import aiohttp
import asyncio
from bs4 import BeautifulSoup, ResultSet
import time


async def main():
    async with aiohttp.request(
        "POST",
        "https://webap0.ncue.edu.tw/DEANV2/Other/OB010",
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        data="sel_cls_branch=D&sel_cls_branch=&sel_scr_english=&sel_scr_english=&sel_SCR_IS_DIS_LEARN=&sel_SCR_IS_DIS_LEARN=&sel_yms_year=112&sel_yms_year=112&sel_yms_smester=2&sel_yms_smester=2&scr_selcode=&sel_cls_id=&sel_cls_id=&sel_sct_week=&sel_sct_week=&sub_name=&emp_name=&X-Requested-With=XMLHttpRequest",
    ) as day_course_response:
        day_course_rows = BeautifulSoup(
            await day_course_response.read(), "html.parser"
        ).find_all("tr")
        th = day_course_rows[0].find_all("th")
        for item in th:
            print(item.text.strip())

        columns = day_course_rows[1].find_all("td")
        for item in columns:
            print(item.text.strip())


start_time = time.time()  # 記錄開始時間
asyncio.run(main())
end_time = time.time()  # 記錄結束時間
print("Execution time: {:.2f} seconds".format(end_time - start_time))  # 顯示執行時間
