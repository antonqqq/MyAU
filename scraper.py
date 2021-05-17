import requests
import time
from bs4 import BeautifulSoup

def Login(username, password, period='Midterm', sem='2', sy='2020-2021'):
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

    sem_name = ''
    if sem == 1: sem_name = '1st Semester'
    if sem == 2: sem_name = '2nd Semester'
    if sem == 3: sem_name = '3rd Semester'
    sy_start = sy[:4]
    sy_end = sy[5:]
    grade_data = {
    'grade_name': period,
    'semester_name': sem_name,
    'grade_for': period,
    'semester': sem,
    'sy_from': sy_start,
    'sy_to': sy_end
    }

    request_grade = s.post('https://sblive.auf.edu.ph/schoolautomate/PARENTS_STUDENTS/acad_performance/grade_release.jsp', data = grade_data)
    html_grade = request_grade.content
    soup_grade = BeautifulSoup(html_grade, 'html.parser')

    # print(html_grade)

    grade_data = []
    table = soup_grade.find('table', {'class':'thinborder'})

    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        grade_data.append([ele for ele in cols if ele])

    for i in grade_data:
        if 'Grade not encoded' in i:
            i.insert(2, 'NA')
            i.append('NA')


    request_sidebar = s.get('https://sblive.auf.edu.ph/schoolautomate/PARENTS_STUDENTS/main_files/parents_students_main_links.jsp')
    html_sidebar = request_sidebar.content
    soup_sidebar = BeautifulSoup(html_sidebar, 'html.parser')

    dashboard_link = soup_sidebar.find('a', {'target': 'rightFrame'})

    request_dashboard = s.get(dashboard_link['href'])
    html_dashboard = request_dashboard.content
    soup_dashboard = BeautifulSoup(html_dashboard, 'html.parser')

    clearance = soup_dashboard.find('div', {'class': 'clearance'})
        
    return {
        'payment': payment,
        'grades': grade_data,
        'clearance': clearance
    }

# print(Login('aufantonq', 'antonquiambao'))
