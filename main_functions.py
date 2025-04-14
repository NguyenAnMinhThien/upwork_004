from selenium.webdriver.support import expected_conditions
import datetime
import time
import re
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support.ui import WebDriverWait
import pygsheets
import proxyscrape
from bottle_neck import run_total_money_list, rank_list


def rotate_proxy():
    proxy = proxyscrape.proxy
    return random.choice(proxy)


def import_sheet(data):
    # authorization
    gc = pygsheets.authorize(client_secret='client_secret.json')
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1d0si0OqSwAL9gvsUJxxcQalcUTsi-qkrciWhdCXxQtQ/edit?gid=0#gid=0')
    # select the first sheet
    wks = sh[0]
    for row in data:
        try:
            wks.append_table(values=row)
        except Exception as e:
            pass


def scrape_espn(driver,url):
    print(datetime.datetime.now(), "\n")
    driver.get(url)
    WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "ResponsiveTable")))
    tomorrow_schedules = driver.find_elements(By.CLASS_NAME, "ResponsiveTable")
    # heree
    # 1.Create a list of all link game
    table = tomorrow_schedules[0].find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody")
    matchups = table.find_elements(By.TAG_NAME, "tr")
    link_games = list()
    for item in matchups:
        link_game = item.find_element(By.CLASS_NAME, "date__col").find_element(By.TAG_NAME, "a").get_attribute("href")
        game_team_pitcher = item.text.split("\n")

        for pitching_matchup in game_team_pitcher:
            if pitching_matchup.__contains__(" vs "):
                pitching = pitching_matchup
                break
        data_row = [game_team_pitcher[3],game_team_pitcher[0],pitching.split(" vs ")[0],game_team_pitcher[2],pitching.split(" vs ")[1],link_game]

        # data_row: it is combined with all data necessary before enter to each page to get predictor
        link_games.append(data_row)

        # 2.with each linkgame, create the data equivalent to
    espn_final = list()
    espn_finals = list()
    # Create a for loop here to run for each link games have scraped
    for data_row in link_games:
        try:
            print(data_row[-1], "\n")
            driver.get(data_row[-1])
            WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "PageLayout__Main")))
            print("Getting content in section")
            # espn_news = driver.find_element(By.CLASS_NAME, "PageLayout__Main").find_element(By.XPATH,
            #                                                                                 '//section[@data-testid="prism-LayoutCard"]')
            # # Surely will get corrected, no use this
            # # if espn_news[1].text.__contains__("Game Odds"):
            # #     espn_new_element = espn_news[1]
            # # elif espn_news[0].text.__contains__("Game Odds"):
            # #     espn_new_element = espn_news[0]
            # # else:
            # #     raise Exception
            # espn_new = espn_news.text.split("\n")
            # series = [2, 7, 8, 16, 17]
            # for serie in series:
            #     espn_final.append(re.sub('\(.*\)', '', espn_new[serie]))
            matchup_predictor = driver.find_elements(By.CLASS_NAME, "matchupPredictor__teamValue")
            print("Finished getting predictor")
            espn_final = data_row[:5]
            espn_final.append(matchup_predictor[0].text)
            espn_final.append(matchup_predictor[1].text)
            espn_final.append(data_row[-1])
            espn_finals.append(espn_final.copy())
            espn_final.clear()
        except Exception as e:
            print(f"Exception at: {data_row}\n")
            pass
    #     1,2,5 is left; 3,4,6 is right
    dict_match_name = dict()
    for rtm in espn_finals:
        mismatch_name1 = rtm[1]
        mismatch_name2 = rtm[3]
        for item in rank_list:
            if item.__contains__(mismatch_name1.split()[-1]):
                dict_match_name[mismatch_name1] = item
            elif item.__contains__(mismatch_name2.split()[-1]):
                dict_match_name[mismatch_name2] = item
        #         Assign again the value of some wrong assign dueto the previous one.
    dict_match_name['Chicago'] = 'Chicago Cubs'
    dict_match_name['New York'] = 'New York Yankees'
    dict_match_name['Los Angeles'] = 'Los Angeles Dodgers'
    print(dict_match_name)
    for item in espn_finals:
        item[1] = dict_match_name[item[1]]
        item[3] = dict_match_name[item[3]]

    return espn_finals


def scrape_sport_book(driver):
    print(datetime.datetime.now())
    # 1. Consider if this time is corrected to scrape ?
    driver.get('https://sportsbook.draftkings.com/leagues/baseball/mlb')
    WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "sportsbook-table")))

    odd_tables = driver.find_elements(By.CLASS_NAME, "sportsbook-table")
    # if odd_tables.__len__() == 2:
    #     print("Script can not run now, output flag to a file outside")
    #     odd_table = odd_tables[1]
    # else:
    #     odd_table = odd_tables[0]

    # Edit for remote server, no matter table is devided
    draftking_lists = list()
    draftking_list = list()
    for odd_table in odd_tables:
        odd_rows = odd_table.find_elements(By.TAG_NAME, "tr")
        # 2.Scrape rows in that table
        for odd_row in odd_rows:
            if (odd_row.text.__contains__("TOMORROW") == False):
                team_name = odd_row.find_element(By.TAG_NAME, "th").text.split("\n")[0]
                if team_name.__contains__("AM") or team_name.__contains__("PM"):
                    team_name = odd_row.find_element(By.TAG_NAME, "th").text.split("\n")[1]
                draftking_list.append(team_name)
                # print(team_name)
                run_total_money = odd_row.find_elements(By.TAG_NAME, "td")
                draftking_list.append(run_total_money[0].text)
                draftking_list.append(run_total_money[1].text)
                draftking_list.append(run_total_money[2].text)
                draftking_lists.append(draftking_list.copy())
                draftking_list.clear()
    return draftking_lists


def scrape_rank(driver):
    print(datetime.datetime.now())
    driver.get('https://www.mlb.com/standings/mlb')

    WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "standings-app-root")))
    rank_data = (driver.find_element(By.ID, "standings-app-root").text.split("\n"))
    toggle = 0
    rank_list = list()
    for rank_maybe in rank_data:
        if rank_maybe.__contains__('W L PCT GB'):
            print("start from here")
            toggle = 1
            continue
        if toggle == 1 and (re.search("\d", rank_maybe)) == None and rank_maybe.strip() != '' and rank_maybe.__contains__('Glossary') == False:
            if not (rank_maybe.__contains__("@") or rank_maybe.__contains__("vs")):
                rank_list.append(rank_maybe)
    return rank_list


def combine_list(espn_list, run_total_money_list, rank_list):
    dict_match_name = dict()
    for rtm in run_total_money_list:
        mismatch_name = rtm[0]
        for item in rank_list:
            if item.__contains__(mismatch_name.split()[-1]) and not item.__contains__("Sox"):
                dict_match_name[item] = rtm[1:]
        if mismatch_name == 'CHI White Sox':
            dict_match_name["Chicago White Sox"] = rtm[1:]
        elif mismatch_name == 'BOS Red Sox':
            dict_match_name["Boston Red Sox"] = rtm[1:]
    # 3.Create final lists for import to sheets
    current = datetime.datetime.now()
    time_tomorrow = current.strftime("%m") + "/" + str(int(current.strftime("%d")) + 1) + "/" + current.strftime("%Y")
    final_list = list()
    final_lists = list()
    for item in espn_list:
        final_list.append(time_tomorrow)
        final_list.append(item[0])
        # For team1
        final_list.append(item[1])
        final_list.append(rank_list.index(item[1].strip()) + 1)
        final_list.append(item[5].replace("\n", ''))
        final_list.append("'"+dict_match_name[item[1].strip()][0].split("\n")[0])
        final_list.append(dict_match_name[item[1].strip()][0].split("\n")[1])
        final_list.append(dict_match_name[item[1].strip()][2])

        # For team2
        final_list.append(item[3])
        final_list.append(rank_list.index(item[3].strip()) + 1)
        final_list.append(item[6].replace("\n", ''))
        final_list.append("'"+dict_match_name[item[3].strip()][0].split("\n")[0])
        final_list.append(dict_match_name[item[3].strip()][0].split("\n")[1])
        final_list.append(dict_match_name[item[3].strip()][2])

        # For total over
        final_list.append(dict_match_name[item[1].strip()][1].split("\n")[1])
        final_list.append(dict_match_name[item[1].strip()][1].split("\n")[2])
        # For total under
        final_list.append(dict_match_name[item[3].strip()][1].split("\n")[1])
        final_list.append(dict_match_name[item[3].strip()][1].split("\n")[2])

        # For test scores
        final_list.append('')
        final_list.append('')
        # For the link_game
        final_list.append(item[-1])

        final_lists.append(final_list.copy())
        final_list.clear()
    return final_lists
