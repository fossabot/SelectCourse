import requests
from bs4 import BeautifulSoup
import json
import time

with open('config.json', encoding='utf-8') as f:
    config = json.load(f)
coursenumber = config['coursenumber']
teachernumber = config['teachernumber']
cookie = config['cookie']

queryurl = 'http://xk.autoisp.shu.edu.cn/StudentQuery/QueryCourseList'
selecturl = 'http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/CourseSelectionSave'

formdata = {'PageIndex': '1',
            'PageSize': '30',
            'FunctionString': 'Query',
            'CID': coursenumber,
            'CourseName': '',
            'IsNotFull': 'false',
            'CourseType': 'B',
            'TeachNo': teachernumber,
            'TeachName': '',
            'Enrolls': '',
            'Capacity1': '',
            'Capacity2': '',
            'CampusId': '',
            'CollegeId': '',
            'Credit': '',
            'TimeText': ''
            }

selectdata = {'cids': coursenumber,
              'tnos': '1001'}

header = {'Host': 'xk.autoisp.shu.edu.cn',
          'Proxy-Connection': 'keep-alive',
          'Content-Length': '207',
          'Accept': 'text/html, */*; q=0.01',
          'X-Requested-With': 'XMLHttpRequest',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Origin': 'http://xk.autoisp.shu.edu.cn',
          'Referer': 'http://xk.autoisp.shu.edu.cn/StudentQuery/QueryCourse',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
          'Cookie': cookie
          }


def queryclass():
    r = requests.post(queryurl, data=formdata, headers=header)
    # print(r.text)
    if r.status_code != requests.codes.ok:
        print('4XX or 5XX Error,check your Internet connection or you cookie')
    soup = BeautifulSoup(r.text, 'lxml')
    for each_course in soup.find_all('tr', attrs={'name': 'rowclass'}):
        # all_tr_tag = each_course.find_all('tr')
        all_td_tag = each_course.find_all('td', attrs={'style': 'text-align: center;'})
        plan = all_td_tag[1].text
        current = all_td_tag[2].text
        print("当前：" + current + "人，计划：" + plan + "人")
        if int(plan) > int(current):
            print("有空余")
            return True
        else:
            print("无空余")
            return False


def selectclass():
    r = requests.post(selecturl, data=selectdata, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    if r.text.find('选课成功') > -1:
        print("选课成功！")
        return True
    if r.text.find('教学班人数已满！') > -1:
        print("选课失败！原因是人数已满！")
        return False
    if r.text.find('已选此课程') > -1:
        print("选课失败！已选此课程！请登陆选课系统查看选课！")
        print("为防止账号被风控，将停止自动选课。")
        return True
    if r.text.find('选课失败') > -1:
        print("选课失败！其他未知原因错误，请自行进入选课系统查看！")
        return False


if __name__ == '__main__':
    while True:
        flag = queryclass()
        if flag == True:
            selectflag = selectclass()
            if selectflag == True:
                break
            if selectflag == False:
                print("10秒后继续查询")
                print("====================\n")
                time.sleep(10)
                continue
        print("10秒后继续查询")
        print("====================\n")
        time.sleep(10)