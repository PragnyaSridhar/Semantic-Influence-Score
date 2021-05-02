from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time


def bibDownloader(driver,partialPaperName,err_file):
    driver.get("https://connectedpapers.com/")

    inputBox = driver.find_element_by_xpath('//*[@id="desktop-app"]/div[2]/div[1]/div[1]/div/div/div[1]/div/input')
    # print("input box xpath")


    inputBox.send_keys(partialPaperName)
    time.sleep(3)
    # Full dropdown list div
    a = driver.find_elements_by_xpath('//*[@id="desktop-app"]/div[2]/div[1]/div[1]/div/div/div[2]')
    b = a[0].find_elements_by_class_name('autocomplete-results-item')
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
        element = WebDriverWait(driver, 240).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'main-view-window')))
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
            f.write(partialPaperName)

def download_all(name_file,err_file):
    
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "./Bibs/A"}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromeOptions.add_argument('--headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chromeOptions)
    with open(name_file,'r') as f:
        names = list(set(f.read().splitlines()))

    # with open(err_file,'w') as f:
    #     pass
    
    i = 0
    for n in names:
        try:
            bibDownloader(driver,n.strip(),err_file)
        except:
            print(n, ' Did not work')
            with open(err_file,'a+') as f:
                f.write(n.strip()+'\n')
        
        i+=1
        if(i%100==0):
            print('\n',i, ' done')

download_all('./Name_files/errored_derworks_A.txt','./Name_files/errored_derworks_A2.txt')
print('All done')