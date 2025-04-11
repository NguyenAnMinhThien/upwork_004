import datetime
import subprocess
import pandas
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions
import undetected_chromedriver as uc

# upwork-scraper.dwg
# The link to scrape
# The number of repeated time if use
# time.sleep(3)
# The list to store previous value and current value.
# uusage: python main.py http
def refresh_page():
    global driver
    driver.refresh()
    # driver.get(url)
    try:
        time.sleep(60)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "job-tile-title")))
    except Exception as e:
        time.sleep(60)
        pass

    Header = driver.find_element(By.CLASS_NAME, "job-tile-title")
    Content = driver.find_element(By.CLASS_NAME, "text-body-sm")
    Token = driver.find_element(By.CLASS_NAME, "air3-token-container")
    sub_url = Header.find_element(By.TAG_NAME, 'a').get_attribute('href')

    # Token = driver.find_elements(By.CLASS_NAME, "air3-token-container")
    # Token_list = [mytoken.text for mytoken in Token]
    # token_text = ""
    # for data in Token_list:
    #     token_text = token_text + data
    Token_text = ""
    # Token_text = str.join()
    for hehe in Token.text.split("\n"):
        Token_text = Token_text + hehe
    # mydata = list()
    # for i in range(Header.__len__()):
    # mydata.append([Header[i],Content[i],Token[i]])
    # Only catch the first element that is newest.
    mydata = [Header.text,Content.text,Token_text, sub_url, datetime.datetime.now().__str__()]
    return mydata

def check_key_word(text,upwork_key):
    import re
    with open(upwork_key,"r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line != ""]
        true_list = [re.search(line, text) != None for line in lines ]
        return any(true_list)



def checking_request_vs_proposal(upwork_key):
    global driver
    global cache
    global count
    global dataframe
    # just call above at once, the call the refresh , put these function in a sub_def
    # when run this script automation, it will raise the web driver everytime, how I can work with the current task ?
    #         if content exit or not exit, print the notification
    # os.walk , print the current extracted data into a local file, or store in an list of list, to compare with the later, it there is any not  _> run at remote server, so, no use , where we can find Chromedriver at remote ?
    #     eachtime refresh page, get the newest element from, just capture the first element of that .
    mydata = refresh_page()
    # print(mydata)
    for sub_content in mydata:
        # Match our proposal
        if check_key_word(str(sub_content).lower(),upwork_key):
            if cache == []:
                # print(f"{sub_content}")
                # play_sound.play_sound("note.mp3")
                # info = input("Do you want to continue ?")
                # if info == "":
                #     cache.append(mydata[0])
                #     continue
                # else:
                #     break
                # cache is used to store all the header name, not the sublist like mydata, cache will not be a single variable because it is used to store for other URLs. cache[0] is for the url[0], cache [1] is for url[1] ,..
                print(f' \n Attention Attention: \n {datetime.datetime.now()}')
                print(mydata[0] + "\n" + mydata[1])
                cache.append(mydata[0])
                # break to make sure there is no more data is append in the same request
                break
            elif cache[0] != mydata[0]:
                # if sys.argv[1] == "pc":
                #     play_sound.play_sound("note.mp3")
                # else:
                # By default, we run with phone_calls.py

                # Alert when the proposal require VietNam people

                driver.switch_to.new_window('tab')
                driver.get(mydata[3])
                sections = driver.find_elements(By.CLASS_NAME, "air3-card-sections")
                for section in sections:
                    if "VIETNAM" in section.text.upper():
                        print(f"URGENT: {mydata[3]}")
                        mydata[4] = "Urgent"
                        subprocess.run("python phone_calls.py", shell=True)
                #  Return back again the old window
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                pandas.DataFrame(data=mydata).to_csv(path_or_buf="output.csv",mode='a', index=False)
                play_sound.play_sound("note.mp3")
                # subprocess.run("python phone_calls.py", shell = True)

                #     update the value of cache[0] - the first index point to first match of Request list. Avoid the next time this condition still match
                print(f' \n Attention Attention: \n {datetime.datetime.now()}')
                print(mydata[0] + "\n" + mydata[1])
                cache[0] = mydata[0]
                break
            else:
                count = count + 1



if __name__ == '__main__':
    # the thread running the playsound get the whole process make the time.sleep() can not reach -> work around: use a small mp3 file.
    # 'https://www.espn.com/mlb/schedule/_/date/20250412'
    url_espn = 'https://www.espn.com/mlb/schedule/_/date/'

    current = datetime.datetime.now()
    current_date = current.strftime("%Y") + current.strftime("%m") + current.strftime("%d")
    url_espn = url_espn + current_date
    # options = ChromeOptions()
    # options.add_argument('--incognito')
    # driver = uc.Chrome(options)
    driver = uc.Chrome()
    driver.get(url_espn)
    try:
        # Why the schedule package can not work ?
        # schedule.every(60).seconds.do(checking_request_vs_proposal,url)
        cache = list()
        count = 0
        while (1):
            time.sleep(10)
            checking_request_vs_proposal(upwork_key)
            # Have sleep inside driver.refresh ready
            # time.sleep(60)
    except KeyboardInterrupt:
        driver.quit()
        pass

