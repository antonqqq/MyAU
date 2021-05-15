import requests
import time
from bs4 import BeautifulSoup

def Login(username, password):
    s = requests.session()

    def gen_data1():
        unixtime = '_' + str(int(time.time()*1000))
        data = {
            'user_id2': 'secured',
            'password2': 'secret',
            unixtime : 'user',
            'user_id': unixtime,
            'body_color': '#9FBFD0',
            'welcome_url': '../PARENTS_STUDENTS/main_files/login_success.htm',
            'page_url': '../PARENTS_STUDENTS/main_files/parents_students_bottom_content.htm',
            'login_type': 'parent_student',
            'user_id3': 'secured',
            'password3': 'secret'
        }
        return data

    # print(gen_data1())

    r = s.post('https://sblive.auf.edu.ph/schoolautomate/PARENTS_STUDENTS/main_files/login_new.jsp', data= gen_data1())
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    ol_lx = soup.find('input', {'name': 'ol_lx'})['value']

    def gen_data2():
        unixtime = '_' + str(int(time.time()*1000))
        data = {
        'ol_lx': ol_lx,
        'user_id2': 'secured',
        'password2': 'secret',
        unixtime: username,
        'user_id': unixtime,
        unixtime+'0': password,
        'password': unixtime+'0',
        'is_secured': '1',
        'body_color': '#9FBFD0',
        'welcome_url': '../PARENTS_STUDENTS/main_files/login_success.htm',
        'page_url': '../PARENTS_STUDENTS/main_files/parents_students_bottom_content.htm',
        'login_type': 'parent_student',
        'user_id3': 'secured',
        'password3': 'secret'
        }
        return data

    login = s.post('https://sblive.auf.edu.ph/schoolautomate/commfile/login.jsp', data = gen_data2())
    request_payment = s.get('https://sblive.auf.edu.ph/schoolautomate/PARENTS_STUDENTS/accounts/pmt_schedule.jsp')
    # r3 = s.get('https://sblive.auf.edu.ph/schoolautomate/PARENTS_STUDENTS/accounts/pmt_schedule.jsp')

    html_payment = request_payment.content
    soup_payment = BeautifulSoup(html_payment, 'html.parser')
    payment_keys = ['pr', 'pc', 'mr', 'mc', 'fr', 'fc']
    payment_arr = []

    for row in soup_payment.findAll('td', {'align': 'right'})[1:]:
        payment_arr.append("{:.2f}".format(float(row.text.replace(',', ''))))

    payment = dict(zip(payment_keys, payment_arr))

    grade_data = {
    'grade_name': 'Midterm',
    'semester_name': '2nd Semester',
    'grade_for': 'Midterm',
    'semester': '2',
    'sy_from': '2020',
    'sy_to': '2021'
    }

    request_grade = s.post('https://sblive.auf.edu.ph/schoolautomate/PARENTS_STUDENTS/acad_performance/grade_release.jsp', data = grade_data)
    html_grade = request_grade.content
    soup_grade = BeautifulSoup(html_grade, 'html.parser')

    grade_data = []
    table = soup_grade.find('table', {'class':'thinborder'})

    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        grade_data.append([ele for ele in cols if ele])

    return {
        'payment': payment,
        'grades': grade_data
    }

# print(Login('aufantonq', 'antonquiambao'))