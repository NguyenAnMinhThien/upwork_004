from selenium import webdriver

#%%
import datetime
import subprocess
import pandas
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions
import undetected_chromedriver as uc


import pygsheets
def import_sheet(data):
    #authorization
    gc = pygsheets.authorize(client_secret='client_secret.json')
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tmS19xOtKI9Z0aHY0cuk3_Tl6fOe55U4Ifwu0yICEME/edit?gid=0#gid=0')
    #select the first sheet
    wks = sh[0]
    for row in data:
        try:
            wks.append_table(values=row)
        except Exception as e:
            pass

#%%
url_espn = 'https://www.espn.com/mlb/schedule/_/date/'

current = datetime.datetime.now()
current_date = current.strftime("%Y") + current.strftime("%m") + current.strftime("%d")
tomorrow_date =  current.strftime("%Y") + current.strftime("%m") +str(int(current.strftime("%d"))+1)
current_espn = url_espn + current_date
tomorrow_espn= url_espn + tomorrow_date
options = ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options)
# driver = uc.Chrome()
driver.get(current_espn)

#%%
tomorrow_schedule = driver.find_element(By.CLASS_NAME,"ResponsiveTable")
tomorrow_schedules = driver.find_elements(By.CLASS_NAME,"ResponsiveTable")
tomorrow_schedule.text
# #%%
# # this script will run at the end of the day, after the result of this day has updated, there is no LIVE table row
# # not finished: find the table contain schedule for tommorow
# for inx in range(tomorrow_schedules.__len__()):
#     print(f"\nnew {inx}\n")
#     # print(tomorrow_schedules[inx].text)
#     print(tomorrow_schedules[inx].find_element(By.XPATH,'//div[contain(@class,"Table__Title")]'))
#%%
tomorrow_schedules[2].text
#%%
table = tomorrow_schedules[2].find_element(By.TAG_NAME,"table").find_element(By.TAG_NAME,"tbody")
matchups = table.find_elements(By.TAG_NAME,"tr")
espn_data=list()
for tr in matchups:
    row_data = tr.text.split("\n")
    match = [''] * 20
    match[0] = current.strftime("%m") + "/" + str(int(current.strftime("%d"))+1) + "/" + current.strftime("%Y")
    match[2] = row_data[0]
    match[8] = row_data[2]
    match[1] = row_data[3]
    espn_data.append(match)
import_sheet(espn_data)

#%%
df = pandas.DataFrame(columns=[
    'Date','Time','Team 1','Team 1 Rank','Team 1 Win Prob','Team 1 Run Line','Team 1 Run Line Odds','Team 1 Moneyline Odds','Team 2','Team 2 Rank','Team 2 Win Prob','Team 2 Run Line','Team 2 Run Line Odds','Team 2 Moneyline Odds','Total Over','Total Over Odds','Total Under','Total Under Odds','Team 1 Score','Team 2 Score'
])


#%%
