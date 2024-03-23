# 載入需要的套件
import numpy as np
from util import (
    get_num_column_dict,
    is_contain_chinese,
    getSyllabusColumns,
    gen_search_res,
)
import sqlite3

# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from selenium.webdriver.chrome.options import Options
import logging

logging.getLogger().setLevel(logging.INFO)
logging.info("search_courses start...")
# logging.error("this is errrrrr.")


def search_courses(
    year="112",
    semester="2",
    crsid="",
    crsclassID="",
    crsnm="",
    is_all_eng="",
    is_dis_learn="",
    crossclass="",
    tchnm="",
    week="",
):
    # 開啟瀏覽器視窗(Chrome)
    # 方法一：執行前需開啟chromedriver.exe且與執行檔在同一個工作目錄
    print("start Chrome")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://webapt.ncue.edu.tw/DEANV2/Other/ob010")
    print("END Chrome")

    # 指定條件區的輸入
    # 指定學年度<select>
    select_element = driver.find_element(By.ID, "ddl_yms_year")
    select = Select(select_element)
    select.select_by_value(year)
    # 指定學期<select>
    select_element = driver.find_element(By.ID, "ddl_yms_smester")
    select = Select(select_element)
    select.select_by_value(semester)

    # 指定課程代碼<input>
    if len(crsid) == 5:
        select_element = driver.find_element(By.ID, "scr_selcode")
        select_element.send_keys(crsid)

    select_element = driver.find_element(By.ID, "sub_name")
    select_element.send_keys(crsnm)

    select_element = driver.find_element(By.ID, "emp_name")
    select_element.send_keys(tchnm)

    select = Select(driver.find_element(By.ID, "ddl_cls_type"))
    select.select_by_value(is_all_eng)
    select = Select(driver.find_element(By.ID, "ddl_SCR_IS_DIS_LEARN"))
    select.select_by_value(is_dis_learn)
    select = Select(driver.find_element(By.ID, "ddl_sct_week"))
    select.select_by_value(week)

    # 指定修課班別<select>
    select = Select(driver.find_element(By.ID, "ddl_scj_cls_id"))
    select.select_by_value(crsclassID)

    # 點擊「查詢」按鈕
    button = driver.find_element(By.XPATH, "//input[@value='查詢']")
    button.click()

    delay = 10  # seconds

    try:
        # 直到開課課程列表的序號出現
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tb_01"))
        )
        print("Page is ready!")
        # 畫面截圖（檢查用）
        driver.save_screenshot("python_test.png")

        html = driver.page_source
        driver.close()  # 關閉瀏覽器
        soup = BeautifulSoup(html, "html.parser")

        results = soup.find(id="result")
        results_row = results.select("tbody tr")

        # 搜尋到的資料筆數 = row的大小
        row = len(results_row)
        # 建立放output的陣列
        output = [[0] * 20 for i in range(row)]

        results = results.select("tbody td")

        i = 0
        deli = 0
        unit = ""  # 開課單位

        for result in results:
            if result.get("data-th") == "課程代碼：":
                output[i][0] = result.get_text()
            elif result.get("data-th") == "開課班別(代表)：":
                output[i][1] = result.get_text()
                unit = result.get_text()
            elif result.get("data-th") == "課程名稱：":
                course_name_all = result.text.split("\n")
                course_name_list = list()
                for ele in course_name_all:
                    if len(ele.strip()) >= 2:
                        course_name_list.append(ele.strip())
                if len(course_name_list) > 1:
                    output[i][2] = course_name_list[0]
                    output[i][3] = course_name_list[1]
                else:
                    output[i][2] = course_name_list[0]
                    output[i][3] = ""
            elif result.get("data-th") == "教學大綱：":
                hasCHT = not "無檔案" in result.text
                hasENG = not "No file" in result.text
                res = getSyllabusColumns(result, hasCHT, hasENG)
                output[i][4] = res[0]
                output[i][5] = res[1]
                output[i][6] = res[2]
            elif result.get("data-th") == "課程性質：":
                output[i][7] = result.get_text()
            elif result.get("data-th") == "課程性質2：":
                output[i][8] = result.get_text()
            elif result.get("data-th") == "全英語授課：":
                output[i][9] = result.get_text()
            elif result.get("data-th") == "學分：":
                output[i][10] = result.get_text()
            elif result.get("data-th") == "教師姓名：":
                teacher_list = list()
                teachers = result.find_all("span")
                for teacher in teachers:
                    teacher_list.append(teacher.get_text())
                teachers = ",".join(str(element) for element in teacher_list)
                output[i][11] = teachers.strip()
            elif result.get("data-th") == "上課大樓：":
                output[i][12] = result.get_text()
            elif result.get("data-th") == "上課節次+地點：":
                output[i][13] = result.get_text()
            elif result.get("data-th") == "上限人數：":
                output[i][14] = result.get_text()
            elif result.get("data-th") == "登記人數：":
                output[i][15] = re.sub(r"\s+", "", result.get_text())
            elif result.get("data-th") == "選上人數：":
                output[i][16] = result.get_text()
                if int(result.get_text()) < 10:
                    if ("碩" in unit) & (int(result.get_text()) >= 3):
                        output[i][17] = "Y"
                    elif (
                        ("博" in unit)
                        & ("碩" not in unit)
                        & (int(result.get_text()) >= 1)
                    ):
                        output[i][17] = "Y"
                    else:
                        output[i][17] = "N"
                else:
                    output[i][17] = "Y"
            elif result.get("data-th") == "可跨班：":
                match crossclass:
                    case "":
                        deli = 1
                        output[i][18] = result.get_text()
                    case "可跨班系":
                        if result.get_text() == "可跨班系":
                            deli = 1
                            output[i][18] = result.get_text()
                        else:
                            deli = 0
                            output[i][18] = result.get_text()
                    case "限本系":
                        if result.get_text() == "限本系":
                            deli = 1
                            output[i][18] = result.get_text()
                        else:
                            deli = 0
                            output[i][18] = result.get_text()
                    case "限本班":
                        if result.get_text() == "限本班":
                            deli = 1
                            output[i][18] = result.get_text()
                        else:
                            deli = 0
                            output[i][18] = result.get_text()
            elif result.get("data-th") == "備註：":
                output[i][19] = result.get_text().strip()
                if deli == 1:
                    i = i + 1
                else:
                    for k in range(0, 19):
                        output[i][k] = 0

    except TimeoutException:
        print("Loading took too much time!")

    # 首欄不為0者才存入output等待輸出
    output = [row for row in output if row[0] != 0]
    print("Total output:", len(output), "rows.")
    # print(output)

    return output


conn = sqlite3.connect("courses.db")
cursor = conn.cursor()


def load_allcrs_into_db():
    res = search_courses()
    search_res = gen_search_res(res)

    insert_command = """
    INSERT INTO COURSES VALUES (
        :課程代碼, :開課班別, :課程名稱, :課程名稱英文, :教學大綱, :教學大綱英文,
        :是否有教學大綱, :課程性質, :課程性質2, :全英語授課, :學分, :教師姓名,
        :上課大樓, :上課教室, :上限人數, :登記人數, :選上人數, :符合開課人數,
        :可跨班, :備註
    );
    """

    for item in search_res:
        cursor.execute(insert_command, item)

    conn.commit()
    conn.close()


def selectdb(
    year="112",
    semester="2",
    crsid="",
    crsclass="",
    crsnm="",
    is_all_eng="",
    is_dis_learn="",
    crossclass="",
    tchnm="",
    week="",
):

    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()
    query = """
        SELECT * FROM COURSES
        WHERE 1=1
    """

    if crsid:
        query += f" AND 課程代碼 = '{crsid}'"
    if crsclass:
        query += f" AND 開課班別 = '{crsclass}'"

    query += f" AND 課程名稱 like '%{crsnm}%'"
    query += f" AND 教師姓名 like '%{tchnm}%'"
    cursor.execute(query)
    res = cursor.fetchall()
    select_res = gen_search_res(res)
    conn.commit()
    conn.close()
    return select_res


def deleteTable(tablenm="COURSES"):
    query = f"DELETE FROM COURSES;"
    cursor.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # res = search_courses(is_all_eng="Y", week="2")
    # print(res)
    # load_allcrs_into_db()
    # deleteTable(tablenm="COURSES")
    selectdb()
