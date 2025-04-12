import pandas
import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(client_secret='client_secret.json')

# How to use dataframe in adding data
# # Create empty dataframe
# df = pd.DataFrame(columns=[['Team1'],['Team2'],['Time']])
#
# # Create a column
# data = ['Team1 name','Team2 name', '12AM']
# pandas.concat(df,data,ignore_index=True)
#
#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tmS19xOtKI9Z0aHY0cuk3_Tl6fOe55U4Ifwu0yICEME/edit?gid=0#gid=0')

#select the first sheet
wks = sh[0]

#update the first sheet with df, starting at cell B2.
try:
    wks.append_table(values=[["a","b"],["c","d"]])
except Exception as e:
    pass
# wks.set_dataframe(df,(2,1))


# --
# --trash
# tomorrow_schedules = driver.find_elements(By.CLASS_NAME,"ResponsiveTable")
# # tomorrow_schedule.text
# # tomorrow_schedules[2].text
# # if tomorrow_schedules[1] contain the corrected tommorw
# table = tomorrow_schedules[1].find_element(By.TAG_NAME,"table").find_element(By.TAG_NAME,"tbody")
# matchups = table.find_elements(By.TAG_NAME,"tr")
# espn_data=list()
# for tr in matchups:
#     row_data = tr.text.split("\n")
#     match = [''] * 20
#     match[0] = current.strftime("%m") + "/" + str(int(current.strftime("%d"))+1) + "/" + current.strftime("%Y")
#     match[2] = row_data[0]
#     match[8] = row_data[2]
#     match[1] = row_data[3]
#     espn_data.append(match)
# print(espn_data)

