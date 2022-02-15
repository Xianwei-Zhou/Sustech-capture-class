import re
from getpass import getpass
from requests import session
import time
import threading

t = time.localtime(time.time())
xuenian = (str(t.tm_year) + '-' + str(t.tm_year + 1)) if t.tm_mon > 6 or (t.tm_mon == 6 and t.tm_mday > 15) else (
        str(t.tm_year - 1) + '-' + str(t.tm_year))
xueqi = 1 if t.tm_mon > 6 or (t.tm_mon == 6 and t.tm_mday > 15) else 2 if t.tm_mon < 5 else 3
data = {
    'p_pylx': 1,  # 培养类型？ 不懂
    'p_xn': xuenian,
    'p_xq': xueqi,
    'p_xnxq': xuenian + str(xueqi),
    'p_xktjz': 'rwtjzyx'  # 任务提交至已选
}
classType = ['bxxk', 'xxxk', 'kzyxk', 'zynknjxk']
session = session()
student_id = '11911224'
password = ''
classList = []


def queryClass(className):
    data1 = {
        "p_xn": xuenian,
        "p_xq": xueqi,
        "p_xnxq": data['p_xnxq'],
        "p_chaxunpylx": 3,
        "mxpylx": 3,
        "p_sfhltsxx": 0,
        "pageNum": 1,
        "pageSize": 2000}
    req = session.post('https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList', data=data1)
    pattern = re.compile('{[^{}]+' + className + '[^{}]+}')
    text = pattern.search(req.text, re.M).group(0)
    return re.search('"id":"([a-zA-Z0-9]+)"', text).group(0)[6:-1]


def config():
    while True:
        cls = input('请输入你要抢的课程（如果不需要继续添加则输入quit）： ').strip()
        if cls == 'quit':
            break
        xkType = ''
        while xkType != '1' and xkType != '2' and xkType != '3' and xkType != '4':
            xkType = input('请输入选课类型（1：通识必修选课 ，2：通识选修选课 ，3：培养方案内课程 ，4：非培养方案内课程）： ')

        d = data.copy()
        try:
            d['p_id'] = queryClass(cls)
        except Exception:
            cls = input('课程名错误，请重新输入： ').strip()
            d['p_id'] = queryClass(cls)
        d['p_xkfsdm'] = classType[int(xkType) - 1]
        global classList
        classList.append(d)


def logIn():
    global student_id, password
    student_id = input('输入你的学号: ').strip()
    password = getpass('输入你的cas密码（输入完成后按回车即可）: ').strip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

    data = {
        'username': student_id,
        'password': password,
        'execution': '',
        '_eventId': 'submit'
    }
    try:
        response = session.get('https://tis.sustech.edu.cn/cas', headers=headers)

        data['execution'] = re.findall('execution" value="(.+?)"', response.text)[0]
        response = session.post('https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas',
                                data=data,
                                headers=headers)
        if '认证信息无效' in response.text:
            return 0
        print("cas验证通过")
    except Exception as e:
        print("something wrong in login")
        print(e)
    return 1


i = 0  # 抢课次数


def capture():
    while True:
        global i, r
        print('这是第{}次抢课'.format(i))
        i += 1
        for classData in classList:
            try:
                r = session.post('https://tis.sustech.edu.cn/Xsxk/addGouwuche', data=classData)
            except Exception as e:
                print(e)
            print(r.text)


def main():
    print('如果程序出现bug建议重启此脚本')
    while logIn() == 0:
        print("cas验证失败，请重新验证")
        time.sleep(0.1)
    config()
    for k in range(15):
        threading.Thread(target=capture).start()
    session.close()


if __name__ == '__main__':
    main()
