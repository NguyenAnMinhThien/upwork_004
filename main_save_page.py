import datetime
import bottle_neck
import zipfile
import os
from selenium import webdriver
import  main_functions
from bottle_neck import final_lists


def get_chromedriver(use_proxy=False, user_agent=None):
    PROXY_HOST = "154.6.115.218"  # rotating  web scraping proxy
    PROXY_PORT = 6687
    PROXY_USER = "qaibfgfd"
    PROXY_PASS = "wdquza3u1uoh"

    manifest_json = """
    {
        "name": "Chrome Proxy",
        "description": "Use proxy with auth",
        "version": "1.0.0",
        "manifest_version": 3,
        "permissions": [
            "proxy",
            "storage",
            "scripting",
            "tabs",
            "unlimitedStorage",
            "webRequest",
            "webRequestAuthProvider"
        ],
        "host_permissions": [
            "<all_urls>"
        ],
        "background": {
            "service_worker": "background.js"
        },
        "action": {
            "default_title": "Proxy Extension"
        }
    }
    """

    background_js = """
    chrome.runtime.onInstalled.addListener(() => {
        const config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
            }
        };
        chrome.proxy.settings.set(
            {value: config, scope: "regular"},
            () => {}
        );
    });

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        },
        {urls: ["<all_urls>"]},
        ["blocking"]
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = "proxy_auth_plugin.zip"

        with zipfile.ZipFile(pluginfile, "w") as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
        chrome_options.add_argument(
            "--proxy-server=http://%s:%s" % (PROXY_HOST, PROXY_PORT)
        )
        # chrome_options.add_argument('--headless=new')
    if user_agent:
        chrome_options.add_argument("--user-agent=%s" % user_agent)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

if __name__ == "__main__":
    driver = get_chromedriver(use_proxy=True)

    url_espn = 'https://www.espn.com/mlb/schedule/_/date/'
    current = datetime.datetime.now()
    current_date = current.strftime("%Y") + current.strftime("%m") + current.strftime("%d")
    tomorrow_date =  current.strftime("%Y") + current.strftime("%m") +str(int(current.strftime("%d"))+1)
    current_espn = url_espn + current_date
    tomorrow_espn= url_espn + tomorrow_date

    print("\nIs scraping Schedule\n")
    espn_list = main_functions.scrape_espn(driver,tomorrow_espn)
    print(espn_list)
    print("\nIs scraping TotalOdd\n")
    run_total_money_list = main_functions.scrape_sport_book(driver)
    print(run_total_money_list)
    print("\nIs scraping Ranking\n")
    rank_list = main_functions.scrape_rank(driver)
    print(rank_list)

    driver.quit()

    espn_list = bottle_neck.espn_list
    run_total_money_list = bottle_neck.run_total_money_list
    rank_list = bottle_neck.rank_list

    print("Is pulishing data")
    final_lists =  main_functions.combine_list(espn_list, run_total_money_list, rank_list)
    main_functions.import_sheet(final_lists)
    print("here")


