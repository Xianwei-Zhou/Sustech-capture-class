import re
from getpass import getpass
from requests import session

data = {
    'p_pylx': 1,
    'p_xn': '2021-2022',
    'p_xq': 1,
    'p_xnxq': '2021-20221',
    'p_xktjz': 'rwtjzyx'
}
classType = ['bxxk', 'xxxk', 'kzyxk', 'zynknjxk']
session = session()
student_id = '11910000'
password = ''
classList = []


def queryClass(className):
    data1 = {
        "p_xn": data['p_xn'],
        "p_xq": data['p_xq'],
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
    response = session.get('https://tis.sustech.edu.cn/cas', headers=headers)

    data['execution'] = re.findall('execution" value="(.+?)"', response.text)[0]
    response = session.post('https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas',
                            data=data,
                            headers=headers)
    if '认证信息无效' in response.text:
        return 0
    return 1


def capture():
    i = 0
    while True:
        for classData in classList:
            print('这是第{}次抢课'.format(i))
            i += 1
            r = session.post('https://tis.sustech.edu.cn/Xsxk/addGouwuche', data=classData)
            print(r.text)


def main():
    print('如果程序出现bug建议重启此脚本')
    while logIn() == 0:
        pass
    config()
    capture()
    session.close()


if __name__ == '__main__':
    main()
