from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import pandas as pd
import time

web = "http://ufcstats.com/statistics/fighters?char=a"
#path = 'C:\ChromeDriver\chromedriver.exe'

#driver = webdriver.Chrome(path)

serv = Service(ChromeDriverManager().install())
opt = Options()

driver = webdriver.Chrome(service=serv, options=opt)

driver.get(web)
driver.maximize_window()

# alphabet = #get all letter links

nav_bar = driver.find_elements(By.XPATH,'//ul/li/a[contains(@class, "nav-link")]')



nav_links = []

names = []
surnames = []
nicknames = []
heights = []
weights = []
reaches = []
wins = []
losses = []
draws = []
titles = []
stances = []

for nav_link in nav_bar:
    nav = nav_link.get_attribute('href')

    nav_links.append(nav)

# press all

for context in nav_links:
    driver.get(context)
    driver.maximize_window()
    
    all_button = driver.find_element(By.XPATH,'//a[contains(text(), "All")]')
    all_button.click()

    fighters = driver.find_elements(By.XPATH,'//tbody//tr[td/a[contains(@href, "fighter-details")]]')

    for fighter in fighters:
        stats = fighter.find_elements(By.XPATH,'./td')
        nickname = stats[2].text
        names.append(stats[0].text)
        surnames.append(stats[1].text)
        nicknames.append(nickname)
        heights.append(stats[3].text)
        weights.append(stats[4].text)
        reaches.append(stats[5].text)
        stances.append(stats[6].text)
        wins.append(stats[7].text)
        losses.append(stats[8].text)
        draws.append(stats[9].text)

        try:
            title = stats[10].find_element(By.XPATH,'.//img[contains(@src, "belt.png")]')
            titles.append('World champion') 
        except:
            titles.append('Contender')
        print(f'name {nickname}')


fighters_df = pd.DataFrame.from_dict({"Name": names, "Surname": surnames, "Nickname": nicknames, "Height": heights, "Weight": weights,
                                       "Reach": reaches, "Won": wins, "Lost": losses, "Draw": draws, "Title": titles})
fighters_df.to_csv('ufc_roster'+ '/' +'ufc_roster.csv')
driver.quit()