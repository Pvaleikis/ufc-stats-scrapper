from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import re
import pandas as pd
import time

web = "http://ufcstats.com/statistics/events/completed" #sita nuoroda suskirsto dar skaiciais
#web = "http://ufcstats.com/statistics/events/completed?page=all"
#path = 'C:\ChromeDriver\chromedriver.exe'
#driver = webdriver.Chrome(path)

serv = Service(ChromeDriverManager().install())
opt = Options()

driver = webdriver.Chrome(service=serv, options=opt)

driver.get(web)
driver.maximize_window()

def if_exists(context, xpath_code):
    try:
        context.find_elements(By.XPATH,xpath_code)
        
    except:
        return "Contender fight"
    return "World title fight"

time.sleep(3)
events = driver.find_elements(By.XPATH,'//a[contains(@href, "http://ufcstats.com/event-details/")]')
event_links = [event.get_attribute('href') for event in events]
event_links.pop(0)



# dadeti kitus eventus






# for event in events:
#     print(event.text)

#Loopas visiems eventams

for event_link in event_links:
    driver.get(event_link)
    time.sleep(3)


    event_name = driver.find_element(By.XPATH,'//h2[contains(@class, "content__title")]').text
    event_data = driver.find_elements(By.XPATH,'//ul/li[contains(text(), "")]')
    event_date = event_data[0].text
    event_location = event_data[1].text

    fights = driver.find_elements(By.XPATH,'//tr[contains(@data-link, "http://ufcstats.com/fight-details")]')

    event_names = []
    winners = []
    losers = []
    results = []
    w_k_downs = []#winner knock downs
    l_k_downs = []#loser knock downs
    w_strikes = []#winner/loser sig strikes
    l_strikes = [] 
    w_t_downs = []
    l_t_downs = []
    w_sub_atmpt = []
    l_sub_atmpt = []
    weight_classes = []
    methods = []
    rounds = []
    times = []
    fight_types = []
    bonuses = []

    print(event_name)
    print(event_date)
    print(event_location)
    event_date = re.sub(r'[^\w]+', ' ', event_date)
    event_name = re.sub(r'[^\w]', ' ', event_name)

    event_csv_name = event_name.split(' ')[0] + event_name.split(' ')[1] + '_' + event_date.split(' ')[1] + '_' + event_date.split(' ')[2] + '_' + event_date.split(' ')[3] + '.csv'

    print(event_csv_name)

    for fight in fights:

        fighters = fight.find_elements(By.XPATH,'.//a[contains(@href, "http://ufcstats.com/fighter-details")]')
        result = fight.find_element(By.XPATH,'.//i[contains(@class, "b-flag__text")]').text
        stats = fight.find_elements(By.XPATH,'.//td')
        knock_downs = stats[2].find_elements(By.XPATH,'./p')
        strike_count = stats[3].find_elements(By.XPATH,'./p')
        take_downs = stats[4].find_elements(By.XPATH,'./p')
        sub_atempts = stats[5].find_elements(By.XPATH,'./p')
        weight_class = stats[6].find_element(By.XPATH,'./p').text

        ## make this into a function
        try:
            title = stats[6].find_element(By.XPATH,'./p/img[contains(@src, "belt.png")]')
            fight_type = "World title fight"
        except:
            fight_type = "Contender fight"

    
        # title = get_title(stats[6], './p/img[contains(@src, "belt.png")]')
        # print(stats[6])

        method = stats[7].find_element(By.XPATH,'./p').text
        round = stats[8].find_element(By.XPATH,'./p').text
        time_ = stats[9].find_element(By.XPATH,'./p').text

        winners.append(fighters[0].text)
        losers.append(fighters[1].text)
        results.append(result)

        w_k_downs.append(knock_downs[0].text)
        l_k_downs.append(knock_downs[1].text)

        w_strikes.append(strike_count[0].text)
        l_strikes.append(strike_count[1].text)

        w_t_downs.append(take_downs[0].text)
        l_t_downs.append(take_downs[1].text)

        w_sub_atmpt.append(sub_atempts[0].text)
        l_sub_atmpt.append(sub_atempts[1].text)
        
        fight_types.append(fight_type)
        print(fight_type)
        weight_classes.append(weight_class)
        methods.append(method)
        rounds.append(round)
        times.append(time_)
        event_names.append(event_name)



    fights_df = pd.DataFrame.from_dict({"Event_name": event_names, "Result": results, "Winner": winners, "Loser" : losers, "Knockdowns by winner": w_k_downs, 
                                        "Knockdowns by loser": l_k_downs, "Sig. strikes by winner": w_strikes, "Sig. strikes by loser": l_strikes, 
                                        "Takedowns by winner": w_t_downs,"Takedowns by loser": l_t_downs, "Sub. attempts by winner": w_sub_atmpt, "Sub. attempts by loser": l_sub_atmpt,
                                        "Fight type": fight_types, "weight_class": weight_classes, "Round": rounds,"time": times})


    fights_df.to_csv('ufc_events' + '/' + event_csv_name)

driver.quit()