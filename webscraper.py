from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import datetime
import calendar
import numpy as np

'''chromedriver options'''
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

url = 'https://hdc-p-ols.spectrumng.net/Samena/Login.aspx?ReturnUrl=%2fSamena%2f'

'''create webdriver object'''
driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe', options = options)
driver.get(url)
# print(driver.page_source)

'''login'''
username = driver.find_element_by_id('ctl00_pageContentHolder_loginControl_UserName').send_keys('USERNAME')
password = driver.find_element_by_id('ctl00_pageContentHolder_loginControl_Password').send_keys('PASSWORD')
submit = driver.find_element_by_id('ctl00_pageContentHolder_loginControl_Login').click()

time.sleep(10)
# driver.save_screenshot('screenshot.png')

'''navigate to reservation page'''

reserve = driver.find_element_by_id('menu_SCH').click()
time.sleep(2)
# swim = driver.find_element_by_xpath("//*[@title='Swim']").click()
swim = driver.find_element_by_xpath("/html/body/form/div[3]/table[1]/tbody/tr/td/div[2]/div/div[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/div[3]/div/div[1]/ul/li[3]/div").click()
time.sleep(2)



'''prompt user for type of reservation'''

reserve_type = input("Which type of reservation would you like to make? Single indoor, single outdoor, shared indoor, or shared outdoor? ")
reserve_type = str(reserve_type)
run = True
while run:
    if (reserve_type.lower() == 'single indoor'):
        run = False
        try:
            si_in = driver.find_element_by_xpath("/html/body/form/div[3]/table[1]/tbody/tr/td/div[2]/div/div[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/div[3]/div/div[1]/ul/li[6]/div").click()
            time.sleep(2)
        except NoSuchElementException:
            print("Page unavailable")

    elif (reserve_type.lower() == 'single outdoor'):
        run = False
        try:
            si_out = driver.find_element_by_xpath("/html/body/form/div[3]/table[1]/tbody/tr/td/div[2]/div/div[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/div[3]/div/div[1]/ul/li[2]/div").click()
            time.sleep(2)
        except NoSuchElementException:
            print("Page unavailable")
    elif (reserve_type.lower() == 'shared indoor'):
        run = False
        try:
            sh_in = driver. find_element_by_xpath("/html/body/form/div[3]/table[1]/tbody/tr/td/div[2]/div/div[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/div[3]/div/div[1]/ul/li[5]/div").click()
            time.sleep(2)
        except NoSuchElementException:
            print("Page unavailable")
    elif (reserve_type.lower() == 'shared outdoor'):
        run = False
        try:
            sh_out = driver.find_element_by_xpath("/html/body/form/div[3]/table[1]/tbody/tr/td/div[2]/div/div[1]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/div[3]/div/div[1]/ul/li[1]/div").click()
            time.sleep(2)
        except NoSuchElementException:
            print("Page unavailable")
    else:
        reserve_type = print("Pleae enter a valid reservation type. Try again. ")



'''click calendar'''
driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[4]/div/div/div[2]/table/tbody/tr[4]/td[3]/div/div/table/tbody/tr/td/div/img").click()



'''prompt user for month'''

run2 = True
while run2:
    month = input("What month? Enter a number from 1-12. ")
    if month.isdigit() and int(month) < 13 and int(month) > 0:
        run2 = False
        datetime_object = datetime.datetime.strptime(month, "%m")
        nmonth = datetime_object.strftime("%b")
        try:
            # month_num = driver.find_element_by_xpath("/html/body/div[3]/div/div/select[1]/option[" + month + "]").click()
            month_num = Select(driver.find_element_by_xpath("/html/body/div[3]/div/div/select[1]"))
            month_num.select_by_visible_text(nmonth)
            time.sleep(2)
        except NoSuchElementException:
            print("Page unavailable")
    else:
        print("Try again. ")



'''prompt user for year'''

run3 = True
while run3:
    year = input("What year? Enter a number from 1900-2025. ")
    if year.isdigit() and int(year) < 2026 and int(year) > 1899:
        run3 = False
        try:
            # driver.find_element_by_xpath("/html/body/div[3]/div/div/select[2]/option[" + year + "]").click()
            driver.find_element_by_xpath("/html/body/div[3]/div/div/select[2]").click()
            year_num = Select(driver.find_element_by_xpath("/html/body/div[3]/div/div/select[2]"))
            year_num.select_by_visible_text(year)
            time.sleep(2)
        except NoSuchElementException:
            print("Page unavailable")
    else:
        print("Try again. ")


''' prompt user for day '''

run4 = True
while run4:
    date = input("What date? Enter a number from 1-31. ")
    if date.isdigit():
        run4 = False
        '''figuring out which day of the week'''
        day = datetime.date(int(year), int(month), int(date)).weekday()
        day += 2
        '''figuring out which week of the month'''
        formatted_date = datetime.datetime(year=int(year), month=int(month), day=int(date)).date()
        week = formatted_date.isocalendar()[1] - formatted_date.replace(day=1).isocalendar()[1] + 1
        # print(week)

        try:
            driver.find_element_by_xpath("/html/body/div[3]/table/tbody/tr[" + str(week) + "]/td[" + str(day) + "]/a").click()
            time.sleep(2)
        except NoSuchElementException:
            print("Page unavailable")
    else:
        print("Try again. ")


'''click continue'''
driver.find_element_by_id("btnContinue").click()
time.sleep(10)

'''beautifulsoup'''
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

'''I made three arrays. First: Array of time tokens (based on whitespace areas). 
Second: Time slots (ie. 8am, 9am, 10am... 8pm)
Third: Time slot availability (ie. 0, 1, 1, 0, 0, 1) where 0 = unavailable time slot and 1 = available time slot. '''

'''next, I made a 2D array that matches Array1 and Array2 values where the corresponding spot in Array2 is 1. '''


'''Array 1: Finding the whitespace areas on the reservation page. The attribute 'value' is assigned a number from 360 to 1140,
in increments of 60. These values are impended in order to an array.  '''

slots = soup.find_all('li')

arr = []

for s in slots:
    try:
        a = s.attrs['value']
        arr.append([a])
    except:
        pass

time.sleep(1)


'''Array 2: Finding the reservation timeslots and putting them into an array'''

timeslots = soup.find_all('li')
times = []
actual_times = []

for t in timeslots:
    try:
        a = t.text
        if ("AM" in a or "PM" in a):
            times.append([a])
    except:
        pass

'''finding the number of lanes that are available for reservation'''

n = 0
lanes = soup.find_all('span')

for l in lanes:
    try:
        a = l.attrs['class']
        if str(a) == "['schempSpan']":
            n += 1
            # print(l.text)
    except:
        pass

'''appending the "times" list (of timeslots 6am-8pm) n number of times 
to the actual_times array, where n is the number of lanes available'''

for i in range(n):
    actual_times.extend(times)

time.sleep(1)

'''Array 3: Finding all of the grey (booked) areas on the reservation page. Different dimensions for 
the height indicate how many time slots each grey box takes up. '''

grey_area = soup.find_all('div')

arr2 = []

''' y = 61x - 46 where y is the height of the grey box and x is the number of timeslots it takes up.
This is because a single grey box can span over multiple timeslots if they are all fully booked. '''

'''Only heights of 15 indicate that the spot is still empty (open for reservations), because empty slots have
a small grey box of height 15 below them. '''

for g in grey_area:
    try:
        a = g.attrs['class']
        # print(a)
        if a == ['ebgreayarea']:
            b = g.attrs['style']
            if "height: 15" in str(b):
                arr2.append([1])
            elif "height: 76" in str(b):
                for i in range(0, 2):
                    arr2.append([0])
            elif "height: 137" in str(b):
                for i in range(0, 3):
                    arr2.append([0])
            elif "height: 198" in str(b):
                for i in range(0, 4):
                    arr2.append([0])
            elif "height: 259" in str(b):
                for i in range(0, 5):
                    arr2.append([0])
            elif "height: 320" in str(b):
                for i in range(0, 6):
                    arr2.append([0])
            elif "height: 381" in str(b):
                for i in range(0, 7):
                    arr2.append([0])
            elif "height: 442" in str(b):
                for i in range(0, 8):
                    arr2.append([0])
            elif "height: 503" in str(b):
                for i in range(0, 9):
                    arr2.append([0])
            elif "height: 564" in str(b):
                for i in range(0, 10):
                    arr2.append([0])
            elif "height: 625" in str(b):
                for i in range(0, 11):
                    arr2.append([0])
            elif "height: 686" in str(b):
                for i in range(0, 12):
                    arr2.append([0])
            elif "height: 747" in str(b):
                for i in range(0, 13):
                    arr2.append([0])
            elif "height: 808" in str(b):
                for i in range(0, 14):
                    arr2.append([0])
            elif "height: 869" in str(b):
                for i in range(0, 15):
                    arr2.append([0])
    except:
        pass


time.sleep(1)


'''make a 2D array of [time key, time slot] (ie. [360, 8:00 AM])'''

available_times = []

for key in range(len(arr2)):
    elem = arr2[key]
    if "1" in str(elem):
        available_times.append([arr[key], actual_times[key]])

'''prints out available times'''

print("The following times are available: ")
for i in range(len(available_times)):
    print(available_times[i][1])

'''asks for user input to make a reservation'''

print()
reserve_time = input("Please indicate which time you would like to make a reservation (ie. 11:00 AM)")


'''function that matches the user input to a time in the available_times array'''

def time_chosen(available_times, reserve_time):
    for i in range(len(available_times)):
        if "['" + reserve_time + "']" == str(available_times[i][1]):
            return str(available_times[i][0])


'''transforms the time token into int without the [' and '] surrounding it '''

time_token = time_chosen(available_times, reserve_time)
time_token = time_token[2 : len(time_token) - 2]
time_token = int(time_token)
# print(time_token)

'''converting time token to an xpath (need to fix b/c I got the xpath wrong) '''

xpathnum = (time_token - 300) / 60
xpathnum = int(xpathnum)
xpathnum = str(xpathnum)
driver.save_screenshot('screenshot.png')

