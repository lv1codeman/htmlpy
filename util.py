import re


def is_contain_chinese(word):
    """
    is_contain_chinese
    判断字符串是否包含中文字符
    :param word: 字符串
    :return: 布尔值，True表示包含中文，False表示不包含中文
    """
    pattern = re.compile(r"[\u4e00-\u9fa5]")
    match = pattern.search(word)
    return True if match else False


def gen_search_res_forgetcourse(res):
    keys = [
        "課程代碼",
        "開課班別",
        "課程名稱",
        "課程名稱英文",
        "教學大綱",
        "教學大綱英文",
        "是否有教學大綱",
        "課程性質",
        "課程性質2",
        "全英語授課",
        "學分",
        "教師姓名",
        "上課大樓",
        "上課教室",
        "上限人數",
        "登記人數",
        "選上人數",
        "符合開課人數",
        "可跨班",
        "備註",
    ]
    # res: 搜尋的結果，資料型態為2維list，計算它的數量即為這次搜尋的筆數
    # search_res_each: 將每筆資料存成dict
    # search_res: 把每筆re加入search_res這個list，做成一個dict array
    search_res = []
    for res_each in range(0, len(res)):
        search_res_each = {key: value for key, value in zip(keys, res[res_each])}
        search_res.append(search_res_each)
    return search_res


def gen_search_res(res):
    """
    keys的順序必須和DB內的欄位順序一樣
    """
    keys = [
        "查詢序號",
        "學年度",
        "學期",
        "序號",
        "課程代碼",
        "開課班別",
        "課程名稱",
        "教學大綱",
        "課程性質",
        "課程性質2",
        "全英語授課",
        "學分",
        "教師姓名",
        "上課大樓",
        "上課教室",
        "上限人數",
        "登記人數",
        "選上人數",
        "可跨班",
        "備註",
    ]
    # res: 搜尋的結果，資料型態為2維list，計算它的數量即為這次搜尋的筆數
    # search_res_each: 將每筆資料存成dict
    # search_res: 把每筆re加入search_res這個list，做成一個dict array
    search_res = []
    for res_each in range(0, len(res)):
        search_res_each = {key: value for key, value in zip(keys, res[res_each])}
        search_res.append(search_res_each)
    return search_res


def get_num_column_dict():
    """
    get_num_column_dict
    產生dict
    {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z', 27: 'AA', 28: 'AB', 29: 'AC', 30: 'AD', 31: 'AE', 32: 'AF', 33: 'AG', 34: 'AH', 35: 'AI', 36: 'AJ', 37: 'AK', 38: 'AL', 39: 'AM', 40: 'AN', 41: 'AO', 42: 'AP', 43: 'AQ', 44: 'AR', 45: 'AS', 46: 'AT', 47: 'AU', 48: 'AV', 49: 'AW', 50: 'AX', 51: 'AY', 52: 'AZ'}
    """
    num_str_dict = {}
    A_Z = [chr(a) for a in range(ord("A"), ord("Z") + 1)]
    AA_AZ = ["A" + chr(a) for a in range(ord("A"), ord("Z") + 1)]
    A_AZ = A_Z + AA_AZ
    for i in A_AZ:
        num_str_dict[A_AZ.index(i) + 1] = i
    return num_str_dict


def getSyllabusColumns(result, hasCHT, hasENG):
    output = [""] * 3
    if hasCHT == False and hasENG == False:
        output[0] = "無檔案"
        output[1] = "No file"
        output[2] = "Y"
    else:
        output[2] = "N"
        if hasCHT == True and hasENG == False:
            output[0] = result.find("a").text.strip()
            output[1] = "No file"
        elif hasCHT == False and hasENG == True:
            output[0] = "無檔案"
            output[1] = result.find("a").text.strip()
        else:
            output[0] = result.find("a").text.strip()
            output[1] = result.find("a").next_sibling.next_sibling.next_sibling.strip()
    return output


# 獨立執行util.py時才會執行，若util.py作為模組被呼叫使用則不執行
if __name__ == "__main__":
    print(is_contain_chinese.__doc__)
    print(get_num_column_dict.__doc__)
