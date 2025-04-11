#%%
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions
from selenium.webdriver import Keys, ActionChains
import undetected_chromedriver as uc
#%%
#%%
from undetected_chromedriver import ChromeOptions
options = ChromeOptions()
options.add_argument('--headless=new')

#%%
driver = uc.Chrome(options)
driver.get('https://sportsbook.draftkings.com/leagues/baseball/mlb')
time.sleep(1)
try:
    espn= driver.find_element(By.CLASS_NAME,'sportsbook-responsive-card-container__body')
    if espn != None:
        print(espn.text)
except Exception as e:
    print(e)
#%%
driver.quit()
