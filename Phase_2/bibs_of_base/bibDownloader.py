from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
import sys
import telegram_send


def bibDownloader(driver,partialPaperName,err_file):
    driver.get("https://connectedpapers.com/")

    inputBox = driver.find_element_by_xpath('//*[@id="desktop-app"]/div[2]/div[1]/div[1]/div/div/div[1]/div/input')
    # print("input box xpath")


    inputBox.send_keys(partialPaperName)
    time.sleep(3)
    # Full dropdown list div
    try:
        a = driver.find_elements_by_xpath('//*[@id="desktop-app"]/div[2]/div[1]/div[1]/div/div/div[2]')
        b = a[0].find_elements_by_class_name('autocomplete-results-item')
    except:
        with open(err_file,'a+') as f:
            f.write(str(partialPaperName)+'\n')
        return
    # print(len(b),b)
    # b contains the autocomplete results
    # b[x] should be b of index that matches closest
    if len(b) == 1:
        c = b[0].find_elements_by_tag_name('div')
        d = c[0].find_elements_by_tag_name('div')
        e = d[0].find_elements_by_tag_name('div')
        f = e[0].find_elements_by_class_name('main-res-text')
        # print(f[0].text)
        f[0].click()   
        # print(driver.current_url) # /graph

        #Takes time to load the graph, so wait

        # print("Waiting for graph to load")
        element = WebDriverWait(driver, 300).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'main-view-window')))
        time.sleep(5)
        # print("Graph Loaded")

        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)

        derivativeWorksButton = driver.find_element_by_xpath('//*[@id="desktop-app"]/div[2]/div[1]/div/button[2]')
        derivativeWorksButton.click() 

        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)
        # print(driver.current_url) #/derivative

        downloadButton = driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div/div/div/div/span')
        downloadButton.click()
        # print("Downloaded Successfully!")
        # time.sleep(5)

    else:
        with open(err_file,'a+') as f:
            f.write(str(partialPaperName)+'\n')

def listdir(dir):
    files = [x for x in os.listdir(dir) if x[-4:]=='.bib']
    return files

def download_all(csv_path,err_file,save_dir,start_index,end_index):
    download_dir = "./Bibs/temp"
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_dir}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromeOptions.add_argument('--headless')
    # chromeOptions.add_experimental_option("prefs",prefs)
    #chromeOptions.add_argument('--headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chromeOptions)
    # with open(name_file,'r') as f:
    #     names = list(set(f.read().splitlines()))
    df = pd.read_csv(csv_path)
    names = list(df['S2 ID'])
    # id = list(df['index'])

    # with open(err_file,'w') as f:
    #     pass

    if(end_index==0):
        end_index = len(df)
    
    # i = 0
    for ind in range(start_index,end_index):
        n = names[ind]
        n = str(n)
        try:
            bibDownloader(driver,n.strip(),err_file)
            f = listdir(download_dir)
            while(len(f)==0):
                f = listdir(download_dir)
            # assert len(f)==1
            # print(f)
            # print(download_dir+'/'+f[0])
            # print(save_dir+'/'+n.lower()+'.bib')
            os.rename(download_dir+'/'+f[0],save_dir+'/'+n.lower()+'.bib')
        except Exception as e:
            print(e)
            print(n, ' Did not work')
            with open(err_file,'a+') as f:
                f.write(n.strip()+'\n')
        
        # i+=1
        if(ind%100==0):
            print('\n',ind, ' done')
        # print(ind, 'worked')

args = sys.argv[1:]

if(len(args)!=2):
    print('Start Index and End Index')
else:
    start_index = int(args[0])
    end_index = int(args[1])

    print('Running between ', start_index, end_index)

    st = time.time()
    download_all('dataset.csv','errors.txt','./Bibs/actual',start_index,end_index)
    en = time.time()
    print('All done in',en-st)

    telegram_token = '1437027031:AAFZ3AiVsGrxNQcWYGrMemHLX4IGqosthjk'
    chat_id = '1422492198'
    path_config = telegram_send.get_config_path()
    with open(path_config, 'w') as f:
        f.write(f'[telegram]\ntoken = {telegram_token}\nchat_id = {chat_id}')
    telegram_send.send(messages=['Check M1'])
