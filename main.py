import datetime
import time
import re
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import random
from undetected_chromedriver import ChromeOptions
import proxyscrape
def rotate_proxy():
    proxy = proxyscrape.proxy
    return random.choice(proxy)
def scrape_espn(url):
    global driver
    print(datetime.datetime.now(),"\n")
    driver.get(url)
    time.sleep(2)
    tomorrow_schedules = driver.find_elements(By.CLASS_NAME,"ResponsiveTable")
    # heree
    table = tomorrow_schedules[2].find_element(By.TAG_NAME,"table").find_element(By.TAG_NAME,"tbody")
    matchups = table.find_elements(By.TAG_NAME,"tr")
    espn_final = list()
    espn_finals = list()
    for idx in range(matchups.__len__()):
        print(matchups.__len__())
        # time = .find_element(By.CLASS_NAME,"date__col").text)
        try:
            link_game_0 = matchups[idx].find_element(By.CLASS_NAME,"date__col")
            link_game = link_game_0.find_element(By.TAG_NAME,"a").get_attribute("href")
            print(link_game,"\n")
            driver.switch_to.new_window("new_tab")
            driver.get(link_game)
            time.sleep(1)
            print("Getting content in section")
            espn_news = driver.find_element(By.CLASS_NAME,"PageLayout__Main").find_element(By.XPATH, '//section[@data-testid="prism-LayoutCard"]')
            # if espn_news[1].text.__contains__("Game Odds"):
            #     espn_new_element = espn_news[1]
            # elif espn_news[0].text.__contains__("Game Odds"):
            #     espn_new_element = espn_news[0]
            # else:
            #     raise Exception
            espn_new = espn_news.text.split("\n")
            series = [2,7,8,16,17]
            for serie in series:
                espn_final.append(re.sub('\(.*\)','',espn_new[serie]))
            matchup_predictor = driver.find_elements(By.CLASS_NAME, "matchupPredictor__teamValue")
            print("Finished getting predictor")
            espn_final.append(matchup_predictor[0].text)
            espn_final.append(matchup_predictor[1].text)
            espn_finals.append(espn_final.copy())
            espn_final.clear()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            matchups = table.find_elements(By.TAG_NAME,"tr")
        except Exception as e:
            print(f"Exception at: {link_game}\n")
            pass
    #     1,2,5 is left; 3,4,6 is right
    return (espn_finals)
def scrape_sport_book():
    global driver
    print(datetime.datetime.now())
    driver.switch_to.new_window("newtab")
    driver.get('https://sportsbook.draftkings.com/leagues/baseball/mlb')
    time.sleep(2)
    odd_tables = driver.find_elements(By.CLASS_NAME,"sportsbook-table")
    if odd_tables.__len__() == 2:
        print("Script can not run now, output flag to a file outside")
        odd_table = odd_tables[1]
    else:
        odd_table = odd_tables[0]
    odd_rows = odd_table.find_elements(By.TAG_NAME,"tr")
    # driver.find_element(By.XPATH,'//table[contain(@class="sportsbook-table")]')
    draftking_lists = list()
    draftking_list = list()

    for odd_row in odd_rows:
        if (odd_row.text.__contains__("TOMORROW") == False):
            team_name = odd_row.find_element(By.TAG_NAME,"th").text.split("\n")[0]
            if team_name.__contains__("AM") or team_name.__contains__("PM"):
                team_name = odd_row.find_element(By.TAG_NAME,"th").text.split("\n")[1]
            draftking_list.append(team_name)
            # print(team_name)
            run_total_money = odd_row.find_elements(By.TAG_NAME,"td")
            draftking_list.append(run_total_money[0].text)
            draftking_list.append(run_total_money[1].text)
            draftking_list.append(run_total_money[2].text)
            draftking_lists.append(draftking_list.copy())
            draftking_list.clear()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return (draftking_lists)

def scrape_rank():
    global driver
    print(datetime.datetime.now())
    driver.switch_to.new_window("newtab")
    driver.get('https://www.mlb.com/standings/mlb')
    time.sleep(2)
    rank_data = (driver.find_element(By.ID, "standings-app-root").text.split("\n"))
    toggle = 0
    rank_list = list()
    for rank_maybe in rank_data:
        if rank_maybe.__contains__('W L PCT GB'):
            print("start from here")
            toggle = 1
            continue
        if toggle == 1 and (re.search("\d", rank_maybe)) == None and rank_maybe.strip() != '':
            rank_list.append(rank_maybe)
    return rank_list

if __name__ == "__main__":
    options = ChromeOptions()
    proxy = rotate_proxy()
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument('--headless=new')
    driver = uc.Chrome(options)

    url_espn = 'https://www.espn.com/mlb/schedule/_/date/'
    current = datetime.datetime.now()
    current_date = current.strftime("%Y") + current.strftime("%m") + current.strftime("%d")
    tomorrow_date =  current.strftime("%Y") + current.strftime("%m") +str(int(current.strftime("%d"))+1)
    current_espn = url_espn + current_date
    tomorrow_espn= url_espn + tomorrow_date

    espn_list = scrape_espn(current_espn)
    print(espn_list)
    run_total_money_list = scrape_sport_book()
    print(run_total_money_list)
    rank_list = scrape_rank()
    print(rank_list)
    print("here")


